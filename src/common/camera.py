
import cv2
from PySide6.QtCore import QObject, Signal, QTimer, Qt
from PySide6.QtGui import QImage, QPixmap

class CameraManager(QObject):
    frame_captured = Signal(object) # Emit the raw frame (numpy array)
    frame_pixmap = Signal(object)   # Emit the QPixmap for display
    error_occurred = Signal(str)

    def __init__(self, camera_index=0):
        super().__init__()
        self.camera_index = camera_index
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.running = False

    def start(self):
        if self.running:
            return
        
        try:
            # Retry logic
            for attempt in range(3):
                self.cap = cv2.VideoCapture(self.camera_index)
                if self.cap.isOpened():
                    break
                else:
                    self.cap.release()
                    self.cap = None
                    import time
                    time.sleep(0.5)

            if not self.cap or not self.cap.isOpened():
                self.error_occurred.emit("Não foi possível acessar a câmera após 3 tentativas.")
                return
            
            self.running = True
            self.timer.start(30) # 30ms ~ 33 FPS
        except Exception as e:
            self.error_occurred.emit(str(e))

    def stop(self):
        self.running = False
        self.timer.stop()
        if self.cap:
            self.cap.release()
            self.cap = None
            # Small delay to ensure OS releases resource
            import time
            time.sleep(0.2)

    def update_frame(self):
        if not self.running or not self.cap:
            return

        ret, frame = self.cap.read()
        if ret:
            # Mirror frame
            frame = cv2.flip(frame, 1)
            
            # Emit raw frame
            self.frame_captured.emit(frame)
            
            # Convert to QPixmap
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.frame_pixmap.emit(pixmap)
        else:
            self.error_occurred.emit("Falha na captura do frame.")
