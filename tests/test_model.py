import os
import pytest

def test_model_weight_file():
    """Verify that YOLO model weight exists."""
    weights = ["yolo11n.pt", "models/best.pt"]
    found = any(os.path.exists(w) for w in weights)
    assert found, "At least one model weights file should be present"

def test_video_directory():
    """Ensure videos directory is accessible."""
    assert os.path.exists("videos"), "videos folder should exist for sample inputs"
