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
                pin TEXT,
                access_level TEXT DEFAULT 'Visitante'
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS face_embeddings (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                embedding BLOB,
                image_blob BLOB,
                created_at TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        
        cursor.execute("PRAGMA table_info(users)")
        columns = [info[1] for info in cursor.fetchall()]
        
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
        
        query = '''
            SELECT f.user_id, u.name, f.embedding, u.access_level, f.id 
            FROM face_embeddings f
            JOIN users u ON f.user_id = u.id
            WHERE f.embedding IS NOT NULL
        '''
        cursor.execute(query)
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
                    "access_level": row[3],
                    "photo_id": row[4]     
                })
            except:
                pass
        return results

    def get_user_by_name(self, name):
        conn = sqlite3.connect(self.sqlite_file)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, access_level FROM users WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"id": row[0], "name": row[1], "access_level": row[2]}
        return None

    def get_user_photos(self, user_id):
        conn = sqlite3.connect(self.sqlite_file)
        cursor = conn.cursor()
        cursor.execute("SELECT id, image_blob, created_at FROM face_embeddings WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        
        photos = []
        for row in rows:
            if row[1]:
                photos.append({
                    "id": row[0],
                    "image_blob": row[1],
                    "created_at": row[2]
                })
        return photos

    def get_user_image(self, user_id):
        photos = self.get_user_photos(user_id)
        if photos:
            return photos[0]["image_blob"]
        return None

    def create_user(self, name, pin=None, access_level="Visitante", frame=None, embedding=None):
        if not name:
            return False, "O nome não pode ser vazio."
        
        existing = self.get_user_by_name(name)
        if existing:
            return False, f"Usuário '{name}' já existe."

        user_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now().isoformat()
        
        try:
            conn = sqlite3.connect(self.sqlite_file)
            cursor = conn.cursor()
            
            cursor.execute("INSERT INTO users (id, name, created_at, pin, access_level) VALUES (?, ?, ?, ?, ?)", 
                           (user_id, name, timestamp, pin, access_level))
            
            conn.commit()
            conn.close()

            if frame is not None and embedding is not None:
                self.add_user_photo(user_id, frame, embedding)
            
            return True, user_id
            
        except Exception as e:
            return False, str(e)

    def add_user_photo(self, user_id, frame, embedding):
        try:
            photo_id = str(uuid.uuid4())
            timestamp = datetime.datetime.now().isoformat()
            
            embedding_blob = pickle.dumps(embedding)
            _, img_encoded = cv2.imencode('.jpg', frame)
            image_blob = img_encoded.tobytes()

            conn = sqlite3.connect(self.sqlite_file)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO face_embeddings (id, user_id, embedding, image_blob, created_at) VALUES (?, ?, ?, ?, ?)",
                           (photo_id, user_id, embedding_blob, image_blob, timestamp))
            conn.commit()
            conn.close()
            return True, photo_id
        except Exception as e:
            return False, str(e)

    def delete_user_photo(self, photo_id):
        try:
            conn = sqlite3.connect(self.sqlite_file)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM face_embeddings WHERE id = ?", (photo_id,))
            conn.commit()
            conn.close()
            return True, "Foto removida."
        except Exception as e:
            return False, str(e)

    def update_user(self, user_id, name=None, pin=None, access_level=None):
        """Atualiza dados cadastrais do usuário (não fotos)."""
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
            cursor.execute("DELETE FROM face_embeddings WHERE user_id = ?", (user_id,))
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
