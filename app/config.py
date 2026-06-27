import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "best.pt")

DATABASE_PATH = os.path.join(BASE_DIR, "logs", "violations.db")

SCREENSHOT_DIR = os.path.join(BASE_DIR, "logs", "screenshots")

# Upload and Output Directories
UPLOAD_IMAGE_DIR = os.path.join(BASE_DIR, "uploads", "images")
UPLOAD_VIDEO_DIR = os.path.join(BASE_DIR, "uploads", "videos")
OUTPUT_IMAGE_DIR = os.path.join(BASE_DIR, "outputs", "images")
OUTPUT_VIDEO_DIR = os.path.join(BASE_DIR, "outputs", "videos")

CONFIDENCE_THRESHOLD = 0.5

IMAGE_SIZE = 640

CLASSES = [
    "Garbage_Pile",
    "Smoke",
    "Fire"
]