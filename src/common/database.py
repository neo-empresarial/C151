import sqlite3
import uuid
import datetime
import cv2
import pickle

class DatabaseManager:
    def __init__(self, sqlite_file="users.db"):
        self.sqlite_file = sqlite_file
        
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.sqlite_file)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                created_at TEXT,
                embedding BLOB,
                image_blob BLOB,
                pin TEXT,
                access_level TEXT DEFAULT 'Visitante'
            )
        ''')
        
        cursor.execute("PRAGMA table_info(users)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'embedding' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN embedding BLOB")
        if 'image_blob' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN image_blob BLOB")
        if 'pin' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN pin TEXT")
        if 'access_level' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN access_level TEXT DEFAULT 'Visitante'")
            
        conn.commit()
        conn.close()

    def get_users(self):
        conn = sqlite3.connect(self.sqlite_file)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, access_level, pin FROM users ORDER BY name")
        rows = cursor.fetchall()
        conn.close()
        return [{"id": row[0], "name": row[1], "access_level": row[2], "pin": row[3]} for row in rows]

    def get_all_embeddings(self):
        conn = sqlite3.connect(self.sqlite_file)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, embedding, access_level FROM users WHERE embedding IS NOT NULL")
        rows = cursor.fetchall()
        conn.close()
        
        results = []
        for row in rows:
            try:
                embedding = pickle.loads(row[2])
                results.append({
                    "id": row[0],
                    "name": row[1],
                    "embedding": embedding,
                    "access_level": row[3]
                })
            except:
                pass
        return results

    def get_user_by_name(self, name):
        conn = sqlite3.connect(self.sqlite_file)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, embedding, access_level FROM users WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"id": row[0], "name": row[1], "access_level": row[3]}
        return None

    def get_user_image(self, user_id):
        conn = sqlite3.connect(self.sqlite_file)
        cursor = conn.cursor()
        cursor.execute("SELECT image_blob FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row and row[0]:
            return row[0]
        return None

    def create_user(self, name, frame, embedding=None, pin=None, access_level="Visitante"):
        if not name:
            return False, "O nome não pode ser vazio."
        
        existing = self.get_user_by_name(name)
        if existing:
            return False, f"Usuário '{name}' já existe."

        user_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now().isoformat()
        
        try:
            embedding_blob = pickle.dumps(embedding) if embedding is not None else None
            
            if frame is not None:
                _, img_encoded = cv2.imencode('.jpg', frame)
                image_blob = img_encoded.tobytes()
            else:
                image_blob = None

            conn = sqlite3.connect(self.sqlite_file)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (id, name, created_at, embedding, image_blob, pin, access_level) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                           (user_id, name, timestamp, embedding_blob, image_blob, pin, access_level))
            conn.commit()
            conn.close()
            
            return True, user_id
            
        except Exception as e:
            return False, str(e)

    def update_user(self, user_id, name, frame=None, embedding=None, pin=None, access_level=None):
        if name is not None and not name:
            return False, "Nome não pode ser vazio."
            
        try:
            conn = sqlite3.connect(self.sqlite_file)
            cursor = conn.cursor()
            
            if name:
                cursor.execute("SELECT id FROM users WHERE name = ? AND id != ?", (name, user_id))
                if cursor.fetchone():
                    conn.close()
                    return False, f"Já existe outro usuário com o nome '{name}'."

            updates = []
            params = []
            
            if name:
                updates.append("name = ?")
                params.append(name)
            
            if frame is not None:
                embedding_blob = pickle.dumps(embedding) if embedding is not None else None
                _, img_encoded = cv2.imencode('.jpg', frame)
                image_blob = img_encoded.tobytes()
                
                updates.append("image_blob = ?")
                updates.append("embedding = ?")
                params.extend([image_blob, embedding_blob])
            
            if pin is not None:
                updates.append("pin = ?")
                params.append(pin)
                
            if access_level is not None:
                updates.append("access_level = ?")
                params.append(access_level)

            if not updates:
                conn.close()
                return True, "Nada para atualizar."

            params.append(user_id)
            sql = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
            
            cursor.execute(sql, params)
            conn.commit()
            conn.close()
            
            return True, "Dados atualizados com sucesso."
        except Exception as e:
            return False, str(e)

    def delete_user(self, user_id):
        try:
            conn = sqlite3.connect(self.sqlite_file)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            conn.close()
            return True, "Usuário removido."
        except Exception as e:
            return False, str(e)
            
    def validate_pin(self, user_id, pin):
        try:
            conn = sqlite3.connect(self.sqlite_file)
            cursor = conn.cursor()
            cursor.execute("SELECT pin FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row and row[0] == pin:
                 return True
            return False
        except:
            return False

    def get_user_by_pin(self, pin):
        conn = sqlite3.connect(self.sqlite_file)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, access_level FROM users WHERE pin = ?", (pin,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"id": row[0], "name": row[1], "access_level": row[2]}
        return None
