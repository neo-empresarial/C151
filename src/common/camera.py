
import cv2
import time
import threading

class CameraManager:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None
        self.running = False
        self.thread = None
        self.lock = threading.Lock()
        self.latest_frame = None
        self.ret = False

    def start(self):
        if self.running:
            return
        
        # Try to find a working camera by scanning indices 0-9
        camera_found = False
        for index in range(10):
            try:
                print(f"Scanning for camera at index {index}...")
                cap = cv2.VideoCapture(index)
                if cap.isOpened():
                    # Try to read a frame to confirm it actually works
                    ret, _ = cap.read()
                    if ret:
                        self.camera_index = index
                        self.cap = cap
                        camera_found = True
                        print(f"Camera found and working at index {index}")
                        break
                    else:
                        cap.release()
                else:
                    cap.release()
            except Exception:
                pass
        
        if not camera_found:
            print("Warning: No working camera found after scanning indices 0-9.")
            # We don't raise an exception here to allow the app to start without a camera
            # The capture loop will just not run or will handle the None cap
            self.running = False
            return

        self.running = True
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()
        print(f"Camera started on index {self.camera_index} in background thread.")

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        if self.cap:
            self.cap.release()
            self.cap = None

    def _capture_loop(self):
        print("Debug: Camera Capture Loop Started")
        while self.running and self.cap:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                with self.lock:
                    self.latest_frame = frame
                    self.ret = True
            else:
                with self.lock:
                    self.ret = False
            time.sleep(0.01)

    def read(self):
        with self.lock:
            if self.ret and self.latest_frame is not None:
                return True, self.latest_frame.copy()
            return False, None
