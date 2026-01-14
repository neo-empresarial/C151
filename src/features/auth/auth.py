
from src.common.database import DatabaseManager

class AuthManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.face_threshold = 0.40 

    def validate_access_by_pin(self, pin):
        user = self.db_manager.get_user_by_pin(pin)
        if user:
            return True, user
        return False, None

    def check_permission(self, user, required_level="Admin"):
        levels = {"Admin": 3, "Funcionario": 2, "Visitante": 1}
        
        user_level = user.get("access_level", "Visitante")
        
        if levels.get(user_level, 0) >= levels.get(required_level, 1):
            return True
        return False
