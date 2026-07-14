import cv2
import numpy as np

def resize_frame_with_aspect_ratio(frame, target_width=640):
    """Resize frame preserving aspect ratio for faster YOLO inference."""
    h, w = frame.shape[:2]
    if w <= target_width:
        return frame
    ratio = target_width / float(w)
    target_height = int(h * ratio)
    return cv2.resize(frame, (target_width, target_height), interpolation=cv2.INTER_AREA)

def check_video_properties(video_path):
    """Retrieve fps, frame count and duration of input video."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps > 0 else 0
    cap.release()
    return {"fps": fps, "total_frames": total_frames, "duration": round(duration, 2)}
