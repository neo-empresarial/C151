
import cv2
import threading
from deepface import DeepFace
from src.common.database import DatabaseManager
from src.common.styles import STYLESHEET
from src.common.camera import CameraManager

class FlashOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: white;")
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setVisible(False)
        
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        
        self.anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim.setDuration(250)
        self.anim.setStartValue(0.8)
        self.anim.setEndValue(0.0)
        self.anim.setEasingCurve(QEasingCurve.OutQuad)
        self.anim.finished.connect(self.hide)

    def flash(self):
        self.resize(self.parent().size())
        self.setVisible(True)
        self.anim.start()

class EmbeddingWorker(QObject):
    finished = Signal(bool, str, object)

    def __init__(self, frame, model_name="Facenet"):
        super().__init__()
        self.frame = frame
        self.model_name = model_name

    def process(self):
        try:
            embedding_objs = DeepFace.represent(
                img_path=self.frame,
                model_name=self.model_name,
                detector_backend="opencv",
                enforce_detection=False,
                align=True
            )
            
            if not embedding_objs:
                self.finished.emit(False, "Nenhum rosto detectado para gerar embedding.", None)
                return

            embedding = embedding_objs[0]["embedding"]
            self.finished.emit(True, "Sucesso", embedding)
            
        except Exception as e:
            self.finished.emit(False, f"Erro na geração do embedding: {str(e)}", None)


