
import cv2
import sys
from src.common.camera import CameraManager
from src.common.database import DatabaseManager
from src.features.inferencia.engine import InferenceController

class LoadingOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #f9f9f9;")
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)
        
        lbl = QLabel("Iniciando Sistema de Reconhecimento")
        lbl.setStyleSheet("color: #333; font-size: 20px; font-weight: 600;")
        lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl)
        
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.setFixedWidth(300)
        self.progress.setStyleSheet("""
            QProgressBar {
                background-color: #e0e0e0; 
                border-radius: 2px; 
                height: 4px;
            }
            QProgressBar::chunk {
                background-color: #0067c0; /* Windows Blue */
            }
        """)
        layout.addWidget(self.progress)

class RecognitionWindow(QWidget):
    closed = Signal()

    def __init__(self, exit_on_detect=False):
        super().__init__()
        self.setWindowTitle("Reconhecimento")
        self.resize(1024, 768)
        self.setStyleSheet("background-color: #202020;") 

        self.exit_on_detect = exit_on_detect
        self.db_manager = DatabaseManager()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("background-color: black;")
        layout.addWidget(self.video_label)
        
        self.loading_overlay = LoadingOverlay(self)
        
        self.lbl_status = QLabel("Inicializando...", self)
        self.lbl_status.setStyleSheet("""
            QLabel {
                color: white; 
                background-color: rgba(0,0,0,150); 
                padding: 10px 20px; 
                border-radius: 20px;
                font-size: 14px;
            }
        """)
        self.lbl_status.setAlignment(Qt.AlignCenter)
        self.lbl_status.resize(300, 40)
        self.lbl_status.move(20, 20) # Top Left

        self.btn_exit = QPushButton("✕", self)
        self.btn_exit.setFixedSize(40, 40)
        self.btn_exit.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 50);
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 180);
            }
        """)
        self.btn_exit.clicked.connect(self.close)
        
        self.camera_manager = CameraManager()
        self.camera_manager.frame_captured.connect(self.on_camera_frame)
        self.camera_manager.error_occurred.connect(self.on_error)
        
        self.controller = InferenceController(self.db_manager)
        self.controller.worker.results_ready.connect(self.on_ai_results)
        self.controller.worker.model_loaded.connect(self.on_model_loaded)
        
        self.controller.start()
        self.camera_manager.start()
        
    def resizeEvent(self, event):
        self.loading_overlay.resize(self.size())
        self.btn_exit.move(self.width() - 60, 20)
        super().resizeEvent(event)

    def on_model_loaded(self):
        self.loading_overlay.hide()
        self.lbl_status.setText("Aguardando Rosto...")

    def on_camera_frame(self, frame):
        self.controller.update_frame(frame)

    def on_ai_results(self, frame, results):
        draw_frame = frame.copy()
        
        detected_known = False
        names = []

        for res in results:
            x, y, w, h = res["box"]
            name = res["name"]
            known = res["known"]
            
            color = (0, 255, 0) if known else (0, 0, 255) 
            
            cv2.rectangle(draw_frame, (x, y), (x+w, y+h), color, 2)
            
            cv2.rectangle(draw_frame, (x, y-30), (x+w, y), color, cv2.FILLED)
            
            if known:
                detected_known = True
                names.append(name)
                text = f"{name}"
                cv2.putText(draw_frame, text, (x + 5, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2)
            else:
                 cv2.putText(draw_frame, "Desconhecido", (x + 5, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

        rgb_image = cv2.cvtColor(draw_frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        scaled = pixmap.scaled(self.video_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.video_label.setPixmap(scaled)
        
        if detected_known:
             self.lbl_status.setText(f"Olá, {names[0]}!")
             if self.exit_on_detect:
                 self.close()
        else:
             self.lbl_status.setText("Aguardando Rosto...")

    def on_error(self, msg):
        self.lbl_status.setText(f"Erro: {msg}")

    def closeEvent(self, event):
        self.camera_manager.stop()
        self.controller.stop()
        self.closed.emit()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = RecognitionWindow()
    win.show()
    sys.exit(app.exec())
