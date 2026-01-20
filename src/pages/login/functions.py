from src.services.services import db_manager, engine
import cv2
import base64

def check_users_exist():
    users = db_manager.get_users()
    return bool(users)

def verify_pin(pin_value):
    return db_manager.get_user_by_pin(pin_value)

def update_engine_frame(frame):
    engine.update_frame(frame)

def get_engine_results():
    return engine.get_results()

def frame_to_b64(frame):
    flipped = cv2.flip(frame, 1)
    _, buffer = cv2.imencode('.jpg', flipped)
    return base64.b64encode(buffer).decode("utf-8")


def resume_engine():
    engine.paused = False

def pause_engine():
    engine.paused = True
