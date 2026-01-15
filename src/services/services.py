from src.common.config import CAMERA_INDEX
from src.common.database import DatabaseManager
from src.common.camera import CameraManager
from src.features.inferencia.engine import InferenceEngine

db_manager = DatabaseManager()
camera_manager = CameraManager(CAMERA_INDEX)
engine = InferenceEngine(db_manager)

def start_services():
    camera_manager.start()
    engine.start()

def stop_services():
    try:
        camera_manager.stop()
    except Exception as e:
        print(f"Error stopping camera: {e}")
        
    try:
        engine.stop()
    except Exception as e:
        print(f"Error stopping engine: {e}")
