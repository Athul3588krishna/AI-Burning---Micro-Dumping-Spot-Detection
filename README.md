# AI Burning & Micro-Dumping Spot Detection 🛰️🔥

AI-powered computer vision system for real-time monitoring and detection of illegal solid waste micro-dumping spots and open biomass burning.

---

## 🌟 Overview
- **Model:** Fine-tuned YOLOv11 nano model on aerial and CCTV surveillance frames.
- **Classes:** Solid waste heaps (micro-dumping), open fire, and dense smoke plumes.
- **Dashboard:** Interactive Streamlit web interface for live video/image analysis, violation logging, and evidence inspection.
- **Database:** SQLite log store tracking violation timestamps, detection confidence, and snapshot evidence.

---

## 🚀 Quick Start

### 1. Local Setup
```bash
# Clone the repository
git clone https://github.com/Athul3588krishna/AI-Burning---Micro-Dumping-Spot-Detection.git
cd AI-Burning---Micro-Dumping-Spot-Detection

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit Dashboard
streamlit run app/dashboard.py
```

### 2. Docker Deployment
```bash
docker-compose up --build
```
Access the dashboard at `http://localhost:8501`.

---

## 📁 Project Structure
```text
├── app/
│   ├── dashboard.py       # Streamlit UI for monitoring and triage
│   ├── detector.py        # Core YOLOv11 video detection pipeline
│   ├── preprocess.py      # Frame resize & video aspect ratio handler
│   └── database.py        # SQLite violation logger
├── models/
│   └── best.pt            # Fine-tuned model weights
├── tests/
│   └── test_model.py      # Automated sanity tests
├── Dockerfile             # Multi-stage production container
├── docker-compose.yml     # Container orchestration
└── requirements.txt       # Project dependencies
```

---

## 📜 License
MIT License
