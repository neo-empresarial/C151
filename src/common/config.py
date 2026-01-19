CAMERA_INDEX = 0

THEME_COLORS = {
    'background': '#f3f3f3', 
    'surface': '#ffffff',
    'primary': '#0067c0',    
    'text_primary': '#202020',
    'text_secondary': '#5d5d5d',
    'border': '#e5e5e5',
    'success': '#107c10',
    'error': '#c42b1c'
}

MODEL_NAME = 'ArcFace'
DETECTOR_BACKEND = 'mtcnn'
DISTANCE_METRIC = 'cosine'
VERIFICATION_THRESHOLD = 0.28

# Liveness / Anti-Spoofing
LIVENESS_THRESHOLD = 0.70  # Threshold for "Real" class score
LIVENESS_MODEL_PATH = 'src/public/weights/2.7_80x80_MiniFASNetV2.pth'
