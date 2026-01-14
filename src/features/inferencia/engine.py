
import threading
import time
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
        self.df_lock = threading.Lock()
        
        self.latest_frame = None
        self.latest_results = []
        
        self.known_embeddings = []
        self.is_loaded = False

    def load_model(self):
        print("Carregando modelos do DeepFace e Embeddings...")
        try:
            with self.df_lock:
                 DeepFace.build_model(self.model_name)
                 
                 self.known_embeddings = self.db_manager.get_all_embeddings()
                 print(f"Carregado {len(self.known_embeddings)} usuários conhecidos.")
                 self.is_loaded = True
             
        except Exception as e:
            print(f"Error loading model: {e}")

    def generate_embedding(self, frame):
        with self.df_lock:
            return DeepFace.represent(
                img_path=frame,
                model_name=self.model_name,
                detector_backend=self.detector_backend,
                enforce_detection=True
            )

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
        # Initial load (safe to call, uses lock)
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
                face_objs = []
                try:
                    with self.df_lock:
                        face_objs = DeepFace.represent(
                            img_path=frame,
                            model_name=self.model_name,
                            detector_backend=self.detector_backend,
                            enforce_detection=True,
                            align=True
                        )
                except Exception as e:
                    # Silent or debug log for "Face not found" etc?
                    # Face not found raises exception usually with enforce_detection=True
                    # But we can print it if it is something else.
                    # Commonly "Face could not be detected"
                    # print(f"DEBUG: Represent Error: {e}")
                    pass

                results = []
                
                for face in face_objs:
                    target_embedding = face["embedding"]
                    area = face["facial_area"]
                    x, y, w, h = area["x"], area["y"], area["w"], area["h"]
                    
                    found_match = False
                    best_score = 0.40 
                    best_name = "Desconhecido"
                    best_id = None
                    best_access = "Visitante"
                    
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
                         # print("DEBUG: New Face Detected (Unknown)")
                         pass
                    
                    h_frame, w_frame, _ = frame.shape
                    cx_frame, cy_frame = w_frame // 2, h_frame // 2
                    
                    cx_face = x + w // 2
                    cy_face = y + h // 2
                    
                    roi_threshold_x = w_frame * 0.15
                    roi_threshold_y = h_frame * 0.20 
                    
                    in_roi = (abs(cx_face - cx_frame) < roi_threshold_x) and (abs(cy_face - cy_frame) < roi_threshold_y)
                    
                    results.append({
                        "box": (x, y, w, h),
                        "name": best_name if found_match else "Desconhecido",
                        "id": best_id,
                        "access_level": best_access,
                        "known": found_match,
                        "confidence": (1 - best_score),
                        "in_roi": in_roi
                    })
                
                with self.lock:
                    self.latest_results = results

            except Exception as e:
                print(f"Engine Loop Error: {e}")
            
            time.sleep(0.05)
