import sys
import os
import pickle
import cv2
import sqlite3
import numpy as np
from deepface import DeepFace

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.common.database import DatabaseManager
from src.common.config import MODEL_NAME, DETECTOR_BACKEND

def migrate():
    print(f"Starting migration to {MODEL_NAME} + {DETECTOR_BACKEND}...")
    db = DatabaseManager()
    users = db.get_all_embeddings() 
    
    conn = db.init_db() 
    
    conn = sqlite3.connect(db.sqlite_file)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, image_blob FROM users")
    rows = cursor.fetchall()
    
    success_count = 0
    fail_count = 0
    
    for row in rows:
        user_id, name, image_blob = row
        print(f"Processing user: {name} ({user_id})...")
        
        if not image_blob:
            print(f"  [SKIPPING] No image found for {name}. Cannot regenerate embedding.")
            fail_count += 1
            continue
            
        try:
            nparr = np.frombuffer(image_blob, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if frame is None:
                print("  [ERROR] Failed to decode image.")
                fail_count += 1
                continue

            embedding_objs = DeepFace.represent(
                img_path=frame,
                model_name=MODEL_NAME,
                detector_backend=DETECTOR_BACKEND,
                enforce_detection=True,
                align=True
            )
            
            if not embedding_objs:
                print("  [ERROR] No face detected during migration.")
                fail_count += 1
                continue
                
            embedding = embedding_objs[0]["embedding"]
            
            embedding_blob = pickle.dumps(embedding)
            cursor.execute("UPDATE users SET embedding = ? WHERE id = ?", (embedding_blob, user_id))
            conn.commit()
            
            print(f"  [SUCCESS] Updated embedding for {name}.")
            success_count += 1
            
        except Exception as e:
            print(f"  [ERROR] Failed to process {name}: {e}")
            fail_count += 1
            
    conn.close()
    print("-" * 30)
    print(f"Migration Complete.\nSuccess: {success_count}\nFailed: {fail_count}")

if __name__ == "__main__":
    migrate()
