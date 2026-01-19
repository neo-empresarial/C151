from nicegui import ui
import cv2
import base64
from src.services.services import camera_manager
from src.common.state import state
from . import functions as f
from .components import header, camera
from .components.pin_dialog import PinDialog, render_trigger_button

def login_page():
    if not f.check_users_exist():
        ui.navigate.to('/setup')
        return
    state.current_user = None
    state.is_admin = False
    
    with ui.column().classes('w-full h-screen items-center justify-center p-4 relative').style('background-color: var(--bg-mica);'):
        ui.label("Demo Version | © Fundação Certi 2026").classes('absolute bottom-4 text-gray-500 text-sm')

        with ui.card().classes('w11-card w-full max-w-[1000px] h-[700px] p-0 flex flex-col overflow-hidden'):
            header.render()
            video_image, feedback_label, face_overlay = camera.render_view()
            render_trigger_button(lambda: pin_dialog.open())

    def finalize_access(user):
        state.current_user = user
        feedback_label.text = f"Bem-vindo, {user['name']}!"
        feedback_label.style('background-color: var(--success); color: white;')
        if user.get('access_level') == 'Admin':
            state.is_admin = True
            ui.notify('Admin Identificado', type='positive')
        else:
            ui.notify('Acesso Liberado', type='positive')
            ui.timer(3.0, lambda: reset_state(), once=True)

    def reset_state():
        state.current_user = None
        state.is_admin = False
        feedback_label.text = "Aguardando rosto..."
        feedback_label.style('background-color: rgba(0,0,0,0.6);')

    logic_state = {'consecutive_hits': 0, 'last_user_id': None, 'in_cooldown': False}

    def trigger_access(user):
        logic_state['in_cooldown'] = True
        feedback_label.text = "ACESSO PERMITIDO"
        feedback_label.style('background-color: var(--success);')
        def on_timeout():
            finalize_access(user)
            logic_state['in_cooldown'] = False
            logic_state['consecutive_hits'] = 0
        ui.timer(2.0, on_timeout, once=True)

    pin_dialog = PinDialog(trigger_access)

    async def loop():
        if state.current_user or logic_state['in_cooldown']: pass
        ret, frame = camera_manager.read()
        if not ret:
            feedback_label.text = "Câmera desconectada"
            feedback_label.style('background-color: var(--error);')
            return

        if logic_state['in_cooldown']:
            # Show the last frame static
            # Optimization: We could just stop updating the image
            flipped_frame = cv2.flip(frame, 1)
            video_image.set_source(f'data:image/jpeg;base64,{f.frame_to_b64(frame)}') # Note: frame_to_b64 already flips
            return

        f.update_engine_frame(frame)
        results = f.get_engine_results()
        
        # Determine display frame
        display_frame = cv2.flip(frame, 1)
        h_frame, w_frame, _ = display_frame.shape
        
        # Calculate scaling for overlay
        # The container is fixed height 500px, width dynamic/full.
        # Ideally we know the rendered width. For now we assume the image fits 'cover' or 'contain'.
        # 'object-cover' might crop the image. 'object-contain' adds bars.
        # Let's assume the displayed image width matches the frame width for coordinate simplicity relative to the image element.
        # The FaceOverlay component handles the positioning.
        
        detected_known = False
        user_found = None
        valid_face_found = False
        
        # Update Overlay
        if results:
            # Show the primary face (biggest or first)
            # engine.py returns a list. We define logic to pick one if needed.
            res = results[0] 
            
            # Normalize coordinates for Frontend Overlay
            x, y, w, h = res["box"]
            
            # Check for zero dimensions to avoid division by zero
            if w_frame > 0 and h_frame > 0:
                x_pct = x / w_frame
                y_pct = y / h_frame
                w_pct = w / w_frame
                h_pct = h / h_frame
                
                # Create a copy/dict for the overlay to avoid mutating the original result which might be used elsewhere
                overlay_res = res.copy()
                overlay_res['box'] = (x_pct, y_pct, w_pct, h_pct)
                
                face_overlay.update(overlay_res, mirror=True)
            
            valid_face_found = True
            
            # Logic Processing
            if res.get("in_roi", False):
                if res["known"]:
                    if res['id'] == logic_state['last_user_id']:
                        logic_state['consecutive_hits'] += 1
                    else:
                        logic_state['consecutive_hits'] = 1
                        logic_state['last_user_id'] = res['id']
                    if logic_state['consecutive_hits'] >= 3:
                        detected_known = True
                        user_found = res
                else:
                    logic_state['consecutive_hits'] = 0
                    logic_state['last_user_id'] = None
        else:
            face_overlay.hide()
            logic_state['consecutive_hits'] = 0
            logic_state['last_user_id'] = None

        if logic_state['in_cooldown']: pass
        elif detected_known and user_found: trigger_access(user_found)
        else:
            # Feedback Label Logic
            if not results:
                feedback_label.text = "Aguardando rosto..."
                feedback_label.style('background-color: rgba(0,0,0,0.6);')
            else:
                if valid_face_found:
                     res = results[0]
                     if res['known']:
                         if logic_state['consecutive_hits'] > 0:
                             feedback_label.text = f"Identificando... {logic_state['consecutive_hits']}/3"
                             feedback_label.style('background-color: var(--primary);')
                     else:
                         feedback_label.text = "Rosto Desconhecido"
                         feedback_label.style('background-color: var(--error);')
                
                     if not res.get("in_roi", False):
                         feedback_label.text = "Centralize o Rosto"
                         feedback_label.style('background-color: var(--warning); color: black;')
                    

        # Send clean frame (no OpenCV drawing)
        _, buffer = cv2.imencode('.jpg', display_frame)
        video_image.set_source(f'data:image/jpeg;base64,{base64.b64encode(buffer).decode("utf-8")}')

    ui.timer(0.05, loop)
