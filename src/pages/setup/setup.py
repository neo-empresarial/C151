from nicegui import ui
import cv2
import base64
from src.services.services import camera_manager
from src.common import theme
from . import functions as f
from .components import form, camera

def setup_page():
    with ui.column().classes('w-full h-screen items-center justify-center'):
        theme.render_theme_toggle_button()
        with ui.card().classes('w11-card w-[500px] p-8'):
            name_input, pin_input = form.render_inputs()
            cam_view = camera.render_view()
            
            capture_state = {
                'frame': None,
                'confirmed': False,
                'paused': False
            }

            with ui.dialog().props('persistent maximized transition-show=slide-up transition-hide=slide-down') as loading_dialog:
                with ui.card().classes('w-full h-full items-center justify-center bg-gray-900/90 text-white'):
                    with ui.column().classes('items-center gap-6'):
                        ui.spinner('rings', size='6rem', color='blue-400').classes('thickness-4')
                        with ui.column().classes('items-center gap-2'):
                            ui.label('Configurando seu Sistema').classes('text-3xl font-bold tracking-wide animate-pulse')
                            ui.label('Inicializando banco de dados e credenciais...').classes('text-lg text-gray-400')

            with ui.dialog().props('persistent maximized transition-show=scale transition-hide=scale') as success_dialog:
                with ui.card().classes('w-full h-full items-center justify-center bg-gradient-to-br from-green-900 to-emerald-900 text-white'):
                    with ui.column().classes('items-center gap-6 animate-bounce'):
                        ui.icon('check_circle', size='8rem', color='green-400').classes('filter drop-shadow-lg')
                        ui.label('Sistema Criado com Sucesso!').classes('text-4xl font-bold tracking-wider')
                    ui.label('Redirecionando para o login...').classes('mt-8 text-xl text-green-200 animate-pulse')

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
                    cam_view.classes('ring-4 ring-blue-400')
                    ui.notify('Revise sua foto.', type='info')

            def retake_photo():
                capture_state['paused'] = False
                capture_state['confirmed'] = False
                capture_btn.set_visibility(True)
                confirm_row.set_visibility(False)
                cam_view.classes(remove='ring-4 ring-blue-400 ring-green-500 opacity-60')

            def confirm_photo():
                capture_state['confirmed'] = True
                cam_view.classes(remove='ring-blue-400', add='ring-4 ring-green-500 opacity-60')
                ui.notify('Foto Confirmada!', type='positive', icon='check')

            with ui.row().classes('w-full justify-center mb-4'):
                capture_btn = ui.button('Capturar Foto', icon='camera_alt', on_click=capture_photo).classes('w-full text-lg bg-slate-800 text-white hover:bg-slate-700 shadow-lg py-2')
                
            with ui.row().classes('w-full gap-4') as confirm_row:
                ui.button('Tentar Novamente', icon='refresh', on_click=retake_photo).classes('flex-1 text-base bg-red-500 text-white hover:bg-red-600 shadow-md py-2').props('rounded no-caps')
                ui.button('Confirmar', icon='check', on_click=confirm_photo).classes('flex-1 text-base bg-green-500 text-white hover:bg-green-600 shadow-md py-2').props('rounded no-caps')
            
            confirm_row.set_visibility(False)

            async def create_admin():
                if not name_input.value or not pin_input.value:
                    ui.notify('Preencha o Nome e o PIN.', type='negative'); return
                if not capture_state['confirmed'] or capture_state['frame'] is None:
                    ui.notify('Por favor, capture e CONFIRME a foto.', type='warning'); return
                
                loading_dialog.open()
                try:
                    await f.create_admin_user(name_input.value, pin_input.value, capture_state['frame'])
                    loading_dialog.close()
                    success_dialog.open()
                    ui.timer(2.0, lambda: ui.navigate.to('/'), once=True)
                except Exception as e:
                    loading_dialog.close()
                    ui.notify(f'Erro ao criar admin: {str(e)}', type='negative', multi_line=True)

            ui.button('Criar Sistema', on_click=create_admin).classes('w-full h-14 text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-700 hover:to-indigo-700 shadow-xl mt-6 rounded-xl transform transition-all hover:scale-[1.02]')
