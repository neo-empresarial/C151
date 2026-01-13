import threading
import time
import os
import csv
import datetime
from deepface import DeepFace
import cv2

class RecognitionEngine:
    def __init__(self, db_path="database", model_name="Facenet"):
        self.db_path = db_path
        self.model_name = model_name
        self.running = True
        self.latest_frame = None
        self.results = []
        self.lock = threading.Lock()
        
        self.log_dir = "Logs"
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file = os.path.join(self.log_dir, "history.csv")
        self.last_logged = {}
        self.log_cooldown = 60
        
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Name"])

    def start(self):
        threading.Thread(target=self._loop, daemon=True).start()

    def stop(self):
        self.running = False

    def update_frame(self, frame):
        with self.lock:
            self.latest_frame = frame.copy()

    def get_results(self):
        return self.results

    def _log_recognition(self, name):
        now = time.time()
        if name in self.last_logged:
            if now - self.last_logged[name] < self.log_cooldown:
                return

        try:
            timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.log_file, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([timestamp_str, name])
            self.last_logged[name] = now
            print(f"Logged: {name}")
        except Exception as e:
            print(f"Log Error: {e}")

    def _loop(self):
        print("Model loading...")
        while self.running:
            frame = None
            with self.lock:
                if self.latest_frame is not None:
                    frame = self.latest_frame.copy()
            
            if frame is None:
                time.sleep(0.1)
                continue

            try:
                dfs = DeepFace.find(
                    img_path=frame,
                    db_path=self.db_path,
                    model_name=self.model_name,
                    detector_backend="opencv",
                    enforce_detection=False,
                    silent=True
                )

                new_results = []
                found_match = False

                for df in dfs:
                    if not df.empty:
                        best_match = df.iloc[0]
                        identity = best_match["identity"]
                        name = os.path.basename(os.path.dirname(identity))
                        
                        x = int(best_match.get("source_x", 0))
                        y = int(best_match.get("source_y", 0))
                        w = int(best_match.get("source_w", 0))
                        h = int(best_match.get("source_h", 0))

                        if w > 0:
                            new_results.append({
                                "box": (x, y, w, h),
                                "name": name,
                                "known": True
                            })
                            self._log_recognition(name)
                            found_match = True

                if not found_match:
                    try:
                        faces = DeepFace.extract_faces(
                            img_path=frame,
                            detector_backend="opencv",
                            enforce_detection=False,
                            align=False
                        )
                        for face in faces:
                             if face.get("confidence", 0) > 0.5:
                                area = face["facial_area"]
                                x, y, w, h = area["x"], area["y"], area["w"], area["h"]
                                
                                cx, cy = x + w/2, y + h/2
                                is_known_overlap = False
                                for res in new_results:
                                    rx, ry, rw, rh = res["box"]
                                    if rx < cx < rx+rw and ry < cy < ry+rh:
                                        is_known_overlap = True
                                        break
                                
                                if not is_known_overlap:
                                    new_results.append({
                                        "box": (x, y, w, h),
                                        "name": "Desconhecido",
                                        "known": False
                                    })
                    except:
                        pass

                self.results = new_results

            except Exception as e:
                pass

            time.sleep(0.05)
