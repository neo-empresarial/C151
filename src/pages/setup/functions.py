from deepface import DeepFace
from src.services.services import db_manager, engine
from src.common.config import MODEL_NAME, DETECTOR_BACKEND

async def create_admin_user(name, pin, frame):
    embedding_objs = DeepFace.represent(
        img_path=frame,
        model_name=MODEL_NAME,
        detector_backend=DETECTOR_BACKEND,
        enforce_detection=True
    )
    embedding = embedding_objs[0]['embedding']
    
    db_manager.create_user(
        name=name, 
        frame=frame,
        embedding=embedding,
        pin=pin, 
        access_level="Admin"
    )
    engine.load_model()
