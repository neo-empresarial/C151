
import cv2
import threading
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QLineEdit, QDialog, QMessageBox, QProgressDialog, QListWidget, 
                             QListWidgetItem, QComboBox, QGraphicsOpacityEffect)
from PyQt5.QtCore import Qt, QTimer, QSize, QPropertyAnimation, QEasingCurve, QObject, pyqtSignal as Signal
from PyQt5.QtGui import QImage, QPixmap
from deepface import DeepFace
from src.common.database import DatabaseManager
from src.common.styles import STYLESHEET
from src.common.camera import CameraManager
from src.common.config import db_config
from src.common.logger import AppLogger
import numpy as np

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
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(500, 680)
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                border: 1px solid #333;
                border-radius: 12px;
            }
            QLabel { color: #e0e0e0; font-family: 'Segoe UI', sans-serif; }
            QLineEdit, QComboBox {
                background-color: #2d2d2d;
                border: 1px solid #3e3e3e;
                border-radius: 6px;
                padding: 8px;
                color: #fff;
                font-size: 14px;
            }
            QLineEdit:focus, QComboBox:focus { border: 1px solid #0078d4; }
            QPushButton {
                background-color: #333;
                border: 1px solid #444;
                border-radius: 6px;
                color: #fff;
                padding: 8px 16px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #444; }
            QPushButton#primary {
                background-color: #0078d4;
                border: 1px solid #0078d4;
            }
            QPushButton#primary:hover { background-color: #106ebe; }
            QPushButton#danger {
                background-color: #d83b01;
                border: 1px solid #d83b01;
            }
            QPushButton#danger:hover { background-color: #ea4a1f; }
            QPushButton#close {
                background-color: transparent;
                border: none;
                color: #888;
                font-size: 16px;
            }
            QPushButton#close:hover { color: #fff; background-color: #c42b1c; border-radius: 0 12px 0 0; }
        """)
        
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
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("background-color: #252525; border-top-left-radius: 12px; border-top-right-radius: 12px; border-bottom: 1px solid #333;")
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 0, 0, 0)
        
        title_lbl = QLabel("Cadastrar Usuário" if not self.edit_mode else f"Editar: {self.user_data['name']}")
        title_lbl.setStyleSheet("font-size: 14px; font-weight: bold; border: none;")
        
        btn_close = QPushButton("✕")
        btn_close.setObjectName("close")
        btn_close.setFixedSize(40, 40)
        btn_close.clicked.connect(self.reject)
        
        title_layout.addWidget(title_lbl)
        title_layout.addStretch()
        title_layout.addWidget(btn_close)
        
        main_layout.addWidget(title_bar)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)
        
        cam_container = QWidget()
        cam_container.setFixedHeight(300)
        cam_container.setStyleSheet("background-color: #000; border-radius: 8px; border: 1px solid #333;")
        cam_layout = QVBoxLayout(cam_container)
        cam_layout.setContentsMargins(0,0,0,0)
        
        self.video_label = QLabel("Inicializando...")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("color: #666; font-size: 12px; border: none;")
        cam_layout.addWidget(self.video_label)
        
        self.flash_overlay = FlashOverlay(self.video_label)
        content_layout.addWidget(cam_container)
        
        cam_controls = QHBoxLayout()
        self.btn_capture = QPushButton("📸 Capturar Foto")
        self.btn_capture.setObjectName("primary")
        self.btn_capture.setCursor(Qt.PointingHandCursor)
        self.btn_capture.clicked.connect(self.toggle_capture)
        cam_controls.addWidget(self.btn_capture)
        content_layout.addLayout(cam_controls)
        
        self.lbl_status = QLabel("")
        self.lbl_status.setAlignment(Qt.AlignCenter)
        self.lbl_status.setStyleSheet("color: #107c10; font-weight: bold; font-size: 12px; margin-top: 5px;")
        content_layout.addWidget(self.lbl_status)

        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nome Completo")
        if self.edit_mode:
            self.name_input.setText(self.user_data['name'])
            self.name_input.textChanged.connect(self.on_input_change)
            
        self.access_input = QComboBox()
        self.access_input.addItems(db_config.config.get('access_levels', ["Visitante"]))
        if self.edit_mode:
            self.access_input.setCurrentText(self.user_data.get('access_level', 'Visitante'))

        form_layout.addWidget(QLabel("Nome do Usuário"))
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(QLabel("Nível de Acesso"))
        form_layout.addWidget(self.access_input)
        
        content_layout.addLayout(form_layout)
        content_layout.addStretch()

        # Action Buttons
        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("Salvar Registro")
        self.btn_save.setObjectName("primary")
        self.btn_save.setFixedHeight(36)
        self.btn_save.setCursor(Qt.PointingHandCursor)
        self.btn_save.clicked.connect(self.prepare_save)
        self.btn_save.setEnabled(False) 
        if self.edit_mode:
             self.btn_save.setText("Salvar Alterações")
             self.btn_save.setEnabled(False) 

        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setFixedHeight(36)
        btn_cancel.setCursor(Qt.PointingHandCursor)
        btn_cancel.clicked.connect(self.reject)
        
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(self.btn_save)
        
        content_layout.addLayout(btn_layout)
        main_layout.addWidget(content)
        
        self.dragging = False
        self.offset = None
        title_bar.mousePressEvent = self.mousePressEvent
        title_bar.mouseMoveEvent = self.mouseMoveEvent
        title_bar.mouseReleaseEvent = self.mouseReleaseEvent

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.dragging = False

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
        self.lbl_status.setStyleSheet("color: #ff5252; font-weight: bold;")
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
            self.lbl_status.setStyleSheet("color: #107c10; font-weight: bold; font-size: 12px; margin-top: 5px;")
            
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
        
        AppLogger.log(f"DEBUG: finish_save called. Edit Mode: {self.edit_mode}")
        AppLogger.log(f"DEBUG: Current Config: {db_config.config}")
        check_sim_val = db_config.config.get('face_tech', {}).get('check_similarity', False)
        AppLogger.log(f"DEBUG: check_similarity value: {check_sim_val}")
        
        if self.edit_mode:
            db_config._config = db_config.load_config()
            AppLogger.log(f"DEBUG: Config reloaded from disk: {db_config.config}")

            check_similarity = db_config.config.get('face_tech', {}).get('check_similarity', False)
            
            if check_similarity and self.captured_frame is not None:
                AppLogger.log(f"DEBUG: Checking similarity for User ID: {self.user_data['id']}")
                try:
                    existing_embeddings = self.db_manager.get_user_embeddings(self.user_data['id'])
                    if existing_embeddings:
                        AppLogger.log(f"DEBUG: Found {len(existing_embeddings)} existing embeddings for user.")
                        new_emb = np.array(embedding)
                        min_distance = float('inf')
                        
                        for old_emb in existing_embeddings:
                            old_emb_np = np.array(old_emb)
                            
                            dot_product = np.dot(new_emb, old_emb_np)
                            norm_new = np.linalg.norm(new_emb)
                            norm_old = np.linalg.norm(old_emb_np)
                            
                            cosine_similarity = dot_product / (norm_new * norm_old)
                            distance = 1.0 - cosine_similarity
                            
                            if distance < min_distance:
                                min_distance = distance
                        
                        threshold = db_config.config.get('face_tech', {}).get('threshold', 0.28)
                        AppLogger.log(f"DEBUG: Similarity Result - Min Dist: {min_distance:.4f}, Threshold: {threshold}")
                        
                        if min_distance > threshold:
                            AppLogger.log(f"DEBUG: Similarity Check Failed.")
                            QMessageBox.critical(self, "Bloqueio de Segurança", 
                                                f"A foto não corresponde ao usuário atual.\n\n"
                                                f"Diferença detectada: {min_distance:.3f}\n"
                                                f"Limite máximo: {threshold}\n\n"
                                                "Certifique-se de que é a mesma pessoa.")
                            return
                        else:
                             AppLogger.log(f"DEBUG: Similarity Check Passed.")
                    else:
                        AppLogger.log(f"DEBUG: No existing embeddings found. Allowing update (First photo).")

                except Exception as e:
                    AppLogger.log(f"Error in similarity check: {e}")



            success_db, msg_db = self.db_manager.update_user(
                user_id=self.user_data['id'], 
                name=name, 
                access_level=self.access_input.currentText()
            )
            # Update photo if new frame captured
            if self.captured_frame is not None:
                self.db_manager.add_user_photo(self.user_data['id'], self.captured_frame, embedding)

        else:
            success_db, msg_db = self.db_manager.create_user(
                 name=name, 
                 access_level=self.access_input.currentText(),
                 frame=self.captured_frame, 
                 embedding=embedding
             )
        
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
