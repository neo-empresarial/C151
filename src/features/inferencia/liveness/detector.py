
import cv2
import torch
import torch.nn.functional as F
import numpy as np
import logging
import os
import sys

from src.common.config import LIVENESS_MODEL_PATH, LIVENESS_THRESHOLD
from src.features.inferencia.liveness.model import MiniFASNetV2

class LivenessDetector:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.is_loaded = False
        self._load_model()

    def _load_model(self):
        try:
            model_path = LIVENESS_MODEL_PATH
            if getattr(sys, 'frozen', False):
                if hasattr(sys, '_MEIPASS'):
                    base_path = sys._MEIPASS
                else:
                    base_path = os.path.dirname(os.path.abspath(sys.executable))
                model_path = os.path.join(base_path, LIVENESS_MODEL_PATH)

            if not os.path.exists(model_path):
                logging.warning(f"Liveness model not found at {model_path}. Liveness check will be disabled.")
                return
            self.model = MiniFASNetV2(conv6_kernel=(5, 5)).to(self.device)
            state_dict = torch.load(model_path, map_location=self.device)
            if list(state_dict.keys())[0].startswith('module.'):
                from collections import OrderedDict
                new_state_dict = OrderedDict()
                for k, v in state_dict.items():
                    name = k.replace("module.", "")
                    new_state_dict[name] = v
                state_dict = new_state_dict
                
            self.model.load_state_dict(state_dict)
            self.model.eval()
            self.is_loaded = True
            logging.info(f"Liveness model loaded successfully from {LIVENESS_MODEL_PATH} on {self.device}")

        except Exception as e:
            logging.error(f"Failed to load liveness model: {e}")
            self.is_loaded = False

    def check_liveness(self, face_img):
        if not self.is_loaded or face_img is None or face_img.size == 0:
            return True, 0.0

        try:
            img = cv2.resize(face_img, (80, 80))
            img = img.transpose((2, 0, 1))
            img = np.ascontiguousarray(img)
            
            img = torch.from_numpy(img).float().unsqueeze(0)
            img = img.to(self.device)

            with torch.no_grad():
                output = self.model(img)
                probs = F.softmax(output, dim=1)            
                score = probs[0][1].item()
                logging.info(f"Liveness Probs: {probs[0].tolist()}") 
            
            is_real = score > LIVENESS_THRESHOLD
            return is_real, score

        except Exception as e:
            logging.error(f"Liveness check error: {e}")
            return True, 0.0 