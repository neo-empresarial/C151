import cv2
import sys
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication
from PySide6.QtGui import QImage, QPixmap, QPainter, QColor, QPen
from PySide6.QtCore import QTimer, Qt
from src.core.recognition import RecognitionEngine
from src.gui.styles import STYLESHEET

class RecognitionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reconhecimento Facial em Tempo Real")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(STYLESHEET)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.video_label)

        self.engine = RecognitionEngine()
        self.engine.start()

        self.cap = cv2.VideoCapture(0)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            
            self.engine.update_frame(frame)
            results = self.engine.get_results()

            for res in results:
                x, y, w, h = res["box"]
                name = res["name"]
                known = res["known"]
                
                color = (0, 255, 0) if known else (0, 0, 255)
                
                self.draw_corners(frame, x, y, w, h, color)
                
                cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            
            scaled_pixmap = pixmap.scaled(self.video_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.video_label.setPixmap(scaled_pixmap)

    def draw_corners(self, img, x, y, w, h, color, thickness=3, length=20):
        cv2.line(img, (x, y), (x + length, y), color, thickness)
        cv2.line(img, (x, y), (x, y + length), color, thickness)
        cv2.line(img, (x + w, y), (x + w - length, y), color, thickness)
        cv2.line(img, (x + w, y), (x + w, y + length), color, thickness)
        cv2.line(img, (x, y + h), (x + length, y + h), color, thickness)
        cv2.line(img, (x, y + h), (x, y + h - length), color, thickness)
        cv2.line(img, (x + w, y + h), (x + w - length, y + h), color, thickness)
        cv2.line(img, (x + w, y + h), (x + w, y + h - length), color, thickness)

    def closeEvent(self, event):
        self.engine.stop()
        self.cap.release()
        event.accept()

def run_recognition():
    app = QApplication(sys.argv)
    window = RecognitionWindow()
    window.show()
    sys.exit(app.exec())
