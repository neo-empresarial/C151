from src.common.config import CAMERA_INDEX
from src.common.database import DatabaseManager
from src.common.camera import CameraManager
from src.features.inferencia.engine import InferenceEngine

import sys
import os

if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)
    db_path = os.path.join(base_dir, "users.db")
else:
    db_path = "users.db"

db_manager = DatabaseManager(db_path)
camera_manager = CameraManager(CAMERA_INDEX)
engine = InferenceEngine(db_manager)

def start_services():
    camera_manager.start()
    engine.start()

def stop_services():
    camera_manager.stop()
    engine.stop()
