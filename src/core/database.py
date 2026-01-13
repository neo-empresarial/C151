import os
import shutil
import cv2

class DatabaseManager:
    def __init__(self, db_path="database"):
        self.db_path = db_path
        os.makedirs(self.db_path, exist_ok=True)

    def get_users(self):
        users = []
        if os.path.exists(self.db_path):
            for name in os.listdir(self.db_path):
                if os.path.isdir(os.path.join(self.db_path, name)):
                    users.append(name)
        return sorted(users)

    def user_exists(self, name):
        return os.path.exists(os.path.join(self.db_path, name))

    def create_user(self, name, frame):
        if not name:
            return False, "Name cannot be empty"
        
        user_dir = os.path.join(self.db_path, name)
        
        if os.path.exists(user_dir):
            # If directory exists, check if it has images. If so, user exists.
            # If we are updating, we might want to allow this, but for create_user strictly:
            if any(fname.endswith(('.jpg', '.png')) for fname in os.listdir(user_dir)):
                 return False, "User already exists"
        
        try:
            os.makedirs(user_dir, exist_ok=True)
            img_path = os.path.join(user_dir, f"{name}.jpg")
            cv2.imwrite(img_path, frame)
            
            self._clear_cache()
            return True, "User created successfully"
        except Exception as e:
            return False, str(e)

    def delete_user(self, name):
        user_dir = os.path.join(self.db_path, name)
        if not os.path.exists(user_dir):
            return False, "User does not exist"
        
        try:
            shutil.rmtree(user_dir)
            self._clear_cache()
            return True, "User deleted successfully"
        except Exception as e:
            return False, str(e)

    def _clear_cache(self):
        for root, dirs, files in os.walk(self.db_path):
            for file in files:
                if file.endswith(".pkl"):
                    try:
                        os.remove(os.path.join(root, file))
                    except:
                        pass
