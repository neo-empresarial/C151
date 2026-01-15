import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.common.database import DatabaseManager

db = DatabaseManager()
users = db.get_users()
print(f"Found {len(users)} users:")
for u in users:
    print(f"- {u['name']}: {u['access_level']}")
