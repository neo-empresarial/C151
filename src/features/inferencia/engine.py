
import threading
import time
import os
import cv2
import datetime
import numpy as np
from deepface import DeepFace
from scipy.spatial.distance import cosine

class InferenceEngine:
    def __init__(self, db_manager, model_name="Facenet", detector_backend="opencv"):
        self.db_manager = db_manager
        self.model_name = model_name
        self.detector_backend = detector_backend
        self.running = False
        self.thread = None
        self.lock = threading.Lock()
        
        self.latest_frame = None
        self.latest_results = []
        
        self.known_embeddings = []
        self.is_loaded = False

    def load_model(self):
        print("Carregando modelos do DeepFace e Embeddings...")
        try:
             # Ensure model is built/downloaded
             DeepFace.build_model(self.model_name)
             
             # Load embeddings from SQLite
             self.known_embeddings = self.db_manager.get_all_embeddings()
             print(f"Carregado {len(self.known_embeddings)} usuários conhecidos.")
             self.is_loaded = True
             
        except Exception as e:
            print(f"Error loading model: {e}")

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._process_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)

    def update_frame(self, frame):
        with self.lock:
            self.latest_frame = frame.copy()

    def get_results(self):
        with self.lock:
            return self.latest_results

    def _process_loop(self):
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
                face_objs = []
                try:
                    face_objs = DeepFace.represent(
                        img_path=frame,
                        model_name=self.model_name,
                        detector_backend=self.detector_backend, # opencv is fast
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
                    best_score = 0.40 # Cosine distance threshold
                    best_name = "Desconhecido"
                    best_id = None
                    best_access = "Visitante"
                    
                    # 2. Compare against known embeddings
                    for known in self.known_embeddings:
                        known_emb = known["embedding"]
                        score = cosine(target_embedding, known_emb)
                        
                        if score < best_score:
                            best_score = score
                            best_name = known["name"]
                            best_id = known["id"]
                            best_access = known.get("access_level", "Visitante")
                            found_match = True
                            print(f"DEBUG: RECOGNIZED USER -> {best_name}")
                    
                    if not found_match:
                         print("DEBUG: New Face Detected (Unknown)")
                    
                    results.append({
                        "box": (x, y, w, h),
                        "name": best_name if found_match else "Desconhecido",
                        "id": best_id,
                        "access_level": best_access,
                        "known": found_match,
                        "confidence": (1 - best_score) 
                    })
                
                with self.lock:
                    self.latest_results = results

            except Exception as e:
                # print(f"Inference error: {e}")
                pass
            
            time.sleep(0.05)