class UserFormDialog(QDialog):
    def __init__(self, parent=None, db_manager=None, user_data=None):
        super().__init__(parent)
        self.user_data = user_data 
        self.edit_mode = user_data is not None
        
        self.setWindowTitle("Cadastrar Usuário" if not self.edit_mode else f"Editar: {user_data['name']}")
        self.setModal(True)
        self.resize(900, 650)
        self.setStyleSheet(STYLESHEET)
        
        self.db_manager = db_manager
        self.captured_frame = None
        self.camera_manager = None
        
        self.init_ui()
        
        if self.edit_mode:
            self.load_existing_image()
            self.btn_capture.setText("📷 Alterar Foto")
        else:
            QTimer.singleShot(100, self.start_camera)

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        body_layout = QHBoxLayout()
        
        cam_container = QWidget()
        cam_layout = QVBoxLayout(cam_container)
        cam_layout.setContentsMargins(0,0,0,0)
        
        lbl_cam = QLabel("Foto do Usuário")
        lbl_cam.setStyleSheet("font-weight: bold; font-size: 16px;")
        cam_layout.addWidget(lbl_cam)
        
        self.video_label = QLabel("Inicializando Câmera...")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("background-color: black; border: 1px solid #ccc; border-radius: 4px;")
        self.video_label.setFixedSize(480, 360)
        cam_layout.addWidget(self.video_label)
        
        self.flash_overlay = FlashOverlay(self.video_label)
        
        self.btn_capture = QPushButton("📸 Capturar Foto")
        self.btn_capture.setObjectName("primary")
        self.btn_capture.clicked.connect(self.toggle_capture)
        cam_layout.addWidget(self.btn_capture)
        
        self.lbl_status = QLabel("")
        self.lbl_status.setAlignment(Qt.AlignCenter)
        self.lbl_status.setStyleSheet("color: #107c10; font-weight: bold; font-size: 14px;")
        cam_layout.addWidget(self.lbl_status)
        
        body_layout.addWidget(cam_container)
        
        form_container = QWidget()
        form_layout = QVBoxLayout(form_container)
        form_layout.setAlignment(Qt.AlignTop)
        
        form_layout.addWidget(QLabel("ID do Usuário (Auto-gerado):"))
        self.id_input = QLineEdit()
        self.id_input.setReadOnly(True)
        self.id_input.setStyleSheet("background-color: #f3f3f3; color: #555;")
        if self.edit_mode:
            self.id_input.setText(self.user_data['id'])
        else:
            self.id_input.setText("Gerado ao Salvar")
        form_layout.addWidget(self.id_input)
        
        form_layout.addWidget(QLabel("Nome Completo:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ex: João Silva")
        if self.edit_mode:
            self.name_input.setText(self.user_data['name'])
            self.name_input.textChanged.connect(self.on_input_change)
        form_layout.addWidget(self.name_input)
        
        body_layout.addWidget(form_container)
        main_layout.addLayout(body_layout)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.btn_save = QPushButton("Salvar Registro")
        self.btn_save.setObjectName("primary")
        self.btn_save.setMinimumWidth(150)
        self.btn_save.clicked.connect(self.prepare_save)
        self.btn_save.setEnabled(False) 
        if self.edit_mode:
             self.btn_save.setText("Salvar Alterações")
             self.btn_save.setEnabled(False) 

        btn_layout.addWidget(self.btn_save)
        
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)
        
        main_layout.addLayout(btn_layout)

    def on_input_change(self):
        if self.edit_mode and self.name_input.text().strip() != self.user_data['name']:
            self.btn_save.setEnabled(True)

    def load_existing_image(self):
        if not self.edit_mode:
            return
            
        blob = self.db_manager.get_user_image(self.user_data['id'])
        if blob:
            import numpy as np
            nparr = np.frombuffer(blob, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is not None:
                rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qt_image)
                
                if self.video_label:
                    scaled = pixmap.scaled(self.video_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.video_label.setPixmap(scaled)

    def start_camera(self):
        if self.camera_manager:
            self.camera_manager.stop()
            self.camera_manager.deleteLater()
            self.camera_manager = None
        
        self.load_existing_image()
            
        self.camera_manager = CameraManager()
        self.camera_manager.frame_pixmap.connect(self.update_video_label)
        self.camera_manager.frame_captured.connect(self.update_captured_frame)
        
        self.camera_manager.error_occurred.connect(self.on_camera_error)
        self.camera_manager.start()

    def on_camera_error(self, err_msg):
        self.lbl_status.setText(f"Erro Câmera: {err_msg}")
        if not self.edit_mode:
            self.video_label.setText(err_msg)

    def stop_camera(self):
         if self.camera_manager:
            self.camera_manager.stop()

    def update_video_label(self, pixmap):
        if self.video_label:
            scaled = pixmap.scaled(self.video_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.video_label.setPixmap(scaled)

    def update_captured_frame(self, frame):
        self.current_live_frame = frame

    def toggle_capture(self):
        text = self.btn_capture.text()
        
        if "Alterar Foto" in text:
            self.start_camera()
            self.btn_capture.setText("📸 Capturar Foto")
            self.lbl_status.setText("")
            return

        if "Capturar" in text:
            if not hasattr(self, 'current_live_frame') or self.current_live_frame is None:
                return
            
            if self.camera_manager:
                self.camera_manager.frame_pixmap.disconnect(self.update_video_label)
                
            self.captured_frame = self.current_live_frame.copy()
            
            self.flash_overlay.flash()
            self.lbl_status.setText("✅ FOTO CAPTURADA")
            
            self.btn_capture.setText("🔄 Refazer Foto")
            self.btn_save.setEnabled(True)
            self.name_input.setFocus()
            
        else:
            if self.camera_manager:
                self.camera_manager.frame_pixmap.connect(self.update_video_label)
                
            self.captured_frame = None
            self.lbl_status.setText("")
            self.btn_capture.setText("📸 Capturar Foto")
            
            if self.edit_mode:
                if self.name_input.text().strip() == self.user_data['name']:
                    self.btn_save.setEnabled(False)
            else:
                self.btn_save.setEnabled(False)

    def prepare_save(self):
        name = self.name_input.text().strip()
        if not name:
             QMessageBox.warning(self, "Aviso", "Por favor, digite o nome do usuário.")
             return
        
        if self.edit_mode and self.captured_frame is None:
            success, msg = self.db_manager.update_user(self.user_data['id'], name, None, None)
            if success:
                QMessageBox.information(self, "Sucesso", msg)
                self.accept()
            else:
                QMessageBox.critical(self, "Erro", msg)
            return

        if self.captured_frame is None:
             QMessageBox.warning(self, "Aviso", "Por favor, capture uma foto.")
             return

        self.progress = QProgressDialog("Gerando assinatura facial...", None, 0, 0, self)
        self.progress.setWindowModality(Qt.WindowModal)
        self.progress.show()

        self.worker = EmbeddingWorker(self.captured_frame)
        self.worker_thread = threading.Thread(target=self.worker.process)
        self.worker.finished.connect(self.finish_save)
        self.worker_thread.start()

    def finish_save(self, success, msg, embedding):
        self.progress.close()
        
        if not success:
            QMessageBox.critical(self, "Erro", msg)
            return

        name = self.name_input.text().strip()
        
        if self.edit_mode:
             success_db, msg_db = self.db_manager.update_user(self.user_data['id'], name, self.captured_frame, embedding)
        else:
             success_db, msg_db = self.db_manager.create_user(name, self.captured_frame, embedding)
        
        if success_db:
            QMessageBox.information(self, "Sucesso", msg_db)
            self.accept()
        else:
            QMessageBox.critical(self, "Erro", msg_db)

    def closeEvent(self, event):
        self.stop_camera()
        super().closeEvent(event)


class ManagementWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciamento de Usuários")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet(STYLESHEET)
        
        self.db_manager = DatabaseManager()
        
        self.init_ui()
        self.load_users()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(layout)
        
        header = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Pesquisar...")
        self.search_input.textChanged.connect(self.load_users)
        header.addWidget(self.search_input)
        
        btn_add = QPushButton("+ Novo Usuário")
        btn_add.setObjectName("primary")
        btn_add.clicked.connect(self.open_add_dialog)
        header.addWidget(btn_add)
        
        layout.addLayout(header)
        
        self.list_widget = QListWidget()
        self.list_widget.setVerticalScrollMode(QListWidget.ScrollPerPixel)
        layout.addWidget(self.list_widget)
        
        layout.addWidget(QLabel("Dica: Use os botões para editar ou excluir."))

    def load_users(self):
        filter_text = self.search_input.text().lower()
        self.list_widget.clear()
        
        users = self.db_manager.get_users()
        for user in users:
            if filter_text and filter_text not in user['name'].lower():
                continue
                
            item = QListWidgetItem()
            widget = self.create_user_widget(user)
            
            item.setSizeHint(QSize(widget.sizeHint().width(), 80))
            
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, widget)

    def create_user_widget(self, user):
        w = QWidget()
        l = QHBoxLayout()
        l.setContentsMargins(10, 10, 10, 10)
        
        info_l = QVBoxLayout()
        name_lbl = QLabel(user['name'])
        name_lbl.setStyleSheet("font-size: 16px; font-weight: 600;")
        id_lbl = QLabel(f"ID: {user['id']}")
        id_lbl.setStyleSheet("color: #666; font-size: 12px;")
        info_l.addWidget(name_lbl)
        info_l.addWidget(id_lbl)
        l.addLayout(info_l)
        
        l.addStretch()
        
        btn_edit = QPushButton("Editar Foto")
        btn_edit.clicked.connect(lambda: self.open_edit_dialog(user))
        l.addWidget(btn_edit)
        
        btn_del = QPushButton("Excluir")
        btn_del.setObjectName("danger")
        btn_del.clicked.connect(lambda: self.delete_user(user))
        l.addWidget(btn_del)
        
        w.setLayout(l)
        return w

    def open_add_dialog(self):
        dlg = UserFormDialog(self, self.db_manager)
        if dlg.exec_():
            self.load_users()

    def open_edit_dialog(self, user):
        dlg = UserFormDialog(self, self.db_manager, user)
        if dlg.exec_():
            self.load_users()

    def delete_user(self, user):
        reply = QMessageBox.question(self, "Confirmar Exclusão", 
                                     f"Tem certeza que deseja apagar {user['name']}?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.db_manager.delete_user(user['name'])
            self.load_users()
