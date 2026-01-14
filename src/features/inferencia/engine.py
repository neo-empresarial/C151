
import threading
import time
import os
import cv2
import datetime
import numpy as np
from deepface import DeepFace
from scipy.spatial.distance import cosine
from PySide6.QtCore import QObject, Signal, QThread

class RecognitionWorker(QObject):
    finished = Signal()
    results_ready = Signal(object, list)
    model_loaded = Signal()
    
    def __init__(self, db_manager, model_name="Facenet", detector_backend="opencv"):
        super().__init__()
        self.db_manager = db_manager
        self.model_name = model_name
        self.detector_backend = detector_backend
        self.running = False
        self.lock = threading.Lock()
        self.latest_frame = None
        
        # Cache for embeddings
        self.known_embeddings = []

    def load_model(self):
        print("Carregando modelos do DeepFace e Embeddings...")
        try:
             # Ensure model is built/downloaded
             DeepFace.build_model(self.model_name)
             
             # Load embeddings from SQLite
             self.known_embeddings = self.db_manager.get_all_embeddings()
             print(f"Carregado {len(self.known_embeddings)} usuários conhecidos.")
             
        except Exception as e:
            print(f"Error loading model: {e}")
        
        self.model_loaded.emit()

    def update_frame(self, frame):
        with self.lock:
            self.latest_frame = frame.copy()

    def process(self):
        self.running = True
        self.load_model()

        while self.running:
            frame = None
            with self.lock:
                if self.latest_frame is not None:
                    frame = self.latest_frame.copy()
            
            if frame is None:
                time.sleep(0.05)
                continue

            try:
                # 1. Detect and Represent Faces
                # DeepFace.represent returns list of dicts: [{embedding, facial_area: {x,y,w,h}}]
                # We handle multiple faces
                
                # Note: enforce_detection=False allows returning something even if detection fails slightly,
                # but usually returns empty list or raises error if really no face.
                # We use try-except to handle no face.
                
                face_objs = []
                try:
                    face_objs = DeepFace.represent(
                        img_path=frame,
                        model_name=self.model_name,
                        detector_backend=self.detector_backend,
                        enforce_detection=True,
                        align=True
                    )
                except:
                    # No face detected
                    pass

                results = []
                
                for face in face_objs:
                    target_embedding = face["embedding"]
                    area = face["facial_area"]
                    x, y, w, h = area["x"], area["y"], area["w"], area["h"]
                    
                    found_match = False
                    best_score = 0.40 # Cosine distance threshold (lower is better). Facenet usually 0.40
                    best_name = "Desconhecido"
                    best_id = None
                    
                    # 2. Compare against known embeddings
                    for known in self.known_embeddings:
                        known_emb = known["embedding"]
                        score = cosine(target_embedding, known_emb)
                        
                        if score < best_score:
                            best_score = score
                            best_name = known["name"]
                            best_id = known["id"]
                            found_match = True
                    
                    results.append({
                        "box": (x, y, w, h),
                        "name": best_name if found_match else "Desconhecido",
                        "id": best_id,
                        "known": found_match,
                        "confidence": (1 - best_score) # Pseudo confidence
                    })

                self.results_ready.emit(frame, results)

            except Exception as e:
                # print(f"Inference error: {e}")
                pass
            
            time.sleep(0.05)
        
        self.finished.emit()

    def stop(self):
        self.running = False

class InferenceController(QObject):
    def __init__(self, db_manager):
        super().__init__()
        self.worker = RecognitionWorker(db_manager)
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        
        self.thread.started.connect(self.worker.process)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

    def start(self):
        self.thread.start()

    def stop(self):
        self.worker.stop()
        self.thread.quit()
        self.thread.wait()

    def update_frame(self, frame):
        self.worker.update_frame(frame)
