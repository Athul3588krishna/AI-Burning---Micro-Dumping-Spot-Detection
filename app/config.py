import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "best.pt")

DATABASE_PATH = os.path.join(BASE_DIR, "logs", "violations.db")

SCREENSHOT_DIR = os.path.join(BASE_DIR, "logs", "screenshots")

VIDEO_PATH = os.path.join(BASE_DIR, "videos", "sample.mp4")

CONFIDENCE_THRESHOLD = 0.5

IMAGE_SIZE = 640

CLASSES = [
    "Garbage_Pile",
    "Smoke",
    "Fire"
]