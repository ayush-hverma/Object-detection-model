# 🚀 YOLO26 Intelligent Object Detection Dashboard

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19.0-61DAFB.svg)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite-6.0-646CFF.svg)](https://vitejs.dev/)
[![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97-Hugging%20Face-yellow.svg)](https://huggingface.co/ayu5hh/object-detection-model)

A high-performance, full-stack object detection ecosystem featuring the **YOLO26 Nano** architecture. This project bridges the gap between complex AI inference and a beautiful, user-centric dashboard, delivering real-time insights with ultra-low latency.

---

## ✨ Key Features

- ⚡ **Ultra-Smooth Inference**: Multithreaded architecture decouples webcam capture from AI processing, ensuring a stutter-free 30+ FPS experience.
- 🎨 **Glassmorphic Dashboard**: A premium, responsive UI built with React 19, featuring real-time detection logs, interactive analytics, and smooth Framer Motion animations.
- 📡 **Real-Time Data Streaming**: Utilizes Server-Sent Events (SSE) to push detection metadata to the frontend instantly without polling overhead.
- ☁️ **Cloud-Native Weights**: Automated model synchronization with Hugging Face Hub for seamless deployment across any environment.
- 🪞 **User-Centric Feedback**: Horizontally mirrored video feed for a natural "mirror-like" webcam interaction.
- 📊 **Live Analytics**: Instant object counting and confidence tracking directly on the dashboard.

---

## 🏗️ System Architecture

### Backend (Python/FastAPI)
- **FastAPI**: Serves the MJPEG video stream and SSE metadata.
- **Ultralytics YOLO26**: The engine behind the detections, optimized for CPU/GPU efficiency.
- **OpenCV**: Handles high-speed frame capture and image processing.
- **Async Processing**: Separate threads for capture and detection to maximize throughput.

### Frontend (React/Vite)
- **React 19**: Modern component-based architecture.
- **Framer Motion**: Powering the fluid UI transitions and detection list updates.
- **Lucide React**: Beautiful, consistent iconography.
- **Glassmorphic Design**: A futuristic aesthetic using backdrop-filter blur and subtle gradients.

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/ayush-hverma/Object-detection-model.git
cd Object-detection-model
```

### 2. Backend Setup
```bash
# Move to backend directory
cd backend

# Create & activate virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 3. Model Weight Acquisition
The system is pre-configured to use `yolo26n.pt`. If not present, download it from the Hugging Face Hub:
```bash
pip install huggingface_hub
hf download ayu5hh/object-detection-model yolo26n.pt --local-dir .
```

### 4. Frontend Setup
```bash
# Move to frontend directory
cd ../frontend

# Install packages
npm install
```

---

## 🛠️ Usage

### Run the Backend
From the `backend` directory:
```bash
python api.py
```
The API will be available at `http://localhost:8000`.

### Run the Frontend
From the `frontend` directory:
```bash
npm run dev
```
Open your browser and navigate to `http://localhost:5173`.

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/video_feed` | `GET` | MJPEG Video stream with bounding box overlays. |
| `/detections/stream` | `GET` | SSE stream for real-time detection metadata. |
| `/detections` | `GET` | Snapshot of current detections (JSON). |

---

## 🧪 Technical Deep Dive: Async Inference
To prevent the "laggy video" common in many AI demos, this project implements a dual-buffer multithreaded approach:
1. **Capture Thread**: Continuously pulls frames from the webcam at the hardware's max FPS.
2. **Detection Thread**: Pulls the *latest* available frame, runs YOLO inference, and updates the shared results pool.
3. **API Thread**: Combines the capture and latest results to serve the stream and metadata independently.

---

## 🤝 Support & Contribution
Model weights are hosted on [Hugging Face](https://huggingface.co/ayu5hh/object-detection-model). For issues or feature requests, please open a GitHub Issue.

Built with ❤️ by [Ayush Verma](https://github.com/ayush-hverma)
