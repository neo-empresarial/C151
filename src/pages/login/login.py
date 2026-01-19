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
    
    with ui.column().classes('w-full h-screen items-center justify-center bg-gray-100 p-4 relative'):
        ui.label("Demo Version | © Fundação Certi 2026").classes('absolute bottom-4 text-gray-500 text-sm')

        with ui.card().classes('w11-card w-full max-w-[1000px] h-[700px] p-0 flex flex-col overflow-hidden shadow-lg'):
            header.render()
            video_image, feedback_label = camera.render_view()
            render_trigger_button(lambda: pin_dialog.open())

    def finalize_access(user):
        state.current_user = user
        feedback_label.text = f"Bem-vindo, {user['name']}!"
        feedback_label.classes(remove='bg-black/60 bg-green-600', add='bg-green-600')
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
        feedback_label.classes(remove='bg-green-600', add='bg-black/60')

    logic_state = {'consecutive_hits': 0, 'last_user_id': None, 'in_cooldown': False}

    def trigger_access(user):
        logic_state['in_cooldown'] = True
        feedback_label.text = "ACESSO PERMITIDO"
        feedback_label.classes(remove='bg-black/60 bg-blue-600 bg-red-600 bg-yellow-600', add='bg-green-600')
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
            feedback_label.classes(remove='bg-green-600', add='bg-red-600')
            return

        if logic_state['in_cooldown']:
            video_image.set_source(f'data:image/jpeg;base64,{f.frame_to_b64(frame)}')
            return

        f.update_engine_frame(frame)
        results = f.get_engine_results()
        display_frame = cv2.flip(frame, 1)
        h_frame, w_frame, _ = display_frame.shape

        detected_known = False
        user_found = None
        valid_face_found = False

        for res in results:
            display_frame = f.draw_face_box(display_frame, res, w_frame)
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
                    valid_face_found = True
                else:
                    logic_state['consecutive_hits'] = 0
                    logic_state['last_user_id'] = None
                    valid_face_found = True
        
        if not valid_face_found:
             logic_state['consecutive_hits'] = 0
             logic_state['last_user_id'] = None

        if logic_state['in_cooldown']: pass
        elif detected_known and user_found: trigger_access(user_found)
        else:
            if not results:
                feedback_label.text = "Aguardando rosto..."
                feedback_label.classes(remove='bg-blue-600 bg-yellow-600 bg-red-600 bg-green-600', add='bg-black/60')
            else:
                if valid_face_found:
                     if logic_state['consecutive_hits'] > 0:
                         feedback_label.text = f"Identificando... {logic_state['consecutive_hits']}/3"
                         feedback_label.classes(remove='bg-black/60', add='bg-blue-600')
                     else:
                         feedback_label.text = "Rosto Desconhecido"
                         feedback_label.classes(remove='bg-black/60', add='bg-red-600')
                else:
                     feedback_label.text = "Centralize o Rosto"
                     feedback_label.classes(remove='bg-black/60 bg-red-600', add='bg-yellow-600')

        flipped_frame = display_frame
        _, buffer = cv2.imencode('.jpg', flipped_frame)
        video_image.set_source(f'data:image/jpeg;base64,{base64.b64encode(buffer).decode("utf-8")}')

    ui.timer(0.05, loop)
