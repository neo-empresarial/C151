CAMERA_INDEX = 0
MODEL_NAME = 'ArcFace'
DETECTOR_BACKEND = 'mtcnn'
DISTANCE_METRIC = 'cosine'
VERIFICATION_THRESHOLD = 0.28
LIVENESS_THRESHOLD = 0.70 
LIVENESS_MODEL_PATH = 'src/public/weights/2.7_80x80_MiniFASNetV2.pth'

import json
import os
from typing import Dict, Any

CONFIG_FILE = "db_config.json"

DEFAULT_CONFIG = {
    "type": "sqlite",  
    "host": "users.db",
    "port": 5432,
    "user": "postgres",
    "password": "",
    "database": "face_recognition_db",
    "face_tech": {
        "required_hits": 1,
        "min_face_width": 0.15,
        "max_offset": 0.15,
        "threshold": 0.28,
        "metric": "cosine",
        "model_name": "ArcFace"
    },
    "access_levels": ["Admin", "Funcionário", "Visitante"],
    "style": {
        "theme_mode": "dark",
        "primary_color": "blue"
    }
}

class ConfigManager:
    def __init__(self):
        self._config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        if not os.path.exists(CONFIG_FILE):
            self.save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG.copy()
        
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return DEFAULT_CONFIG.copy()

    def save_config(self, config: Dict[str, Any]):
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            self._config = config
        except Exception as e:
            print(f"Error saving config: {e}")

    @property
    def config(self) -> Dict[str, Any]:
        return self._config

db_config = ConfigManager()
