
import base64
import cv2
from nicegui import ui
from deepface import DeepFace

from src.services import camera_manager, db_manager, engine

def setup_page():
    # First Run Setup
    with ui.column().classes('w-full h-screen items-center justify-center bg-gray-50'):
        with ui.card().classes('w11-card w-[500px] p-8'):
            ui.label('Configuração Inicial').classes('text-2xl font-bold mb-2')
            ui.label('Nenhum usuário encontrado. Crie o Administrador.').classes('text-gray-600 mb-6')
            
            name_input = ui.input('Nome do Admin').classes('w-full mb-4')
            pin_input = ui.input('PIN do Admin').classes('w-full mb-6')
            
            ui.label('Posicione-se para foto:').classes('font-bold mb-2')
            cam_view = ui.interactive_image().classes('w-full h-[300px] bg-black rounded mb-6')
            
            # State for capture
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
                    _, buffer = cv2.imencode('.jpg', frame)
                    cam_view.set_source(f'data:image/jpeg;base64,{base64.b64encode(buffer).decode("utf-8")}')
            
            cam_timer = ui.timer(0.05, cam_loop)

            def capture_photo():
                if capture_state['frame'] is not None:
                    capture_state['paused'] = True
                    capture_btn.visible = False
                    confirm_row.visible = True
                    ui.notify('Foto capturada. Confirme se ficou boa.', type='info')

            def retake_photo():
                capture_state['paused'] = False
                capture_state['confirmed'] = False
                capture_btn.visible = True
                confirm_row.visible = False

            def confirm_photo():
                capture_state['confirmed'] = True
                ui.notify('Foto confirmada!', type='positive')

            # Buttons for capture logic
            with ui.row().classes('w-full justify-center mb-4'):
                capture_btn = ui.button('Capturar Foto', icon='camera_alt', on_click=capture_photo).classes('w-full w11-btn')
                
                with ui.row().classes('w-full gap-2 hidden') as confirm_row:
                    ui.button('Tentar Novamente', icon='refresh', color='warning', on_click=retake_photo).classes('flex-1')
                    ui.button('Confirmar', icon='check', color='positive', on_click=confirm_photo).classes('flex-1')

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
