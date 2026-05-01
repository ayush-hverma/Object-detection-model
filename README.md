# 🚀 YOLO26 Real-Time Object Detection (Hugging Face Edition)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Ultralytics](https://img.shields.io/badge/Ultralytics-YOLO26-orange.svg)](https://ultralytics.com/)
[![Hugging Face Model](https://img.shields.io/badge/%F0%9F%A4%97-Model%20on%20HF-yellow.svg)](https://huggingface.co/ayu5hh/object-detection-model)

This project features a high-performance, real-time object detection engine powered by the **YOLO26 Nano** architecture. The model is exclusively hosted on Hugging Face for seamless deployment across different systems.

---

## 📥 Getting the Model

The model is hosted on Hugging Face as `ayu5hh/object-detection-model`. To use it on a new system, you must pull the weights from the hub.

### 1. Install Hugging Face Hub
```bash
pip install huggingface_hub
```

### 2. Download the Model
You can download the model file directly into the project directory:
```bash
hf download ayu5hh/object-detection-model yolo26n.pt --local-dir .
```

---

## 🧪 Testing on a Different System

Follow these steps to ensure the model works correctly on a fresh installation:

### Step 1: Clone & Environment Setup
```bash
git clone https://github.com/ayush-hverma/Object-detection-model.git
cd Object-detection-model

# Recommended: Create a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Verify Hardware (Webcam)
Ensure your system has a functional webcam. The script defaults to `src=0`. If you have multiple cameras, you may need to adjust the `WebcamStream(src=0)` line in `ObjectDetection.py`.

### Step 4: Run the Model
```bash
python ObjectDetection.py
```

### Step 5: Expected Behavior
- A window titled **"YOLO26 Object Detection"** should appear.
- You should see a live video feed with **bounding boxes** and **labels** (e.g., "person", "cell phone") around detected objects.
- The console should log: `Loading yolo26n.pt network...` and `Detection Engine ready.`

---

## 🏗️ Architecture Features

- **HF-First Workflow**: No manual weight management; pull directly from the cloud.
- **Async Threading**: Decoupled inference prevents video lag, maintaining a high FPS on the display thread.
- **Nano-Scale Efficiency**: Optimized for CPU-based real-time detection without requiring expensive GPUs.

---

## 🛠️ Troubleshooting

- **Model Not Found**: Ensure `yolo26n.pt` is in the root directory or the `yolo26_model/` folder.
- **Camera Error**: Check if another application is using the webcam.
- **Missing Dependencies**: Re-run `pip install -r requirements.txt` to ensure `ultralytics` and `opencv-python` are installed.

---

## 🤝 Support
For issues with the model weights, visit the [Hugging Face Repository](https://huggingface.co/ayu5hh/object-detection-model).
