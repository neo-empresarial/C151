
import sys
import argparse
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt

from src.common.styles import STYLESHEET
from src.features.cadastro.ui_cadastro import ManagementWindow
from src.features.inferencia.ui_inferencia import RecognitionWindow

class LauncherWindow(QWidget):
    def __init__(self, exit_on_detect=False):
        super().__init__()
        self.setWindowTitle("DeepFace Industrial Launcher")
        self.setGeometry(100, 100, 600, 500)
        self.setStyleSheet(STYLESHEET)
        
        self.exit_on_detect = exit_on_detect
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(60, 60, 60, 60)
        self.setLayout(layout)

        # Title
        title = QLabel("Sistema de Controle de Acesso")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        layout.addWidget(title)

        subtitle = QLabel("Selecione o Módulo Operacional")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #666; font-size: 16px; margin-bottom: 30px;")
        layout.addWidget(subtitle)

        # Buttons
        btn_rec = QPushButton("INICIAR RECONHECIMENTO")
        btn_rec.setMinimumHeight(60)
        btn_rec.setObjectName("primary")
        btn_rec.setStyleSheet("font-size: 18px;")
        btn_rec.clicked.connect(self.launch_recognition)
        layout.addWidget(btn_rec)

        btn_cad = QPushButton("GERENCIAMENTO DE USUÁRIOS")
        btn_cad.setMinimumHeight(60)
        btn_cad.setStyleSheet("font-size: 18px;")
        btn_cad.clicked.connect(self.launch_management)
        layout.addWidget(btn_cad)


        # Footer
        footer = QLabel("v2.1")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #999; margin-top: 20px;")
        layout.addWidget(footer)

    def launch_recognition(self):
        self.rec_window = RecognitionWindow(exit_on_detect=self.exit_on_detect)
        self.rec_window.closed.connect(self.show)
        self.rec_window.show()
        self.hide()

    def launch_management(self):
        self.man_window = ManagementWindow()
        self.man_window.show()
        # Should management close launcher? Usually no, opens as separate window or modal.
        # But if we want single-window feel:
        # self.hide()
        # self.man_window.closeEvent = lambda e: self.show() 
        # For now, let's keep launcher open or use same pattern
        # Simple pattern: Open separate, keep launcher.

def main():
    parser = argparse.ArgumentParser(description="DeepFace Industrial App")
    parser.add_argument("--exit-on-detect", action="store_true", help="Close application immediately upon detecting a known user.")
    args = parser.parse_args()

    app = QApplication(sys.argv)
    
    # If exit-on-detect is strictly for automation, maybe we want to launch directly into recognition?
    # Requirement: "Ao identificar o usuário o software precisa sair"
    # Usually this implies auto-start if flag is present? 
    # Or just config for the runtime. 
    # Assuming user still launches via GUI button unless another flag says otherwise.
    # But if it's for automation, maybe launch directly.
    # Let's support both. For now simple flag passed to Launcher.
    
    launcher = LauncherWindow(exit_on_detect=args.exit_on_detect)
    launcher.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
