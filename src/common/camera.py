
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

    def _scan_and_connect(self):
        """Scans for available cameras and connects to the first working one."""
        print("DEBUG: Starting camera scan (forcing DirectShow)...")
        
        indices_to_try = list(range(10))
        if self.camera_index in indices_to_try:
            indices_to_try.remove(self.camera_index)
            indices_to_try.insert(0, self.camera_index)
            
        for index in indices_to_try:
            try:
                print(f"DEBUG: Checking camera index {index} with CAP_DSHOW...")
                cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
                if cap.isOpened():
                    ret, _ = cap.read()
                    if ret:
                        self.camera_index = index
                        self.cap = cap
                        print(f"DEBUG: Camera found and working at index {index}")
                        return True
                    else:
                        print(f"DEBUG: Camera at index {index} opened but failed to read frame.")
                        cap.release()
                else:
                     print(f"DEBUG: Could not open camera at index {index}.")
            except Exception as e:
                print(f"DEBUG: Exception checking camera {index}: {e}")
        
        print("DEBUG: No working camera found after scanning all indices.")
        return False

    def start(self):
        if self.running:
            return
        
        print("DEBUG: CameraManager starting...")
        if not self._scan_and_connect():
            print("WARNING: Failed to connect to any camera on startup.")
        
        self.running = True
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()
        print(f"DEBUG: Background capture thread started.")

    def stop(self):
        print("DEBUG: Stopping CameraManager...")
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        if self.cap:
            self.cap.release()
            self.cap = None
        print("DEBUG: CameraManager stopped.")

    def _capture_loop(self):
        print("DEBUG: Camera Capture Loop Active")
        consecutive_errors = 0
        
        while self.running:
            if self.cap is None or not self.cap.isOpened():
                print("DEBUG: No active camera. Attempting to connect/reconnect...")
                if self._scan_and_connect():
                    consecutive_errors = 0
                else:
                    time.sleep(2.0)
                    continue

            try:
                ret, frame = self.cap.read()
                if ret:
                    frame = cv2.flip(frame, 1)
                    with self.lock:
                        self.latest_frame = frame
                        self.ret = True
                    if consecutive_errors > 0:
                        print(f"DEBUG: Camera recovered after {consecutive_errors} errors.")
                    consecutive_errors = 0
                else:
                    consecutive_errors += 1
                    with self.lock:
                        self.ret = False
                    
                    if consecutive_errors % 10 == 0:
                        print(f"DEBUG: Frame capture failed. Consecutive errors: {consecutive_errors}")
                    
                    if consecutive_errors > 30:
                        print("DEBUG: Too many consecutive errors. Releasing camera to trigger rescan.")
                        self.cap.release()
                        self.cap = None
                        
            except Exception as e:
                print(f"DEBUG: Exception in capture loop: {e}")
                consecutive_errors += 1
                if self.cap:
                    self.cap.release()
                    self.cap = None
            
            time.sleep(0.01)

    def read(self):
        with self.lock:
            if self.ret and self.latest_frame is not None:
                return True, self.latest_frame.copy()
            return False, None
