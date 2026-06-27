# AI Burning & Micro-Dumping Spot Detection System

An AI-powered monitoring system designed for local panchayats/municipalities to automatically detect illegal solid waste heaps (micro-dumping) and active waste burning (smoke and fire). 

This project is tailored for an MCA academic project, supporting file-based uploads (images and videos) with a centralized inspector dashboard, while remaining fully adaptable for live CCTV/RTSP stream integration.

---

## 📁 Project Structure

```text
AI-Burning-Detection/
├── app/
│   ├── detector.py      # Core YOLO detection & video processing logic
│   ├── dashboard.py     # Streamlit-based Inspector Dashboard
│   └── database.py      # SQLite database manager for violation logs
├── models/
│   └── best.pt          # Trained YOLOv11 model weights
├── uploads/             # Directory for uploaded user images/videos
│   ├── images/
│   └── videos/
├── outputs/             # Directory for annotated output files
│   ├── images/
│   └── videos/
├── logs/                # System logs and databases
│   ├── screenshots/     # Captured evidence screenshots
│   └── violations.db    # SQLite database storing violation records
├── dataset/             # YOLO format dataset (train, valid, test)
├── train.py             # CLI script to train/fine-tune the model
├── detect.py            # CLI script to run detection on files
├── requirements.txt     # Python package requirements
└── data.yaml            # Dataset configuration file
```

---

## 🚀 Getting Started

### 1. Installation & Setup

Ensure you have Python 3.8+ installed. Clone the repository and install the dependencies:

```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Dataset Preparation
Place your dataset under the `dataset/` directory. Ensure the structure matches the one defined in `data.yaml`:
* `dataset/train/images` and `dataset/train/labels`
* `dataset/valid/images` and `dataset/valid/labels`
* `dataset/test/images` and `dataset/test/labels`

### 3. Model Training
To train or fine-tune a YOLOv11 model on your custom dataset:

```bash
python train.py --epochs 50 --batch 16 --imgsz 640
```

This will automatically save the trained weights to `models/best.pt`.

### 4. Running Detection via Command Line
You can run the detection system on local images or videos using the CLI:

```bash
# Detect in an image
python detect.py --image uploads/sample.jpg

# Detect in a video
python detect.py --video uploads/sample.mp4
```

Annotated outputs will be saved in `outputs/images/` or `outputs/videos/`, and violations will be logged in `logs/violations.db`.

### 5. Running the Dashboard
Start the Streamlit dashboard to review violations, upload files interactively, and view analytics:

```bash
streamlit run app/dashboard.py
```

---

## 📊 Inspector Dashboard Features
* **Home**: Key Performance Indicators (KPIs) showing total violations, pending cases, resolved spots, and category-wise counts.
* **Detect**: Interactive upload section supporting both images and videos. Watch detections happen in real-time.
* **Historical Records**: Log table containing all violations. Click on any record to view details and the captured screenshot.
* **Status Management**: Toggle violation status between `Pending`, `Resolved`, and `Spurious` to simulate real-world municipal workflows.
* **Analytics**: Visually rich charts (pie charts, bar charts, line charts) showing violation trends and distributions.

---

## 🔮 Future Enhancements
* Live CCTV and RTSP camera stream integration.
* GPS location tagging and GIS mapping.
* Automated email/SMS alerts to local health inspectors.
* PDF/Excel monthly report generation.
* Cloud database integration (PostgreSQL / Firebase).
