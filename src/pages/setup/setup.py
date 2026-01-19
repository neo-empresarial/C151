from nicegui import ui
import cv2
import base64
from src.services.services import camera_manager
from . import functions as f
from .components import form, camera

def setup_page():
    with ui.column().classes('w-full h-screen items-center justify-center'):
        with ui.card().classes('w11-card w-[500px] p-8'):
            name_input, pin_input = form.render_inputs()
            cam_view = camera.render_view()
            
            capture_state = {
                'frame': None,
                'confirmed': False,
                'paused': False
            }

            async def cam_loop():
                if capture_state['paused']: return
                ret, frame = camera_manager.read()
                if ret:
                    capture_state['frame'] = frame.copy()
                    flipped_frame = cv2.flip(frame, 1)
                    _, buffer = cv2.imencode('.jpg', flipped_frame)
                    cam_view.set_source(f'data:image/jpeg;base64,{base64.b64encode(buffer).decode("utf-8")}')
            
            ui.timer(0.05, cam_loop)

            def capture_photo():
                if capture_state['frame'] is not None:
                    capture_state['paused'] = True
                    capture_btn.set_visibility(False)
                    confirm_row.set_visibility(True)
                    ui.notify('Foto capturada. Confirme se ficou boa.', type='info')

            def retake_photo():
                capture_state['paused'] = False
                capture_state['confirmed'] = False
                capture_btn.set_visibility(True)
                confirm_row.set_visibility(False)

            def confirm_photo():
                capture_state['confirmed'] = True
                ui.notify('Foto confirmada!', type='positive')

            with ui.row().classes('w-full justify-center mb-4'):
                capture_btn = ui.button('Capturar Foto', icon='camera_alt', on_click=capture_photo).classes('w-full w11-btn')
                
            with ui.row().classes('w-full gap-2') as confirm_row:
                ui.button('Tentar Novamente', icon='refresh', on_click=retake_photo).classes('flex-1 w11-btn')
                ui.button('Confirmar', icon='check', on_click=confirm_photo).classes('flex-1 w11-btn bg-green-600 text-white')
            
            confirm_row.set_visibility(False)

            async def create_admin():
                if not name_input.value or not pin_input.value:
                    ui.notify('Preencha tudo', type='negative'); return
                if not capture_state['confirmed'] or capture_state['frame'] is None:
                    ui.notify('Por favor, capture e confirme a foto.', type='warning'); return
                try:
                    await f.create_admin_user(name_input.value, pin_input.value, capture_state['frame'])
                    ui.navigate.to('/')
                except Exception as e:
                    ui.notify(f'Erro na foto: {e}', type='negative')

            ui.button('Criar Sistema', on_click=create_admin).classes('w-full w11-btn bg-blue-600 text-white')
