import base64
import cv2
import time
from nicegui import ui

from src.services.services import camera_manager, db_manager, engine
from src.common.state import state

def login_page():
    users = db_manager.get_users()
    if not users:
        ui.navigate.to('/setup')
        return
    state.current_user = None
    state.is_admin = False
    with ui.column().classes('w-full h-screen items-center justify-center bg-gray-100 p-4 relative'):
        
        ui.label("Demo Version | © Fundação Certi 2026").classes('absolute bottom-4 text-gray-500 text-sm')

        with ui.card().classes('w11-card w-full max-w-[1000px] h-[700px] p-0 flex flex-col overflow-hidden shadow-lg'):
            with ui.row().classes('w-full h-[60px] bg-white border-b border-gray-200 items-center px-6 justify-between shrink-0'):
                with ui.row().classes('items-center gap-4'):
                     ui.image('src/public/images/certi/logo-certi.png').classes('h-12 w-auto object-contain')
                     ui.label('Reconhecimento Facial').classes('text-xl font-semibold text-gray-800')
                with ui.row().classes('gap-2'):
                    ui.button(icon='home', on_click=lambda: ui.navigate.to('/')).props('flat round dense')
            with ui.column().classes('w-full h-[500px] bg-black items-center justify-center relative overflow-hidden'):
                video_image = ui.interactive_image().classes('w-full h-full object-cover')
                ui.element('div').classes('absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[220px] h-[320px] border-2 border-white/50 rounded-[50%] pointer-events-none shadow-[0_0_0_9999px_rgba(0,0,0,0.5)]')
                ui.element('div').classes('absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[220px] h-[320px] border-2 border-white/50 rounded-[50%] pointer-events-none shadow-[0_0_0_9999px_rgba(0,0,0,0.5)]')
                feedback_label = ui.label('Inicializando...').classes('absolute bottom-4 left-1/2 transform -translate-x-1/2 bg-black/60 text-white px-6 py-2 rounded-full text-lg font-medium backdrop-blur-sm z-10')
            with ui.row().classes('w-full h-[80px] bg-white border-t border-gray-200 items-center justify-center px-6 shrink-0'):
                 ui.button('Entrar com PIN', on_click=lambda: pin_dialog.open()).classes('w11-btn bg-gray-100 text-gray-800 border border-gray-300 hover:bg-gray-200')
    def go_dashboard():
        ui.navigate.to('/dashboard')

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

    logic_state = {
        'consecutive_hits': 0,
        'last_user_id': None,
        'in_cooldown': False
    }

    def trigger_access(user):
        logic_state['in_cooldown'] = True
        feedback_label.text = "ACESSO PERMITIDO"
        feedback_label.classes(remove='bg-black/60 bg-blue-600 bg-red-600 bg-yellow-600', add='bg-green-600')
        
        def on_timeout():
            finalize_access(user)
            logic_state['in_cooldown'] = False
            logic_state['consecutive_hits'] = 0
            
        ui.timer(2.0, on_timeout, once=True)

    pin_dialog = ui.dialog()
    with pin_dialog, ui.card().classes('w11-card w-[320px] items-center p-6'):
        ui.label('Digite o PIN').classes('text-xl font-semibold mb-6')
        pin_input = ui.input(password=True).classes('w-full mb-6 text-center text-2xl tracking-widest')
        
        def verify_pin():
            user = db_manager.get_user_by_pin(pin_input.value)
            if user:
                pin_dialog.close()
                trigger_access(user)
            else:
                ui.notify('PIN Inválido', type='negative')
                pin_input.value = ''

        with ui.grid(columns=3).classes('gap-3 w-full'):
            for i in range(1, 10):
                ui.button(str(i), on_click=lambda x=i: pin_input.set_value(pin_input.value + str(x))).classes('w11-btn text-lg h-12 bg-gray-50')
            ui.button('C', on_click=lambda: pin_input.set_value('')).classes('w11-btn text-lg h-12 bg-red-50 text-red-600')
            ui.button('0', on_click=lambda: pin_input.set_value(pin_input.value + '0')).classes('w11-btn text-lg h-12 bg-gray-50')
            ui.button('OK', on_click=verify_pin).classes('w11-btn text-lg h-12 bg-blue-600 text-white col-span-3')

    async def loop():
        if state.current_user or logic_state['in_cooldown']:
            pass
            
        ret, frame = camera_manager.read()
        
        if not ret:
            feedback_label.text = "Câmera desconectada"
            feedback_label.classes(remove='bg-green-600', add='bg-red-600')
            return

        if logic_state['in_cooldown']:
            _, buffer = cv2.imencode('.jpg', frame)
            video_image.set_source(f'data:image/jpeg;base64,{base64.b64encode(buffer).decode("utf-8")}')
            return

        engine.update_frame(frame)
        results = engine.get_results()
        
        display_frame = frame.copy()
        
        detected_known = False
        user_found = None
        
        valid_face_found = False

        for res in results:
            x, y, w, h = res["box"]
            known = res["known"]
            name = res.get("name", "Desconhecido")
            in_roi = res.get("in_roi", False)
            
            color = (100, 100, 100)
            if in_roi:
                if known:
                    color = (0, 255, 0)
                else:
                    color = (0, 0, 255)
            else:
                color = (0, 255, 255)
            
            cv2.rectangle(display_frame, (x, y), (x+w, y+h), color, 2)
            
            if not in_roi:
                 cv2.putText(display_frame, "Centralize", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            else:
                 cv2.putText(display_frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

            if in_roi:
                if known:
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

        if logic_state['in_cooldown']:
             pass
        elif detected_known and user_found:
             trigger_access(user_found)

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

        _, buffer = cv2.imencode('.jpg', display_frame)
        video_image.set_source(f'data:image/jpeg;base64,{base64.b64encode(buffer).decode("utf-8")}')

    ui.timer(0.05, loop)
