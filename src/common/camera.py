import cv2
import threading
import time
import logging

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
            
            if self.index is not None:
                logging.debug(f"Tentando abrir a câmera no index {self.index}...")
                self.cap = cv2.VideoCapture(self.index, cv2.CAP_DSHOW)
                if not self.cap.isOpened():
                     self.cap = cv2.VideoCapture(self.index)
                
                # Set Resolution to HD (1280x720) to prevent blur
                if self.cap.isOpened():
                    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
                
                if self.is_working():
                    self.running = True
                    logging.info(f"Câmera {self.index} iniciada com sucesso.")
                    return
                else:
                    logging.warning(f"Falha na câmera {self.index}. Iniciando busca automática...")
                    if self.cap:
                        self.cap.release()

            new_index = self.find_working_camera()
            if new_index is not None:
                self.index = new_index
                self.cap = cv2.VideoCapture(self.index, cv2.CAP_DSHOW)
                if not self.cap.isOpened():
                    self.cap = cv2.VideoCapture(self.index)
                
                # Set Resolution
                if self.cap.isOpened():
                    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

                self.running = True
                logging.info(f"Câmera encontrada e iniciada no index {self.index}.")
            else:
                logging.error("Nenhuma câmera funcional encontrada nos primeiros 10 índices.")
                self.index = 0
                self.cap = cv2.VideoCapture(0)
                
                # Set Resolution
                if self.cap.isOpened():
                    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

                self.running = True

    def is_working(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            return ret and frame is not None
        return False

    def find_working_camera(self, max_check=10):
        logging.debug("Buscando câmera disponível...")
        for i in range(max_check):
            temp_cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            if not temp_cap.isOpened():
                temp_cap = cv2.VideoCapture(i)
            
            if temp_cap.isOpened():
                ret, frame = temp_cap.read()
                temp_cap.release()
                if ret and frame is not None:
                    logging.info(f"Câmera funcional encontrada no index {i}")
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
