import os
import cv2
from datetime import datetime
from app.config import SCREENSHOT_DIR


def create_directories():
    """
    Create required folders if they don't exist.
    """
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def get_timestamp():
    """
    Return current timestamp.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def generate_filename():
    """
    Generate a unique screenshot filename.
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"


def save_screenshot(frame):
    """
    Save detected frame as an image.
    """
    create_directories()

    filename = generate_filename()
    filepath = os.path.join(SCREENSHOT_DIR, filename)

    cv2.imwrite(filepath, frame)

    return filepath


def draw_detection(frame, x1, y1, x2, y2, label, confidence):
    """
    Draw bounding box and label.
    """

    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    text = f"{label} ({confidence:.2f})"

    cv2.putText(
        frame,
        text,
        (x1, y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )

    return frame