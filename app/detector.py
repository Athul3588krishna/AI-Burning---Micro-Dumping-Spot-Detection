import os
import cv2
import time
from datetime import datetime
from ultralytics import YOLO
from app.config import MODEL_PATH, CONFIDENCE_THRESHOLD, CLASSES, SCREENSHOT_DIR
from app.database import create_database, insert_violation
from app.utils import draw_detection, save_screenshot, get_timestamp

class WasteDetector:
    def __init__(self, model_path=MODEL_PATH, confidence_threshold=CONFIDENCE_THRESHOLD):
        # Fallback to yolo11n.pt if best.pt is not found or is empty
        if not os.path.exists(model_path) or os.path.getsize(model_path) == 0:
            print(f"Warning: Model weights not found at {model_path}. Falling back to default yolo11n.pt.")
            self.model = YOLO("yolo11n.pt")
        else:
            self.model = YOLO(model_path)
            
        self.confidence_threshold = confidence_threshold
        create_database()

    def detect_image(self, image_path, output_path):
        """
        Runs detection on a single image, saves the annotated output, and logs violations to database.
        """
        frame = cv2.imread(image_path)
        if frame is None:
            raise ValueError(f"Could not read image from {image_path}")

        results = self.model.predict(frame, conf=self.confidence_threshold, verbose=False)
        filename = os.path.basename(image_path)
        detections = []

        annotated_frame = frame.copy()

        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls = int(box.cls[0])
                confidence = float(box.conf[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                # Get the label
                if cls < len(CLASSES):
                    label = CLASSES[cls]
                else:
                    label = result.names.get(cls, f"Class_{cls}")

                # Draw bounding box and label
                draw_detection(annotated_frame, x1, y1, x2, y2, label, confidence)
                
                # Save screenshot of this violation (annotated frame)
                screenshot_path = save_screenshot(annotated_frame)
                
                # Insert into database
                insert_violation(
                    filename=filename,
                    violation_type=label,
                    confidence=confidence,
                    timestamp=get_timestamp(),
                    screenshot_path=screenshot_path,
                    status='Pending'
                )
                
                detections.append({
                    "class": label,
                    "confidence": confidence,
                    "box": (x1, y1, x2, y2)
                })

        # Save the final annotated image
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, annotated_frame)
        
        return detections

    def detect_video(self, video_path, output_path, cooldown_seconds=30.0, progress_callback=None):
        """
        Runs detection on a video frame-by-frame.
        Applies a cooldown mechanism based on video elapsed time to prevent database bloat.
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Could not open video from {video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            fps = 25.0
            
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Setup video writer
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        filename = os.path.basename(video_path)
        
        # Track last logged time for each class: (filename, label) -> video_elapsed_seconds
        last_logged = {}
        violations_logged = 0
        frame_index = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Calculate video playback time in seconds
            video_time = frame_index / fps
            
            results = self.model.predict(frame, conf=self.confidence_threshold, verbose=False)
            annotated_frame = frame.copy()
            
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    cls = int(box.cls[0])
                    confidence = float(box.conf[0])
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    
                    if cls < len(CLASSES):
                        label = CLASSES[cls]
                    else:
                        label = result.names.get(cls, f"Class_{cls}")
                    
                    # Draw detection on the frame
                    draw_detection(annotated_frame, x1, y1, x2, y2, label, confidence)
                    
                    # Cooldown check
                    key = (filename, label)
                    if key not in last_logged or (video_time - last_logged[key]) >= cooldown_seconds:
                        # Save screenshot of the violation frame
                        screenshot_path = save_screenshot(annotated_frame)
                        
                        # Insert into database
                        insert_violation(
                            filename=filename,
                            violation_type=label,
                            confidence=confidence,
                            timestamp=get_timestamp(),
                            screenshot_path=screenshot_path,
                            status='Pending'
                        )
                        
                        last_logged[key] = video_time
                        violations_logged += 1

            # Write the annotated frame to output video
            out.write(annotated_frame)
            
            frame_index += 1
            if progress_callback and total_frames > 0:
                progress_callback(frame_index / total_frames)

        cap.release()
        out.release()
        
        return violations_logged