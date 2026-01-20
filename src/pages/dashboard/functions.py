from src.services.services import db_manager, engine, camera_manager
import cv2
import base64
from nicegui import run
import time

def get_all_users():
    return db_manager.get_users()

def delete_user_from_db(uid):
    db_manager.delete_user(uid)

def get_user_photos(user_id):
    return db_manager.get_user_photos(user_id)

def delete_photo_from_db(photo_id):
    return db_manager.delete_user_photo(photo_id)

async def reload_model_logic():
    await run.io_bound(engine.load_model)

def read_camera_frame():
    return camera_manager.read()

def process_frame_for_display(frame):
    flipped_frame = cv2.flip(frame, 1)
    _, buffer = cv2.imencode('.jpg', flipped_frame)
    return base64.b64encode(buffer).decode('utf-8')

async def generate_embedding_logic(frame):
    was_paused = engine.paused
    engine.paused = True
    try:
        await run.io_bound(lambda: time.sleep(0.001))
        embedding_objs = await run.io_bound(engine.generate_embedding, frame)
        return embedding_objs
    finally:
        engine.paused = was_paused

import asyncio

async def verify_enrollment_logic(frame):
    was_paused = engine.paused
    engine.paused = True
    try:
        await run.io_bound(lambda: time.sleep(0.001))
        # Set a timeout (e.g., 10 seconds) to prevent infinite hanging
        result = await asyncio.wait_for(
            run.io_bound(engine.verify_enrollment_face, frame),
            timeout=10.0
        )
        return result
    except asyncio.TimeoutError:
         return {'success': False, 'message': 'O sistema demorou muito para responder (Timeout). Tente novamente.', 'embedding': None, 'matched_user': None}
    finally:
        engine.paused = was_paused

def add_user_photo_db(user_id, frame, emb):
    return db_manager.add_user_photo(user_id, frame, emb)

def update_user_db(user_id, updates):
    return db_manager.update_user(user_id, **updates)

def create_user_db(name, pin, access_level):
    return db_manager.create_user(name=name, pin=pin, access_level=access_level)

def pause_engine():
    engine.paused = True
