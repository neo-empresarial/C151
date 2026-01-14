import os
import sqlite3
import shutil
import uuid
import datetime
import cv2
import pickle
import numpy as np

class DatabaseManager:
    def __init__(self, sqlite_file="users.db"):
        self.sqlite_file = sqlite_file
        
        # Initialize SQLite
        self.init_db()

    def init_db(self):
        """Initialize the SQLite database with the users table."""
        conn = sqlite3.connect(self.sqlite_file)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                created_at TEXT,
                embedding BLOB,
                image_blob BLOB
            )
        ''')
        
        # Check if columns exist (migration for existing db)
        cursor.execute("PRAGMA table_info(users)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'embedding' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN embedding BLOB")
        if 'image_blob' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN image_blob BLOB")
            
        conn.commit()
        conn.close()

    def get_users(self):
        """Retrieve all users key-value pairs (id, name)."""
        conn = sqlite3.connect(self.sqlite_file)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM users ORDER BY name")
        rows = cursor.fetchall()
        conn.close()
        return [{"id": row[0], "name": row[1]} for row in rows]

    def get_all_embeddings(self):
        """Retrieve all user embeddings for in-memory recognition."""
        conn = sqlite3.connect(self.sqlite_file)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, embedding FROM users WHERE embedding IS NOT NULL")
        rows = cursor.fetchall()
        conn.close()
        
        results = []
        for row in rows:
            try:
                embedding = pickle.loads(row[2])
                results.append({
                    "id": row[0],
                    "name": row[1],
                    "embedding": embedding
                })
            except:
                pass
        return results

    def get_user_by_name(self, name):
        """Find a user by name."""
        conn = sqlite3.connect(self.sqlite_file)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, embedding FROM users WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"id": row[0], "name": row[1]}
        return None

    def get_user_image(self, user_id):
        """Retrieve the image blob for a specific user ID."""
        conn = sqlite3.connect(self.sqlite_file)
        cursor = conn.cursor()
        cursor.execute("SELECT image_blob FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row and row[0]:
            return row[0]
        return None

    def create_user(self, name, frame, embedding=None):
        """Create a new user with generated ID, save metadata, image blob, and embedding to SQLite."""
        if not name:
            return False, "O nome não pode ser vazio."
        
        existing = self.get_user_by_name(name)
        if existing:
            return False, f"Usuário '{name}' já existe."

        user_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now().isoformat()
        
        try:
            # Serialize embedding
            embedding_blob = pickle.dumps(embedding) if embedding is not None else None
            
            # Encode image to BLOB
            _, img_encoded = cv2.imencode('.jpg', frame)
            image_blob = img_encoded.tobytes()

            conn = sqlite3.connect(self.sqlite_file)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (id, name, created_at, embedding, image_blob) VALUES (?, ?, ?, ?, ?)", 
                           (user_id, name, timestamp, embedding_blob, image_blob))
            conn.commit()
            conn.close()
            
            return True, user_id
            
        except Exception as e:
            return False, str(e)

    def update_user(self, user_id, new_name, frame=None, embedding=None):
        """Update user data (name and optionally photo/embedding) using ID."""
        if not new_name:
            return False, "Nome não pode ser vazio."
            
        try:
            conn = sqlite3.connect(self.sqlite_file)
            cursor = conn.cursor()
            
            # Check if new name exists for OTHER user
            cursor.execute("SELECT id FROM users WHERE name = ? AND id != ?", (new_name, user_id))
            if cursor.fetchone():
                conn.close()
                return False, f"Já existe outro usuário com o nome '{new_name}'."

            if frame is not None:
                # Update Photo & Name & Embedding
                embedding_blob = pickle.dumps(embedding) if embedding is not None else None
                _, img_encoded = cv2.imencode('.jpg', frame)
                image_blob = img_encoded.tobytes()
                
                cursor.execute("""
                    UPDATE users 
                    SET name = ?, image_blob = ?, embedding = ? 
                    WHERE id = ?
                """, (new_name, image_blob, embedding_blob, user_id))
            else:
                # Update Name Only
                cursor.execute("UPDATE users SET name = ? WHERE id = ?", (new_name, user_id))
            
            conn.commit()
            conn.close()
            
            return True, "Dados atualizados com sucesso."
        except Exception as e:
            return False, str(e)

    def delete_user(self, name):
        """Delete user from DB."""
        # Check logic: do we still delete from filesystem? 
        # Plan said specific "Database Only". So we focus on DB.
        # But for cleanup we might check FS.
        
        # 1. DB Delete
        try:
            conn = sqlite3.connect(self.sqlite_file)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE name = ?", (name,))
            conn.commit()
            conn.close()
            
            # 2. Legacy Cleanup (if exists)
            user_dir = os.path.join(self.db_folder, name)
            if os.path.exists(user_dir):
                shutil.rmtree(user_dir)

            return True, "Usuário removido."
        except Exception as e:
            return False, str(e)
