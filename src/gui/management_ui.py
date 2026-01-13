import cv2
import sys
import os
from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLineEdit, QListWidget, QMessageBox, QApplication, QDialog, 
    QListWidgetItem, QFrame
)
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QTimer, Qt, QSize
from src.core.database import DatabaseManager
from src.gui.styles import STYLESHEET, SIDEBAR_COLOR, ACCENT_COLOR, DANGER_COLOR

class UserFormDialog(QDialog):
    def __init__(self, parent=None, db_manager=None, user_name=None):
        super().__init__(parent)
        self.setWindowTitle("Cadastrar Usuário" if not user_name else f"Editar Foto: {user_name}")
        self.setModal(True)
        self.resize(900, 600)  # Increased size for side-by-side view
        self.setStyleSheet(STYLESHEET)
        
        self.db_manager = db_manager
        self.edit_mode = user_name is not None
        self.initial_name = user_name
        self.captured_frame = None

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Content Area (Side by Side if editing)
        content_layout = QHBoxLayout()
        
        # 1. Current Photo (Only in Edit Mode)
        if self.edit_mode:
            current_layout = QVBoxLayout()
            lbl_current = QLabel("Foto Atual")
            lbl_current.setStyleSheet("font-weight: bold; font-size: 16px; margin-bottom: 5px;")
            current_layout.addWidget(lbl_current)
            
            self.current_img_label = QLabel("Carregando...")
            self.current_img_label.setAlignment(Qt.AlignCenter)
            self.current_img_label.setStyleSheet("background-color: black; border: 1px solid #454545;")
            self.current_img_label.setFixedSize(400, 300)
            self.load_current_image(user_name)
            current_layout.addWidget(self.current_img_label)
            
            content_layout.addLayout(current_layout)

        # 2. Camera Preview
        camera_layout = QVBoxLayout()
        lbl_cam = QLabel("Nova Foto (Câmera)")
        lbl_cam.setStyleSheet("font-weight: bold; font-size: 16px; margin-bottom: 5px;")
        camera_layout.addWidget(lbl_cam)
        
        self.video_label = QLabel("Iniciando Câmera...")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("background-color: black; border: 1px solid #454545;")
        self.video_label.setFixedSize(400, 300)
        camera_layout.addWidget(self.video_label)
        
        content_layout.addLayout(camera_layout)
        main_layout.addLayout(content_layout)

        # Form Controls
        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(0, 20, 0, 0)
        
        lbl_name = QLabel("Nome do Usuário:")
        lbl_name.setStyleSheet("font-weight: bold;")
        form_layout.addWidget(lbl_name)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Digite o nome...")
        self.name_input.setMinimumHeight(40)
        if self.initial_name:
            self.name_input.setText(self.initial_name)
            self.name_input.setReadOnly(True)
            self.name_input.setToolTip("Para renomear, exclua e crie novamente.")
        form_layout.addWidget(self.name_input)
        
        main_layout.addLayout(form_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 20, 0, 0)
        
        self.btn_capture = QPushButton("Salvar Alterações" if self.edit_mode else "Cadastrar")
        self.btn_capture.setMinimumHeight(45)
        self.btn_capture.setStyleSheet(f"background-color: {ACCENT_COLOR}; font-size: 14px;")
        self.btn_capture.clicked.connect(self.save_user)
        btn_layout.addWidget(self.btn_capture)

        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setMinimumHeight(45)
        btn_cancel.setStyleSheet("background-color: #6c757d; font-size: 14px;")
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)

        main_layout.addLayout(btn_layout)

        # Camera Setup
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def load_current_image(self, user):
        # Optimized to search for common extensions
        possible_exts = [".jpg", ".png", ".jpeg"]
        img_path = None
        user_dir = os.path.join(self.db_manager.db_path, user)
        
        if os.path.exists(user_dir):
            for ext in possible_exts:
                path = os.path.join(user_dir, f"{user}{ext}")
                if os.path.exists(path):
                    img_path = path
                    break
        
        if img_path:
            pixmap = QPixmap(img_path)
            if not pixmap.isNull():
                scaled = pixmap.scaled(self.current_img_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.current_img_label.setPixmap(scaled)
            else:
                self.current_img_label.setText("Erro ao carregar imagem")
        else:
             self.current_img_label.setText("Imagem não encontrada")

    def update_frame(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                self.captured_frame = frame.copy()
                
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qt_image)
                
                scaled_pixmap = pixmap.scaled(self.video_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.video_label.setPixmap(scaled_pixmap)

    def save_user(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Aviso", "O nome é obrigatório.")
            return
        
        if self.captured_frame is None:
            QMessageBox.warning(self, "Aviso", "Câmera não inicializada.")
            return

        # Confirmations
        if self.edit_mode:
             reply = QMessageBox.question(
                 self, "Confirmar Atualização", 
                 f"Tem certeza que deseja substituir a foto de '{name}' pela captura atual?",
                 QMessageBox.Yes | QMessageBox.No
             )
             if reply != QMessageBox.Yes: return

             self.db_manager.delete_user(name)
             success, msg = self.db_manager.create_user(name, self.captured_frame)
             
             if success:
                 QMessageBox.information(self, "Sucesso", "Foto atualizada com sucesso!")
                 self.accept()
             else:
                 QMessageBox.critical(self, "Erro", msg)
        else:
            reply = QMessageBox.question(
                 self, "Confirmar Cadastro", 
                 f"Tem certeza que deseja cadastrar o novo usuário '{name}'?",
                 QMessageBox.Yes | QMessageBox.No
             )
            if reply != QMessageBox.Yes: return

            success, msg = self.db_manager.create_user(name, self.captured_frame)
            if success:
                QMessageBox.information(self, "Sucesso", f"Usuário {name} cadastrado com sucesso!")
                self.accept()
            else:
                 QMessageBox.critical(self, "Erro", msg)

    def closeEvent(self, event):
        self.timer.stop()
        if self.cap:
            self.cap.release()
        if event: event.accept()
    
    def reject(self):
        self.closeEvent(None)
        super().reject()
    
    def accept(self):
        self.closeEvent(None)
        super().accept()


class UserActionWidget(QWidget):
    def __init__(self, user_name, edit_callback, delete_callback):
        super().__init__()
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10) # Added padding
        self.setLayout(layout)

        # Name
        self.name_label = QLabel(user_name)
        self.name_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self.name_label, stretch=1)

        # Buttons
        self.btn_edit = QPushButton("Editar Foto")
        self.btn_edit.setFixedSize(120, 35) # Increased size
        self.btn_edit.setStyleSheet(f"background-color: {ACCENT_COLOR}; font-size: 13px; border-radius: 4px;")
        self.btn_edit.clicked.connect(lambda: edit_callback(user_name))
        layout.addWidget(self.btn_edit)

        self.btn_delete = QPushButton("Excluir")
        self.btn_delete.setFixedSize(90, 35) # Increased size
        self.btn_delete.setStyleSheet(f"background-color: {DANGER_COLOR}; font-size: 13px; border-radius: 4px;")
        self.btn_delete.clicked.connect(lambda: delete_callback(user_name))
        layout.addWidget(self.btn_delete)


class ManagementWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciamento de Usuários")
        self.setGeometry(100, 100, 900, 700)
        self.setStyleSheet(STYLESHEET)
        
        self.db_manager = DatabaseManager()
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(30, 30, 30, 30)
        self.setLayout(main_layout)

        # Header
        header_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Pesquisar usuário por nome...")
        self.search_input.textChanged.connect(self.filter_users)
        self.search_input.setMinimumHeight(45)
        self.search_input.setStyleSheet("font-size: 14px; padding-left: 10px;")
        header_layout.addWidget(self.search_input)
        
        self.btn_add = QPushButton("+ Novo Usuário")
        self.btn_add.setMinimumHeight(45)
        self.btn_add.setStyleSheet(f"background-color: #198754; font-size: 14px; font-weight: bold; padding: 0 25px;")
        self.btn_add.clicked.connect(self.open_add_dialog)
        header_layout.addWidget(self.btn_add)
        
        main_layout.addLayout(header_layout)

        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("border: 1px solid #3e3e3e;")
        main_layout.addWidget(line)

        # List Title
        lbl_list = QLabel("Lista de Usuários")
        lbl_list.setStyleSheet("font-size: 18px; font-weight: bold; color: #858585; margin-top: 10px;")
        main_layout.addWidget(lbl_list)

        # User List
        self.user_list = QListWidget()
        self.user_list.setStyleSheet(f"background-color: {SIDEBAR_COLOR}; border-radius: 6px;")
        self.user_list.setSpacing(5) # Space between items
        main_layout.addWidget(self.user_list)

        self.load_users()

    def load_users(self, filter_text=""):
        self.user_list.clear()
        users = self.db_manager.get_users()
        
        for user in users:
            if filter_text.lower() in user.lower():
                item = QListWidgetItem(self.user_list)
                widget = UserActionWidget(user, self.open_edit_dialog, self.confirm_delete)
                
                # Dynamic Height Calculation or Fix
                item.setSizeHint(QSize(widget.sizeHint().width(), 65)) # Enforce height
                
                self.user_list.setItemWidget(item, widget)

    def filter_users(self, text):
        self.load_users(text)

    def open_add_dialog(self):
        dialog = UserFormDialog(self, self.db_manager)
        if dialog.exec_():
            self.load_users(self.search_input.text())

    def open_edit_dialog(self, user_name):
        dialog = UserFormDialog(self, self.db_manager, user_name)
        if dialog.exec_():
            self.load_users(self.search_input.text())

    def confirm_delete(self, user_name):
        confirm = QMessageBox.question(
            self, 
            "Confirmar Exclusão", 
            f"Tem certeza que deseja excluir permanentemente o usuário '{user_name}'?\nEsta ação não pode ser desfeita.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            success, msg = self.db_manager.delete_user(user_name)
            if success:
                QMessageBox.information(self, "Sucesso", "Usuário removido com sucesso.")
                self.load_users(self.search_input.text())
            else:
                QMessageBox.critical(self, "Erro", msg)

def run_management():
    app = QApplication(sys.argv)
    window = ManagementWindow()
    window.show()
    sys.exit(app.exec())
