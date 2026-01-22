from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import pickle
import numpy as np
import cv2
from contextlib import contextmanager
import sys

from src.common.config import db_config
from src.common.security import encrypt_data, decrypt_data, encrypt_bytes, decrypt_bytes
from src.common.models import Base, User, FaceEmbedding

class DatabaseManager:
    def __init__(self):
        print(f"DEBUG: Initializing DatabaseManager. Loaded Config: {db_config.config}")
        self.engine = self._create_engine()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.active_db_type = 'unknown'
        try:
             self.active_db_type = db_config.config.get("type", "sqlite")
        except: 
             pass
        self.init_db()

    def reload_engine(self):
        """Reloads the database engine based on current config."""
        print("DEBUG: Reloading database engine...")
        print(f"DEBUG: Current Config for Reload: {db_config.config}")
        try:
            self.engine.dispose()
        except:
            pass
            
        self.engine = self._create_engine()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        try:
            self.active_db_type = db_config.config.get("type", "sqlite")
        except:
            self.active_db_type = 'unknown'
            
        print(f"DEBUG: Database reloaded. Active type: {self.active_db_type}")

    def _create_engine(self):
        config = db_config.config
        try:
            db_type = config.get("type", "sqlite")
            print(f"DEBUG: Creating engine for type: {db_type}")
            
            if db_type == "sqlite":
                db_file = config.get("host", "users.db")
                print(f"DEBUG: SQLite Host: {db_file}")
                self.active_db_type = "sqlite"
                return create_engine(f"sqlite:///{db_file}", echo=True, connect_args={"check_same_thread": False})
            
            elif db_type == "postgres":
                user = config.get("user")
                password = config.get("password")
                host = config.get("host")
                port = config.get("port")
                db_name = config.get("database")
                print(f"DEBUG: Postgres Host: {host}, DB: {db_name}, User: {user}")
                self.active_db_type = "postgres"
                return create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db_name}", 
                                     echo=True,
                                     poolclass=QueuePool,
                                     connect_args={'connect_timeout': 5, 'sslmode': 'require'})
            else:
                 raise ValueError(f"Unsupported database type: {db_type}")
            
        except Exception as e:
            print(f"CRITICAL: DB Engine Creation Error: {e}")
            print("Falling back to local SQLite due to config error.")
            return create_engine("sqlite:///fallback_users.db", echo=True, connect_args={"check_same_thread": False})

    @staticmethod
    def test_connection(config):
        print(f"DEBUG: Testing connection with config: {config}")
        try:
            db_type = config.get("type", "sqlite")
            if db_type == "sqlite":
                db_file = config.get("host", "users.db")
                engine = create_engine(f"sqlite:///{db_file}", echo=True)
                with engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                return True, "Conexão SQLite bem-sucedida!"
            
            elif db_type == "postgres":
                user = config.get("user")
                password = config.get("password")
                host = config.get("host")
                port = config.get("port")
                db_name = config.get("database")
                engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db_name}", 
                                       echo=True, # Enable logging for connection test
                                       connect_args={'connect_timeout': 3, 'sslmode': 'require'})
                with engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                return True, "Conexão PostgreSQL bem-sucedida!"
            
            return False, f"Tipo de banco desconhecido: {db_type}"
        except Exception as e:
            return False, f"Falha na conexão: {str(e)}"

    @staticmethod
    def verify_and_setup_database(config):
        print(f"DEBUG: Verifying and Setting up DB with: {config}")
        try:
            db_type = config.get("type", "sqlite")
            engine = None
            
            if db_type == "sqlite":
                db_file = config.get("host", "users.db")
                engine = create_engine(f"sqlite:///{db_file}", echo=True, connect_args={"check_same_thread": False})
            
            elif db_type == "postgres":
                user = config.get("user")
                password = config.get("password")
                host = config.get("host")
                port = config.get("port")
                db_name = config.get("database")
                engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db_name}", 
                                     echo=True,
                                     poolclass=QueuePool,
                                     connect_args={'connect_timeout': 5, 'sslmode': 'require'})
            else:
                 return False, f"Tipo de banco desconhecido: {db_type}"

            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            Base.metadata.create_all(bind=engine)
            DatabaseManager._migrate_schema_static(engine, db_type)
            
            return True, "Conexão e Schema verificados com sucesso!"

        except Exception as e:
            return False, f"Erro na verificação/setup: {str(e)}"

    def init_db(self):
        try:
            Base.metadata.create_all(bind=self.engine)
            current_type = db_config.config.get("type", "sqlite")
            self._migrate_schema_static(self.engine, current_type)
        except Exception as e:
            print(f"CRITICAL DB ERROR: {e}")
            print("Falling back to local SQLite 'fallback_users.db' to allow application startup.")
            
            self.active_db_type = "sqlite_fallback"
            self.engine = create_engine("sqlite:///fallback_users.db", echo=True, connect_args={"check_same_thread": False})
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            
            Base.metadata.create_all(bind=self.engine)
            self._migrate_schema_static(self.engine, "sqlite")

    @staticmethod
    def _migrate_schema_static(engine, db_type):
        try:
            if db_type == "sqlite":
                with engine.connect() as conn:
                    result = conn.execute(text("PRAGMA table_info(users)")).fetchall()
                    columns = [row[1] for row in result]
                    
                    if 'access_level' not in columns:
                        print("Migrating: Adding 'access_level' column to users table...")
                        conn.execute(text("ALTER TABLE users ADD COLUMN access_level VARCHAR DEFAULT 'Visitante'"))
                        conn.commit()
                        print("Migration complete.")
        except Exception as e:
            print(f"Migration warning: {e}")

    def _migrate_schema(self):
        current_type = db_config.config.get("type", "sqlite")
        self._migrate_schema_static(self.engine, current_type)

    @contextmanager
    def get_session(self):
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_users(self):
        with self.get_session() as session:
            users = session.query(User).order_by(User.name).all()
            result = []
            for user in users:
                decrypted_pin = decrypt_data(user.pin) if user.pin else None
                result.append({
                    "id": user.id,
                    "name": user.name,
                    "access_level": user.access_level,
                    "pin": decrypted_pin
                })
            return result

    def get_all_embeddings(self):
        with self.get_session() as session:
            embeddings_records = session.query(FaceEmbedding).join(User).all()
            
            results = []
            for record in embeddings_records:
                try:
                    decrypted_emb_bytes = decrypt_bytes(record.embedding)
                    if not decrypted_emb_bytes:
                        continue
                    embedding = pickle.loads(decrypted_emb_bytes)
                    
                    results.append({
                        "id": record.user_id,
                        "name": record.user.name,
                        "embedding": embedding,
                        "access_level": record.user.access_level,
                        "photo_id": record.id
                    })
                except Exception as e:
                    print(f"Error loading embedding for user {record.user.name}: {e}")
                    pass
            return results

    def get_user_embeddings(self, user_id):
        """Retrieves all face embeddings for a specific user ID."""
        with self.get_session() as session:
            embeddings_records = session.query(FaceEmbedding).filter(FaceEmbedding.user_id == user_id).all()
            
            results = []
            for record in embeddings_records:
                try:
                    decrypted_emb_bytes = decrypt_bytes(record.embedding)
                    if not decrypted_emb_bytes:
                        continue
                    embedding = pickle.loads(decrypted_emb_bytes)
                    results.append(embedding)
                except Exception as e:
                    print(f"Error loading embedding for user {user_id}: {e}")
                    pass
            return results

    def get_user_by_name(self, name):
        with self.get_session() as session:
            user = session.query(User).filter(User.name == name).first()
            if user:
                return {
                    "id": user.id, 
                    "name": user.name, 
                    "access_level": user.access_level
                }
        return None

    def get_user_photos(self, user_id):
        with self.get_session() as session:
            photos = session.query(FaceEmbedding).filter(FaceEmbedding.user_id == user_id).all()
            result = []
            for photo in photos:
                decrypted_img = decrypt_bytes(photo.image_blob)
                if decrypted_img:
                    result.append({
                        "id": photo.id,
                        "image_blob": decrypted_img,
                        "created_at": photo.created_at
                    })
            return result

    def get_user_image(self, user_id):
        photos = self.get_user_photos(user_id)
        if photos:
            return photos[0]["image_blob"]
        return None

    def create_user(self, name, pin=None, access_level="Visitante", frame=None, embedding=None):
        if not name:
            return False, "O nome não pode ser vazio."
        
        with self.get_session() as session:
            existing = session.query(User).filter(User.name == name).first()
            if existing:
                return False, f"Usuário '{name}' já existe."

            encrypted_pin = encrypt_data(pin) if pin else None
            
            new_user = User(name=name, pin=encrypted_pin, access_level=access_level)
            session.add(new_user)
            session.flush() 

            if frame is not None and embedding is not None:
                self._add_user_photo_session(session, new_user.id, frame, embedding)
            
            return True, new_user.id

    def add_user_photo(self, user_id, frame, embedding):
        try:
            with self.get_session() as session:
                return self._add_user_photo_session(session, user_id, frame, embedding)
        except Exception as e:
            return False, str(e)
            
    def _add_user_photo_session(self, session, user_id, frame, embedding):
        try:
            embedding_blob = pickle.dumps(embedding)
            encrypted_embedding = encrypt_bytes(embedding_blob)
            
            _, img_encoded = cv2.imencode('.jpg', frame)
            image_blob = img_encoded.tobytes()
            encrypted_image = encrypt_bytes(image_blob)

            new_photo = FaceEmbedding(
                user_id=user_id,
                embedding=encrypted_embedding,
                image_blob=encrypted_image
            )
            session.add(new_photo)
            return True, new_photo.id
        except Exception as e:
             raise e

    def delete_user_photo(self, photo_id):
        try:
            with self.get_session() as session:
                photo = session.query(FaceEmbedding).filter(FaceEmbedding.id == photo_id).first()
                if photo:
                    session.delete(photo)
                    return True, "Foto removida."
                return False, "Foto não encontrada."
        except Exception as e:
            return False, str(e)

    def update_user(self, user_id, name=None, pin=None, access_level=None):
        if name is not None and not name:
            return False, "Nome não pode ser vazio."
            
        try:
            with self.get_session() as session:
                user = session.query(User).filter(User.id == user_id).first()
                if not user:
                    return False, "Usuário não encontrado."
                
                if name:
                    existing = session.query(User).filter(User.name == name, User.id != user_id).first()
                    if existing:
                        return False, f"Já existe outro usuário com o nome '{name}'."
                    user.name = name
                
                if pin is not None:
                    user.pin = encrypt_data(pin)
                    
                if access_level is not None:
                    user.access_level = access_level
                    
                return True, "Dados atualizados com sucesso."
        except Exception as e:
            return False, str(e)

    def delete_user(self, user_id):
        try:
            with self.get_session() as session:
                user = session.query(User).filter(User.id == user_id).first()
                if user:
                    session.delete(user)
                    return True, "Usuário removido."
                return False, "Usuário não encontrado."
        except Exception as e:
            return False, str(e)
            
    def validate_pin(self, user_id, pin):
        try:
            with self.get_session() as session:
                user = session.query(User).filter(User.id == user_id).first()
                if user and user.pin:
                    decrypted = decrypt_data(user.pin)
                    if decrypted == pin:
                        return True
            return False
        except:
            return False

    def get_user_by_pin(self, pin):
        with self.get_session() as session:
            users = session.query(User).filter(User.pin != None).all()
            for user in users:
                try:
                    decrypted = decrypt_data(user.pin)
                    if decrypted == pin:
                        return {"id": user.id, "name": user.name, "access_level": user.access_level}
                except:
                    continue
        return None
