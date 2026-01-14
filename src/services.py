
from src.common.config import CAMERA_INDEX
from src.common.database import DatabaseManager
from src.common.camera import CameraManager
from src.features.inferencia.engine import InferenceEngine

# Singleton Instances
db_manager = DatabaseManager()
camera_manager = CameraManager(CAMERA_INDEX)
engine = InferenceEngine(db_manager)

def start_services():
    camera_manager.start()
    engine.start()

def stop_services():
    camera_manager.stop()
    engine.stop()
