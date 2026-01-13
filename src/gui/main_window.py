import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from src.gui.recognition_ui import RecognitionWindow
from src.gui.management_ui import ManagementWindow
from src.gui.styles import STYLESHEET, BG_COLOR

class LauncherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DeepFace Launcher")
        self.setGeometry(100, 100, 500, 400)
        self.setStyleSheet(STYLESHEET)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)
        self.setLayout(layout)

        label = QLabel("DeepFace Recognition")
        label.setAlignment(Qt.AlignCenter)
        label.setObjectName("h1")
        layout.addWidget(label)

        sub_label = QLabel("Selecione o modo de operação")
        sub_label.setAlignment(Qt.AlignCenter)
        sub_label.setStyleSheet("color: #858585; margin-bottom: 20px;")
        layout.addWidget(sub_label)

        btn_recognition = QPushButton("Iniciar Reconhecimento")
        btn_recognition.setMinimumHeight(50)
        btn_recognition.setStyleSheet("font-size: 16px;")
        btn_recognition.clicked.connect(self.launch_recognition)
        layout.addWidget(btn_recognition)

        btn_management = QPushButton("Gerenciar Usuários")
        btn_management.setMinimumHeight(50)
        btn_management.setStyleSheet("background-color: #3c3c3c; font-size: 16px;")
        btn_management.clicked.connect(self.launch_management)
        layout.addWidget(btn_management)

    def launch_recognition(self):
        self.rec_window = RecognitionWindow()
        self.rec_window.show()
        self.close()

    def launch_management(self):
        self.man_window = ManagementWindow()
        self.man_window.show()
        self.close()

def run_launcher():
    app = QApplication(sys.argv)
    launcher = LauncherWindow()
    launcher.show()
    sys.exit(app.exec())
