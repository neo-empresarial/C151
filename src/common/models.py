from sqlalchemy import Column, String, ForeignKey, LargeBinary, Integer
from sqlalchemy.orm import declarative_base, relationship
import uuid
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, unique=True)
    created_at = Column(String, default=lambda: datetime.datetime.now().isoformat())
    pin = Column(String, nullable=True) 
    access_level = Column(String, default='Visitante')

    face_embeddings = relationship("FaceEmbedding", back_populates="user", cascade="all, delete-orphan")

class FaceEmbedding(Base):
    __tablename__ = 'face_embeddings'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    embedding = Column(LargeBinary) 
    image_blob = Column(LargeBinary) 
    created_at = Column(String, default=lambda: datetime.datetime.now().isoformat())

    user = relationship("User", back_populates="face_embeddings")
