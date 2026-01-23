import sys
import os
import sqlite3
import shutil

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.common.database import DatabaseManager
from src.common.config import db_config
from src.common.security import load_key

def verify_encryption():
    print("--- Starting Verification ---")
    
    if os.path.exists("test_users.db"):
        os.remove("test_users.db")
    
    original_config = db_config.config.copy()
    
    try:
        test_config = original_config.copy()
        test_config["host"] = "test_users.db"
        test_config["type"] = "sqlite"
        db_config.save_config(test_config)
        
        db = DatabaseManager()
        
        USER_NAME = "Test User"
        USER_PIN = "123456"
        
        print("\n[Action] Creating user with PIN...")
        success, uid = db.create_user(USER_NAME, pin=USER_PIN)
        if not success:
            print(f"FAILED: Could not create user. {uid}")
            return
        print(f"SUCCESS: User created with ID {uid}")
        
        print("\n[Check] Inspecting raw database file for encrypted PIN...")
        conn = sqlite3.connect("test_users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT pin FROM users WHERE id = ?", (uid,))
        raw_pin = cursor.fetchone()[0]
        conn.close()
        
        print(f"Raw PIN in DB: {raw_pin}")
        
        if raw_pin == USER_PIN:
            print("CRITICAL FAILURE: PIN is stored in PLAIN TEXT!")
        else:
            print("SUCCESS: PIN is NOT plain text (Encrypted).")
            
        print("\n[Check] Retrieving user via DatabaseManager (Decryption)...")
        db2 = DatabaseManager()
        users = db2.get_users()
        user = next((u for u in users if u["id"] == uid), None)
        
        if user and user["pin"] == USER_PIN:
             print("SUCCESS: PIN decrypted correctly in application.")
        else:
             print(f"FAILED: PIN decryption failed. Got {user['pin'] if user else 'None'}")
             
        print("\n[Check] Checking security key...")
        if os.path.exists("secret.key"):
            print("SUCCESS: secret.key exists.")
        else:
            print("FAILED: secret.key missing.")

    finally:
        db_config.save_config(original_config)
        if os.path.exists("test_users.db"):
            os.remove("test_users.db")
    
    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    verify_encryption()
