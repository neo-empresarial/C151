
from src.common.database import DatabaseManager
from scipy.spatial.distance import cosine

class AuthManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        # Threshold for cosine distance (lower means more similar)
        # DeepFace default for Facenet is usually 0.40
        self.face_threshold = 0.40 

    def authenticate_face(self, target_embedding):
        """
        Compare target embedding with all users.
        Returns: (user_dict, score) or (None, best_score)
        """
        # Get all embeddings from DB (in-memory cache ideally, but DB get is fast enough for now or engine handles cache)
        # Note: The engine.py usually handles the tight loop comparison. 
        # This method might be used for single-shot verification or if we move logic here.
        # However, for real-time video, the engine loop does it.
        # Let's assume this is for 'Verification' actions if needed, or Engine calls this?
        # Actually, Engine is efficient with caching. 
        # Use this for decision logic AFTER engine finds a "best match".
        pass 

    def validate_access_by_pin(self, pin):
        """
        Validate PIN and return user if valid.
        """
        user = self.db_manager.get_user_by_pin(pin)
        if user:
            return True, user
        return False, None

    def check_permission(self, user, required_level="Admin"):
        """
        Check if user has required permission.
        Levels: Admin > Funcionario > Visitante
        """
        levels = {"Admin": 3, "Funcionario": 2, "Visitante": 1}
        
        user_level = user.get("access_level", "Visitante")
        
        if levels.get(user_level, 0) >= levels.get(required_level, 1):
            return True
        return False
