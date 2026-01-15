import cv2
import threading
import time

class CameraManager:
    def __init__(self, index=0):
        self.index = index
        self.cap = None
        self.running = False
        self.lock = threading.Lock()

    def start(self):
        with self.lock:
            if self.running:
                return
            self.cap = cv2.VideoCapture(self.index)
            self.running = True

    def stop(self):
        with self.lock:
            self.running = False
            if self.cap:
                self.cap.release()
                self.cap = None

    def read(self):
        with self.lock:
            if self.cap and self.cap.isOpened():
                return self.cap.read()
            return False, None
