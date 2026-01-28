from nicegui import ui
import cv2
import base64
from src.services.services import camera_manager
from src.common.state import state
from src.common import theme
from src.common.styles import Colors
from . import functions as f
from .components import header, camera
from .components.pin_dialog import PinDialog, render_trigger_button
from src.language.manager import language_manager as lm

from src.common.config import db_config

DEFAULT_MIN_FACE_WIDTH = 0.15
DEFAULT_REQUIRED_HITS = 1
DEFAULT_MAX_OFFSET = 0.15

def login_page():
    face_config = db_config.config.get('face_tech', {})
    REQUIRED_HITS = face_config.get('required_hits', DEFAULT_REQUIRED_HITS)
    MIN_FACE_WIDTH = face_config.get('min_face_width', DEFAULT_MIN_FACE_WIDTH)
    MAX_OFFSET = face_config.get('max_offset', DEFAULT_MAX_OFFSET)

    print(f"DEBUG: login_page loaded. REQUIRED_HITS = {REQUIRED_HITS}")
    f.resume_engine()
    if not f.check_users_exist():
        ui.navigate.to('/setup')
        return
    state.current_user = None
    state.is_admin = False

    logic_state = {'consecutive_hits': 0, 'last_user_id': None, 'in_cooldown': False, 'last_timestamp': 0, 'matched_user_name': ''}

    def reset_state():
        state.current_user = None
        state.is_admin = False

    def finalize_access(user):
        state.current_user = user
        if user.get('access_level') == 'Admin':
            state.is_admin = True
            ui.notify(lm.t('admin_identified'), type='positive')
        else:
            ui.notify(lm.t('access_granted'), type='positive')
            ui.notify(f"{user.get('name')}", type='positive')
            ui.timer(3.0, lambda: reset_state(), once=True)

    def trigger_access(user):
        logic_state['in_cooldown'] = True
        logic_state['matched_user_name'] = user.get('name', '')
        def on_timeout():
            finalize_access(user)
            logic_state['in_cooldown'] = False
            logic_state['consecutive_hits'] = 0
            logic_state['last_timestamp'] = 0
            logic_state['last_user_id'] = None
        ui.timer(2.0, on_timeout, once=True)

    pin_dialog = PinDialog(on_success=trigger_access)
    
    ui.context.client.on_disconnect(lambda: f.pause_engine())

    async def safe_back():
        f.pause_engine()
        await ui.run_javascript('window.location.href = "/"')

    with ui.column().classes('w-full h-screen p-0 relative bg-surface'):
        theme.render_theme_toggle_button()
        theme.render_window_controls()
        
        header.render(on_pin_click=None, on_back=safe_back)
        
        with ui.column().classes('w-full flex-grow items-center justify-center p-2 gap-4'):
            with ui.card().classes('w-full max-w-[80vw] max-h-[70vh] aspect-video rounded-3xl overflow-hidden shadow-2xl relative bg-transparent'):
                 video_image, feedback_label, face_overlay = camera.render_view()

            ui.button(lm.t('enter_with_pin'), on_click=lambda: pin_dialog.open()).classes('w11-btn bg-surface border border-white/10 text-primary px-8 py-3 rounded-xl hover:bg-white/5 backdrop-blur-md transition-all shadow-lg text-lg tracking-wide')
            
        ui.label(lm.t('demo_footer')).classes('absolute bottom-4 left-6 opacity-40 text-white')

    async def loop():
        if not ui.context.client.has_socket_connection:
             return
        
        ret, frame = camera_manager.read()
        if not ret:
            face_overlay.set_state(lm.t('camera_disconnected'), 'var(--error)')
            return
            
        display_frame = cv2.flip(frame, 1)
        _, buffer = cv2.imencode('.jpg', display_frame)
        video_image.set_source(f'data:image/jpeg;base64,{base64.b64encode(buffer).decode("utf-8")}')
        
        if logic_state['in_cooldown']:
             user_name = logic_state.get('matched_user_name', '')
             face_overlay.set_state(lm.t('access_granted'), Colors.SUCCESS, subtext=user_name)
             return

        f.update_engine_frame(frame)
        results = f.get_engine_results()
        
        h_frame, w_frame, _ = display_frame.shape
        
        if results:
            res = results[0] 
            x, y, w, h = res["box"]
            
            if w_frame > 0 and h_frame > 0:
                x_pct = x / w_frame
                y_pct = y / h_frame
                w_pct = w / w_frame
                h_pct = h / h_frame
                
                overlay_res = res.copy()
                overlay_res['box'] = (x_pct, y_pct, w_pct, h_pct)
                
                final_text = lm.t('position_face_center')
                final_color = Colors.WARNING 
                
                
                cx = x_pct + w_pct / 2
                cy = y_pct + h_pct / 2
                diff_x = cx - 0.5
                diff_y = cy - 0.5
                dist_from_center = (diff_x**2 + diff_y**2)**0.5
                
                if dist_from_center > MAX_OFFSET:
                     final_text = lm.t('position_face_center')
                     final_color = Colors.WARNING
                     logic_state['consecutive_hits'] = 0
                     logic_state['last_timestamp'] = 0

                elif w_pct < MIN_FACE_WIDTH:
                     final_text = lm.t('move_face_closer')
                     final_color = Colors.WARNING
                     logic_state['consecutive_hits'] = 0
                     logic_state['last_timestamp'] = 0
                     
                elif not res.get('is_real', True):
                     final_text = lm.t('fake_face_detected')
                     final_color = Colors.ERROR
                     logic_state['consecutive_hits'] = 0
                     logic_state['last_timestamp'] = 0
                     
                else: 
                     if res.get('known'):
                         current_ts = res.get('result_timestamp', 0)
                         if current_ts > logic_state['last_timestamp']:
                             if res['id'] == logic_state['last_user_id']:
                                 logic_state['consecutive_hits'] += 1
                             else:
                                 logic_state['consecutive_hits'] = 1
                                 logic_state['last_user_id'] = res['id']
                             logic_state['last_timestamp'] = current_ts
                         
                         if logic_state['consecutive_hits'] >= REQUIRED_HITS:
                             trigger_access(res)
                             final_text = lm.t('hello', name=res.get('name'))
                             final_color = Colors.SUCCESS
                         else:
                             pct = int((logic_state['consecutive_hits'] / REQUIRED_HITS) * 100)
                             final_text = lm.t('identifying', pct=pct)
                             final_color = Colors.INFO 
                     else:
                         if res.get('in_roi', False):
                             final_text = lm.t('not_recognized')
                             final_color = Colors.ERROR
                         else:
                             final_text = lm.t('position_face_center')
                             final_color = Colors.WARNING
                         
                         logic_state['consecutive_hits'] = 0
                         logic_state['last_timestamp'] = 0
                         logic_state['last_user_id'] = None

                face_overlay.update(overlay_res, text=final_text, color=final_color, mirror=True)
                
        else:
            face_overlay.update(None, text=lm.t('position_face_center'), color=Colors.WARNING) 
            logic_state['consecutive_hits'] = 0
            logic_state['last_timestamp'] = 0
            logic_state['last_user_id'] = None

    ui.timer(0.05, loop)
