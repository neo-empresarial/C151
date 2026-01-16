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
            
            # Try the configured index first
            if self.index is not None:
                print(f"DEBUG: Tentando abrir a câmera no index {self.index}...", flush=True)
                self.cap = cv2.VideoCapture(self.index, cv2.CAP_DSHOW)
                if not self.cap.isOpened():
                     self.cap = cv2.VideoCapture(self.index)
                
                if self.is_working():
                    self.running = True
                    print(f"DEBUG: Câmera {self.index} iniciada com sucesso.", flush=True)
                    return
                else:
                    print(f"DEBUG: Falha na câmera {self.index}. Iniciando busca automática...", flush=True)
                    if self.cap:
                        self.cap.release()

            # Auto search
            new_index = self.find_working_camera()
            if new_index is not None:
                self.index = new_index
                self.cap = cv2.VideoCapture(self.index, cv2.CAP_DSHOW)
                if not self.cap.isOpened():
                    self.cap = cv2.VideoCapture(self.index)
                self.running = True
                print(f"DEBUG: Câmera encontrada e iniciada no index {self.index}.", flush=True)
            else:
                print("DEBUG: Nenhuma câmera funcional encontrada nos primeiros 10 índices.", flush=True)
                # Initialize with 0 anyway to avoid crashes, even if it doesn't work
                self.index = 0
                self.cap = cv2.VideoCapture(0) 
                self.running = True

    def is_working(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            return ret and frame is not None
        return False

    def find_working_camera(self, max_check=10):
        print("DEBUG: Buscando câmera disponível...", flush=True)
        for i in range(max_check):
            # Skip the current index if we already tried it
            # if self.index is not None and i == self.index: continue
            
            temp_cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            if not temp_cap.isOpened():
                temp_cap = cv2.VideoCapture(i)
            
            if temp_cap.isOpened():
                ret, frame = temp_cap.read()
                temp_cap.release()
                if ret and frame is not None:
                    print(f"DEBUG: Câmera funcional encontrada no index {i}", flush=True)
                    return i
        return None

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
