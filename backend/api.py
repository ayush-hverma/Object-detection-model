from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
import json
import time
from ObjectDetection import WebcamStream, DetectionEngine

app = FastAPI(title="YOLO26 Object Detection API")

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize detector and stream
vs = WebcamStream(src=0).start()
detector = DetectionEngine(model_name="yolo26n.pt").start()

def generate_frames():
    """MJPEG stream generator with rendered bounding boxes."""
    while True:
        frame = vs.read()
        if frame is None:
            time.sleep(0.01)
            continue

        # Mirror frame horizontally (Webcam feel)
        frame = cv2.flip(frame, 1)

        detector.update_frame(frame)
        detections = detector.get_results()

        # Draw detections on the frame for the video stream
        for det in detections:
            x, y, w, h = det['box']
            color = det['color']
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            
            # Label styling
            (tw, th), _ = cv2.getTextSize(det['label'], cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
            cv2.rectangle(frame, (x, y - th - 10), (x + tw + 10, y), color, -1)
            cv2.putText(frame, det['label'], (x + 5, y - 7), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

        # Encode as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
            
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.get("/video_feed")
async def video_feed():
    """Video streaming route."""
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/detections")
async def get_detections():
    """Endpoint for detection metadata (useful for UI lists)."""
    detections = detector.get_results()
    serializable = []
    for d in detections:
        serializable.append({
            "label": d["label"],
            "box": d["box"],
            "color": [int(c) for c in d["color"]]
        })
    return {
        "count": len(serializable),
        "detections": serializable,
        "timestamp": time.time()
    }

@app.on_event("shutdown")
def shutdown_event():
    vs.stop()
    detector.stop()

if __name__ == "__main__":
    import uvicorn
    # Run API
    print("Starting YOLO26 API on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
