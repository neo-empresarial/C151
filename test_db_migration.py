
import os
import sys
import sqlite3

# Add src to path
sys.path.append(os.getcwd())

from src.common.database import DatabaseManager

def test_migration():
    print("Testing Database Migration...")
    
    # 1. Initialize DB (should run migration)
    db = DatabaseManager("users.db")
    print("DB Initialized.")
    
    # 2. Check columns
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(users)")
    columns = [info[1] for info in cursor.fetchall()]
    conn.close()
    
    print(f"Columns found: {columns}")
    
    expected = ['id', 'name', 'created_at', 'embedding', 'image_blob', 'pin', 'access_level']
    missing = [col for col in expected if col not in columns]
    
    if missing:
        print(f"FAILED: Missing columns: {missing}")
        sys.exit(1)
    else:
        print("SUCCESS: All columns present.")

    # 3. Test Insert with new fields
    print("Testing Insert with PIN and Access Level...")
    success, uid = db.create_user("TestAdmin", None, pin="1234", access_level="Admin")
    if success:
        print(f"User created: {uid}")
        
        # Verify
        user = db.get_user_by_name("TestAdmin")
        print(f"Retrieved: {user}")
        
        if user['access_level'] == 'Admin':
            print("SUCCESS: Access level correct.")
        else:
            print(f"FAILED: Access level is {user.get('access_level')}")

        # Test PIN
        if db.validate_pin(uid, "1234"):
            print("SUCCESS: PIN validated.")
        else:
            print("FAILED: PIN validation.")

        # Cleanup
        db.delete_user(uid)
        print("Test user deleted.")
        
    else:
        print(f"FAILED to create user: {uid}")

if __name__ == "__main__":
    test_migration()
