from collections import deque
from collections import Counter
import threading

class AccessController:
    def __init__(self):
        self.denied = False
        self.user = None
        self.lock = threading.Lock()
        self.history = deque(maxlen=5)
        self.unauthorized_count = 0

    def process_result(self, results):
        found_admin = False
        found_someone = False
        
        if results:
            for res in results:
                found_someone = True
                if res.get("access_level") == "Admin":
                    found_admin = True
                    break
        
        with self.lock:
            if found_someone and not found_admin:
                self.unauthorized_count += 1
                if self.unauthorized_count >= 5:
                    if not self.denied:
                        self.denied = True
                        self.user = results[0]["name"]
                    return "DENY"
            
            elif found_admin:
                self.unauthorized_count = 0
                if self.denied:
                    self.denied = False
                    self.user = None
                    return "ALLOW"
            
            else:
                self.unauthorized_count = 0
                
            return "NEUTRAL"

    def unlock_with_pin(self, pin, db_manager):
        user = db_manager.get_user_by_pin(pin)
        if user and user.get("access_level") == "Admin":
            with self.lock:
                self.denied = False
                self.unauthorized_count = 0
            return True
        return False
