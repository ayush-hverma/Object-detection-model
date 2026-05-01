import cv2
import numpy as np
import threading
import time
import os
from ultralytics import YOLO
from huggingface_hub import hf_hub_download

class WebcamStream:
    """
    Handles webcam frame capture in a separate thread to ensure 
    the video buffer is always fresh and the main loop never blocks.
    """
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
        self.lock = threading.Lock()

    def start(self):
        t = threading.Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return
            (grabbed, frame) = self.stream.read()
            with self.lock:
                self.grabbed = grabbed
                self.frame = frame

    def read(self):
        with self.lock:
            return self.frame.copy() if self.frame is not None else None

    def stop(self):
        self.stopped = True
        self.stream.release()

class DetectionEngine:
    """
    Handles heavy YOLO26 inference in a background thread.
    """
    def __init__(self, model_name="yolo26n.pt", repo_id="ayush-hverma/yolo26_model"):
        print(f"Loading {model_name} network...")
        
        # Ensure model exists locally, otherwise pull from Hugging Face
        if not os.path.exists(model_name):
            print(f"Model '{model_name}' not found locally. Downloading from Hugging Face ({repo_id})...")
            try:
                hf_hub_download(repo_id=repo_id, filename=model_name, local_dir=".")
                print("Download complete.")
            except Exception as e:
                print(f"Warning: Failed to download from Hugging Face: {e}")
                print("Attempting to continue with default YOLO initialization...")

        try:
            self.model = YOLO(model_name)
            
            # Save a backup to the model folder
            os.makedirs("yolo26_model", exist_ok=True)
            self.model.save(os.path.join("yolo26_model", model_name))
            
        except Exception as e:
            raise Exception(f"Failed to initialize YOLO26: {e}")
            
        self.current_frame = None
        self.results = []
        self.stopped = False
        self.lock = threading.Lock()
        print("Detection Engine ready.")

    def start(self):
        t = threading.Thread(target=self.detect, args=())
        t.daemon = True
        t.start()
        return self

    def update_frame(self, frame):
        with self.lock:
            self.current_frame = frame

    def get_results(self):
        with self.lock:
            return self.results

    def detect(self):
        while not self.stopped:
            local_frame = None
            with self.lock:
                if self.current_frame is not None:
                    local_frame = self.current_frame.copy()
            
            if local_frame is not None:
                # YOLO26 Inference (End-to-End, no manual NMS needed)
                # We use stream=True for high-frequency loops
                results = self.model(local_frame, conf=0.5, verbose=False, stream=True)
                
                new_results = []
                for r in results:
                    for box in r.boxes:
                        # Get box coordinates
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        w, h = x2 - x1, y2 - y1
                        
                        # Get class info
                        cls_id = int(box.cls[0])
                        label = r.names[cls_id]
                        conf = float(box.conf[0])
                        
                        # Stable color based on class ID
                        np.random.seed(cls_id)
                        color = tuple(np.random.randint(0, 255, size=3).tolist())
                        
                        display_label = f"{label} {conf:.2f} ({w}x{h})"
                        new_results.append({
                            'box': (x1, y1, w, h),
                            'label': display_label,
                            'color': color
                        })
                
                with self.lock:
                    self.results = new_results
            else:
                time.sleep(0.01)

    def stop(self):
        self.stopped = True

def main():
    # Initialize threads
    try:
        vs = WebcamStream(src=0).start()
        # YOLO26 Nano (n) is optimized for edge CPU performance
        detector = DetectionEngine(model_name="yolo26n.pt").start()
    except Exception as e:
        print(f"Initialization failed: {e}")
        return

    print("\n" + "="*57)
    print("Model saved to: 'yolo26_model/'")
    print("Press 'q' to quit.")
    print("="*57 + "\n")

    while True:
        # 1. Grab latest frame
        frame = vs.read()
        if frame is None:
            continue

        # 2. Update detector with the new frame
        detector.update_frame(frame)

        # 3. Get latest detection results
        detections = detector.get_results()

        # 4. Draw detections on the frame
        for det in detections:
            x, y, w, h = det['box']
            color = det['color']
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            
            # Label styling
            (tw, th), _ = cv2.getTextSize(det['label'], cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
            cv2.rectangle(frame, (x, y - th - 10), (x + tw + 10, y), color, -1)
            cv2.putText(frame, det['label'], (x + 5, y - 7), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

        # 5. Show frame
        cv2.imshow("YOLO26 Object Detection (Ultra-Smooth)", frame)

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    vs.stop()
    detector.stop()
    cv2.destroyAllWindows()
    print("Cleaned up successfully.")

if __name__ == "__main__":
    main()
