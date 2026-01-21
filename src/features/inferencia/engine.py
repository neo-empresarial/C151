import cv2
import threading
import time
import numpy as np
import faiss
import logging
from deepface import DeepFace
from src.common.config import MODEL_NAME, DETECTOR_BACKEND, VERIFICATION_THRESHOLD
from src.features.inferencia.liveness.detector import LivenessDetector

class InferenceEngine:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.model_name = MODEL_NAME
        self.detector_backend = DETECTOR_BACKEND
        self.threshold = VERIFICATION_THRESHOLD
        self.running = False
        self._paused = True
        self.last_recognition_time = 0
        self.last_result_time = 0
        self.thread = None
        self.lock = threading.Lock()
        self.df_lock = threading.Lock()
        self.latest_frame = None
        self.latest_results = []
        self.known_embeddings = []
        self.known_ids = []
        self.faiss_index = None
        self.is_loaded = False
        self.liveness_detector = LivenessDetector()

    @property
    def paused(self):
        return self._paused

    @paused.setter
    def paused(self, value):
        if self._paused != value:
            logging.info(f"Engine paused state changed: {self._paused} -> {value}")
            self._paused = value

    def load_model(self):
        try:
            with self.df_lock:
                DeepFace.build_model(self.model_name)
                all_embeddings_data = self.db_manager.get_all_embeddings()
                
                self.known_embeddings = []
                self.known_ids = []
                
                if all_embeddings_data:
                    embeddings = [data["embedding"] for data in all_embeddings_data]
                    self.known_ids = [data for data in all_embeddings_data]
                    params = np.array(embeddings).astype('float32')
                    faiss.normalize_L2(params)
                    dimension = params.shape[1]
                    self.faiss_index = faiss.IndexFlatIP(dimension)
                    self.faiss_index.add(params)
                
                if self.faiss_index:
                    logging.debug(f"Index rebuilt with {self.faiss_index.ntotal} vectors/photos.")
                self.is_loaded = True
        except Exception as e:
            logging.error(f"Failed to load model/index: {e}")
            import traceback
            logging.error(traceback.format_exc())

    def generate_embedding(self, frame):
        logging.debug("generate_embedding called. Requesting df_lock...")
        with self.df_lock:
            logging.debug("df_lock acquired. Starting DeepFace.represent...")
            start_time = time.time()
            try:
                result = DeepFace.represent(
                    img_path=frame,
                    model_name=self.model_name,
                    detector_backend=self.detector_backend,
                    enforce_detection=True,
                    align=True,
                    anti_spoofing=False
                )
                logging.debug(f"DeepFace.represent finished in {time.time() - start_time:.2f}s")
                return result
            except Exception as e:
                logging.error(f"DeepFace.represent failed: {e}")
                raise e
            finally:
                logging.debug("Releasing df_lock.")

    def verify_enrollment_face(self, frame):
        logging.debug("verify_enrollment_face called.")
        try:
             results = self.generate_embedding(frame)
             
        except Exception as e:
            return {'success': False, 'message': 'Nenhum rosto detectado ou erro na detecção.', 'embedding': None, 'matched_user': None}

        if not results:
             return {'success': False, 'message': 'Nenhum rosto detectado.', 'embedding': None, 'matched_user': None}
        
        try:
            face_data = results[0]
            embedding = face_data['embedding']
            facial_area = face_data.get('facial_area')
            is_real = True
            liveness_score = 0.0

            if facial_area:
                x = facial_area['x']
                y = facial_area['y']
                w = facial_area['w']
                h = facial_area['h']
                
                scale = 2.7
                center_x = x + w / 2
                center_y = y + h / 2
                h_new = int(h * scale)
                w_new = int(w * scale)
                
                h_orig, w_orig = frame.shape[:2]
                
                x1 = int(center_x - w_new / 2)
                y1 = int(center_y - h_new / 2)
                x2 = x1 + w_new
                y2 = y1 + h_new
                
                x1 = max(0, x1)
                y1 = max(0, y1)
                x2 = min(w_orig, x2)
                y2 = min(h_orig, y2)
                
                if x2 > x1 and y2 > y1:
                    face_crop = frame[y1:y2, x1:x2]
                    is_real, liveness_score = self.liveness_detector.check_liveness(face_crop)
                    logging.info(f"Enrollment Liveness: {is_real} ({liveness_score:.4f})")
                
            if not is_real:
                return {
                    'success': False,
                    'message': f'Rosto identificado como FALSO (Spoofing). Score: {liveness_score:.4f}',
                    'embedding': None,
                    'matched_user': None
                }

            matched_user = None
            if self.faiss_index and self.faiss_index.ntotal > 0:
                query = np.array([embedding]).astype('float32')
                faiss.normalize_L2(query)
                
                D, I = self.faiss_index.search(query, 1)
                score = D[0][0]
                
                if score > (1 - self.threshold):
                    idx = I[0][0]
                    if idx < len(self.known_ids):
                        matched_user = self.known_ids[idx]
                        logging.info(f"Enrollment Match Found: {matched_user.get('name')} score={score}")

            return {
                'success': True,
                'message': 'OK',
                'embedding': embedding,
                'matched_user': matched_user
            }
        except Exception as e:
            logging.error(f"Error in verification logic: {e}")
            return {'success': False, 'message': f'Erro interno verificação: {str(e)}', 'embedding': None, 'matched_user': None}

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._process_loop, daemon=True)
        self.thread.start()

    def stop(self):
        logging.info("Stopping InferenceEngine...")
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2.0)
        logging.info("InferenceEngine stopped.")


    def update_frame(self, frame):
        with self.lock:
            self.latest_frame = frame.copy()

    def get_results(self):
        with self.lock:
            if (time.time() - self.last_result_time) > 5.0:
                return []
            return self.latest_results

    def _process_loop(self):
        self.load_model()

        while self.running:
            if self._paused:
                time.sleep(0.1)
                continue

            frame = None
            with self.lock:
                if self.latest_frame is not None:
                    frame = self.latest_frame.copy()
                    self.latest_frame = None
            
            if frame is None:
                time.sleep(0.01)
                continue

            try:
                
                face_objs = []
                try:
                     with self.df_lock:
                        current_index = self.faiss_index
                        current_known_ids = self.known_ids
                        h_orig, w_orig = frame.shape[:2]
                        target_w = 320 
                        scale_factor = 1.0
                        process_frame = frame
                        if w_orig > target_w:
                            scale_factor = target_w / w_orig
                            new_h = int(h_orig * scale_factor)
                            process_frame = cv2.resize(frame, (target_w, new_h))
                        
                        face_objs = DeepFace.represent(
                            img_path=process_frame,
                            model_name=self.model_name,
                            detector_backend=self.detector_backend,
                            enforce_detection=True,
                            align=True,
                            anti_spoofing=False
                        )
                        self.last_recognition_time = time.time()
                except Exception:
                    pass 

                results = []
                for face in face_objs:
                    target_embedding = face["embedding"]
                    area = face["facial_area"]
                    x = int(area["x"] / scale_factor)
                    y = int(area["y"] / scale_factor)
                    w = int(area["w"] / scale_factor)
                    h = int(area["h"] / scale_factor)
                    
                    found_match = False
                    best_name = "Desconhecido"
                    best_id = None
                    best_access = "Visitante"
                    confidence = 0.0
                    is_real = True 
                    liveness_score = 0.0
                    
                    if current_index and current_index.ntotal > 0:
                        query = np.array([target_embedding]).astype('float32')
                        faiss.normalize_L2(query)
                        
                        D, I = current_index.search(query, 1)
                        score = D[0][0] 
                        
                        if score > (1 - self.threshold):
                            scale = 2.7
                            center_x = x + w / 2
                            center_y = y + h / 2
                            h_new = int(h * scale)
                            w_new = int(w * scale)
                            
                            x1 = int(center_x - w_new / 2)
                            y1 = int(center_y - h_new / 2)
                            x2 = x1 + w_new
                            y2 = y1 + h_new
                            
                            x1 = max(0, x1)
                            y1 = max(0, y1)
                            x2 = min(w_orig, x2)
                            y2 = min(h_orig, y2)
                            
                            if (x2 > x1) and (y2 > y1):
                                face_crop = frame[y1:y2, x1:x2]
                                is_real, liveness_score = self.liveness_detector.check_liveness(face_crop)
                                logging.debug(f"Matches user. Liveness Check: {is_real} ({liveness_score:.4f})")
                            
                            if is_real:
                                idx = I[0][0]
                                if idx < len(current_known_ids):
                                    user_data = current_known_ids[idx]
                                    best_name = user_data["name"]
                                    best_id = user_data["id"]
                                    best_access = user_data.get("access_level", "Visitante")
                                    found_match = True
                                    confidence = float(score)
                                    logging.info(f"MATCH FOUND! User: {best_name}, Confidence: {confidence:.4f}")
                            else:
                                best_name = "Fake/Spoof"
                                best_access = "Negado"
                                logging.warning(f"Spoof detected for potential match! Score: {liveness_score:.4f}")
                        
                        else:
                            logging.debug(f"No match (score {score:.4f}). Skipping liveness.")
                    
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
                        "confidence": confidence,
                        "in_roi": in_roi,
                        "is_real": is_real,
                        "liveness_score": liveness_score,
                        "result_timestamp": time.time()
                    })
                
                with self.lock:
                    self.latest_results = results
                    self.last_result_time = time.time()

            except Exception as e:
                import traceback
                logging.error(f"Engine Loop Error: {e} - {traceback.format_exc()}")
            
            time.sleep(0.001)
