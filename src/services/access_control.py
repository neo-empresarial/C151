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
        self.authorized_count = 0
        self.last_authorized_user = None

    def process_result(self, results):
        found_admin = False
        found_someone = False
        admin_name = None
        
        if results:
            for res in results:
                found_someone = True
                
                if not res.get("is_real", True) or res.get("access_level") == "Negado":
                    continue

                if res.get("access_level") == "Admin":
                    found_admin = True
                    admin_name = res.get("name")
                    break
        
        with self.lock:
            if found_someone and not found_admin:
                self.unauthorized_count += 1
                print(f"DEBUG: Unauthorized Count: {self.unauthorized_count}", flush=True)
                self.authorized_count = 0 
                self.last_authorized_user = None
                
                if self.unauthorized_count >= 3:
                    if not self.denied:
                        print(f"DEBUG: AccessController - DENIED triggered (Hit {self.unauthorized_count}/3). User={results[0]['name'] if results else 'Unknown'}", flush=True)
                        self.denied = True
                        self.user = results[0]["name"] if results else "Desconhecido"
                    return "DENY"
            elif found_admin:
                self.unauthorized_count = 0
                if admin_name == self.last_authorized_user:
                    self.authorized_count += 1
                else:
                    self.authorized_count = 1
                    self.last_authorized_user = admin_name
                print(f"DEBUG: Admin Found: {admin_name} - Count: {self.authorized_count}", flush=True)
                if self.authorized_count >= 3:
                     if self.denied:
                         print("DEBUG: AccessController - Admin authorized (3x). Resetting denied state.", flush=True)
                         self.denied = False
                         self.user = None
                     return "ALLOW"
            
            else:
                self.unauthorized_count = 0
                self.authorized_count = 0
                self.last_authorized_user = None
            
            return "NEUTRAL"

    def unlock_with_pin(self, pin, db_manager):
        user = db_manager.get_user_by_pin(pin)
        if user and user.get("access_level") == "Admin":
            with self.lock:
                self.denied = False
                self.unauthorized_count = 0
            return True
        return False
