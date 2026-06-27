import cv2
from ultralytics import YOLO

from app.config import (
    MODEL_PATH,
    VIDEO_PATH,
    CONFIDENCE_THRESHOLD,
    CLASSES
)

from app.database import (
    create_database,
    insert_violation
)

from app.utils import (
    save_screenshot,
    get_timestamp,
    draw_detection
)


class WasteDetector:

    def __init__(self):

        self.model = YOLO(MODEL_PATH)

        create_database()

    def run(self):

        cap = cv2.VideoCapture(VIDEO_PATH)

        camera_id = "CAM_001"

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            results = self.model.predict(
                frame,
                conf=CONFIDENCE_THRESHOLD,
                verbose=False
            )

            for result in results:

                boxes = result.boxes

                for box in boxes:

                    cls = int(box.cls[0])

                    confidence = float(box.conf[0])

                    x1, y1, x2, y2 = map(
                        int,
                        box.xyxy[0]
                    )

                    label = CLASSES[cls]

                    draw_detection(
                        frame,
                        x1,
                        y1,
                        x2,
                        y2,
                        label,
                        confidence
                    )

                    image_path = save_screenshot(frame)

                    insert_violation(
                        camera_id,
                        label,
                        confidence,
                        get_timestamp(),
                        image_path
                    )

            cv2.imshow(
                "AI Burning & Micro-Dumping Detection",
                frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()

        cv2.destroyAllWindows()