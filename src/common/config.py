CAMERA_INDEX = 0
MODEL_NAME = 'ArcFace'
DETECTOR_BACKEND = 'yunet'
DISTANCE_METRIC = 'cosine'
VERIFICATION_THRESHOLD = 0.28
LIVENESS_THRESHOLD = 0.70 
LIVENESS_MODEL_PATH = 'src/public/weights/2.7_80x80_MiniFASNetV2.pth'

import json
import os
import sys
from typing import Dict, Any

CONFIG_FILE = "db_config.json"

def get_app_data_dir():
    try:
        if sys.platform == 'win32':
            app_data = os.getenv('APPDATA')
        else:
            app_data = os.path.expanduser('~/.config')
        
        data_dir = os.path.join(app_data, 'FaceRecon')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        return data_dir
    except Exception as e:
        print(f"Error creating data dir: {e}")
        return "."


DATA_DIR = get_app_data_dir()
DB_CONFIG_FILE = os.path.join(DATA_DIR, "db_config.json")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")

DEFAULT_DB_CONFIG = {
    "type": "sqlite",  
    "host": os.path.join(DATA_DIR, "users.db"),
    "port": 5432,
    "user": "postgres",
    "password": "",
    "database": "face_recognition_db"
}

DEFAULT_SETTINGS = {




    "face_tech": {
        "required_hits": 1,
        "min_face_width": 0.15,
        "max_offset": 0.15,
        "threshold": 0.28,
        "metric": "cosine",
        "model_name": "ArcFace",
        "detector_backend": "yunet", 
        "check_similarity": False
    },
    "access_levels": ["Admin", "Funcionário", "Visitante"],
    "style": {
        "theme_mode": "dark",
        "primary_color": "blue"
    }
}

class DatabaseConfigManager:
    def __init__(self):
        self._config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        if not os.path.exists(DB_CONFIG_FILE):
            self.save_config(DEFAULT_DB_CONFIG)
            return DEFAULT_DB_CONFIG.copy()
        
        try:
            with open(DB_CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading db config: {e}")
            return DEFAULT_DB_CONFIG.copy()

    def save_config(self, config: Dict[str, Any]):
        try:
            with open(DB_CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            self._config = config
        except Exception as e:
            print(f"Error saving db config: {e}")

    @property
    def config(self) -> Dict[str, Any]:
        return self._config

class SettingsManager:
    def __init__(self):
        self._config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        if not os.path.exists(SETTINGS_FILE):
            self.save_config(DEFAULT_SETTINGS)
            return DEFAULT_SETTINGS.copy()
        
        try:
            with open(SETTINGS_FILE, 'r') as f:
                config = json.load(f)
                # Ensure structure integrity by merging with default
                # This handles cases where we add new keys (like detector_backend)
                # and the user has an old config file
                merged = DEFAULT_SETTINGS.copy()
                
                # Deep merge for dictionary fields
                for key, value in config.items():
                    if isinstance(value, dict) and key in merged and isinstance(merged[key], dict):
                        merged[key].update(value)
                    else:
                        merged[key] = value
                
                return merged
        except Exception as e:
            print(f"Error loading settings: {e}")
            return DEFAULT_SETTINGS.copy()

    def save_config(self, config: Dict[str, Any]):
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            self._config = config
        except Exception as e:
            print(f"Error saving settings: {e}")

    @property
    def config(self) -> Dict[str, Any]:
        return self._config

# Renaming to support backward compatibility where possible, or just new usage
db_config = DatabaseConfigManager()
settings_manager = SettingsManager()
