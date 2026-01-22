from src.common.config import CAMERA_INDEX
from src.common.database import DatabaseManager
from src.common.camera import CameraManager
from src.features.inferencia.engine import InferenceEngine

import sys
import os


db_manager = DatabaseManager()
camera_manager = CameraManager(CAMERA_INDEX)
engine = InferenceEngine(db_manager)

def start_services():
    camera_manager.start()
    engine.start()

def stop_services():
    print("DEBUG: stop_services called")
    try:
        print("DEBUG: Stopping camera_manager...")
        camera_manager.stop()
        print("DEBUG: camera_manager stopped")
    except Exception as e:
        print(f"Error stopping camera: {e}")
        
    try:
        print("DEBUG: Stopping engine...")
        engine.stop()
        print("DEBUG: engine stopped")
    except Exception as e:
        print(f"Error stopping engine: {e}")

