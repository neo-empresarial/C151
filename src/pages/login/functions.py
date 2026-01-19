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

def draw_face_box(frame, res, w_frame):
    x, y, w, h = res["box"]
    known = res["known"]
    name = res.get("name", "Desconhecido")
    in_roi = res.get("in_roi", False)
    
    mirror_x = w_frame - x - w
    
    color = (100, 100, 100)
    if in_roi:
        if known:
            color = (0, 255, 0)
        else:
            color = (0, 0, 255)
    else:
        color = (0, 255, 255)
    
    cv2.rectangle(frame, (mirror_x, y), (mirror_x+w, y+h), color, 2)
    
    if not in_roi:
            cv2.putText(frame, "Centralize", (mirror_x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    else:
            cv2.putText(frame, name, (mirror_x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    
    return frame
