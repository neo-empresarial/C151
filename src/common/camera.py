
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
        
        try:
            for attempt in range(3):
                self.cap = cv2.VideoCapture(self.camera_index)
                if self.cap.isOpened():
                    break
                else:
                    self.cap.release()
                    self.cap = None
                    time.sleep(0.5)

            if not self.cap or not self.cap.isOpened():
                raise Exception("Não foi possível acessar a câmera após 3 tentativas.")
            
            self.running = True
            self.thread = threading.Thread(target=self._capture_loop, daemon=True)
            self.thread.start()
            print("Camera started in background thread.")
        except Exception as e:
            print(f"Camera Error: {e}")
            self.running = False

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
