
import base64
import cv2
from nicegui import ui
from deepface import DeepFace

from src.services.services import camera_manager, db_manager, engine

def setup_page():
    with ui.column().classes('w-full h-screen items-center justify-center bg-gray-50'):
        with ui.card().classes('w11-card w-[500px] p-8'):
            ui.label('Configuração Inicial').classes('text-2xl font-bold mb-2')
            ui.label('Nenhum usuário encontrado. Crie o Administrador.').classes('text-gray-600 mb-6')
            
            name_input = ui.input('Nome do Admin').classes('w-full mb-4')
            pin_input = ui.input('PIN do Admin').classes('w-full mb-6')
            
            ui.label('Posicione-se para foto:').classes('font-bold mb-2')
            with ui.element('div').classes('relative w-full h-[300px] mb-6 bg-black rounded overflow-hidden'):
                cam_view = ui.interactive_image().classes('w-full h-full object-cover')
                ui.element('div').classes('absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[180px] h-[260px] border-2 border-white/50 rounded-[50%] pointer-events-none shadow-[0_0_0_9999px_rgba(0,0,0,0.5)]')
            
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
            
            cam_timer = ui.timer(0.05, cam_loop)

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
                    embedding_objs = DeepFace.represent(
                        img_path=capture_state['frame'],
                        model_name="Facenet",
                        detector_backend="opencv",
                        enforce_detection=True
                    )
                    embedding = embedding_objs[0]['embedding']
                    
                    db_manager.create_user(
                        name=name_input.value, 
                        frame=capture_state['frame'],
                        embedding=embedding,
                        pin=pin_input.value, 
                        access_level="Admin"
                    )
                    engine.load_model()
                    ui.navigate.to('/')
                except Exception as e:
                    ui.notify(f'Erro na foto (rosto não detectado?): {e}', type='negative')

            ui.button('Criar Sistema', on_click=create_admin).classes('w-full w11-btn bg-blue-600 text-white')
