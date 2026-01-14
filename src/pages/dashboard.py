
import base64
import cv2
from nicegui import ui
from deepface import DeepFace

from src.services import camera_manager, db_manager, engine
from src.common.state import state

def dashboard_page():
    # if not state.is_admin:
    #     ui.navigate.to('/')
    #     return

    with ui.column().classes('w-full h-screen bg-gray-100 p-8'):
        with ui.row().classes('w-full justify-between items-center mb-6'):
            ui.label('Painel Administrativo').classes('text-2xl font-bold text-gray-800')
            ui.button('Sair', on_click=lambda: ui.navigate.to('/')).classes('w11-btn bg-gray-200 text-black')

        # Users List
        users_card = ui.card().classes('w11-card w-full p-4')
        with users_card:
            ui.label('Usuários Cadastrados').classes('text-lg font-semibold mb-4')
            
            # Grid/Table
            users = db_manager.get_users()
            
            with ui.grid(columns=4).classes('w-full gap-4'):
                ui.label('Nome').classes('font-bold text-gray-500')
                ui.label('Nível').classes('font-bold text-gray-500')
                ui.label('ID').classes('font-bold text-gray-500')
                ui.label('Ações').classes('font-bold text-gray-500')
                
                for u in users:
                    ui.label(u['name'])
                    ui.label(u['access_level'])
                    ui.label(u['id'][:8] + '...')
                    with ui.row():
                        ui.button(icon='edit', on_click=lambda _, user=u: open_edit_dialog(user)).props('flat dense')
                        ui.button(icon='delete', color='negative', on_click=lambda _, uid=u['id']: delete_user(uid)).props('flat dense')

        # Add User Button
        ui.button('Adicionar Usuário', on_click=lambda: add_user_dialog.open()).classes('w11-btn bg-blue-600 text-white mt-4')

    async def delete_user(uid):
        db_manager.delete_user(uid)
        ui.notify('Usuário removido')
        ui.navigate.reload()

    # --- Edit User Dialog ---
    edit_dialog = ui.dialog()
    with edit_dialog, ui.card().classes('w11-card w-[500px] p-6'):
        ui.label('Editar Usuário').classes('text-xl font-bold mb-4')
        
        edit_name = ui.input('Nome').classes('w-full')
        edit_pin = ui.input('PIN').classes('w-full')
        edit_access = ui.select(['Admin', 'Funcionario', 'Visitante'], label='Acesso').classes('w-full')
        
        current_edit_id = [None] # stored in closure

        # Edit Photo Logic
        edit_capture_state = {'frame': None, 'confirmed': False, 'paused': False}
        
        with ui.expansion('Atualizar Foto', icon='face').classes('w-full mb-4') as photo_exp:
            edit_cam_view = ui.interactive_image().classes('w-full h-[250px] bg-black rounded')
            
            async def edit_cam_loop():
                if not edit_dialog.value or not photo_exp.value: return
                if edit_capture_state['paused']: return
                
                ret, frame = camera_manager.read()
                if ret:
                    edit_capture_state['frame'] = frame.copy()
                    _, buffer = cv2.imencode('.jpg', frame)
                    edit_cam_view.set_source(f'data:image/jpeg;base64,{base64.b64encode(buffer).decode("utf-8")}')
            
            edit_cam_timer = ui.timer(0.05, edit_cam_loop, active=False)
            photo_exp.on_value_change(lambda e: edit_cam_timer.activate() if e.value else edit_cam_timer.deactivate())

            def edit_reset():
                edit_capture_state['paused'] = False
                edit_capture_state['confirmed'] = False
                edit_capture_state['frame'] = None
                e_capture_btn.visible = True
                e_confirm_row.visible = False

            def edit_capture():
                if edit_capture_state['frame'] is not None:
                    edit_capture_state['paused'] = True
                    e_capture_btn.visible = False
                    e_confirm_row.visible = True

            def edit_confirm():
                edit_capture_state['confirmed'] = True
                ui.notify('Nova foto confirmada!', type='positive')

            with ui.row().classes('w-full justify-center mt-2'):
                e_capture_btn = ui.button('Capturar', icon='camera_alt', on_click=edit_capture).classes('w11-btn')
                with ui.row().classes('gap-2 hidden') as e_confirm_row:
                     ui.button('Retirar', icon='refresh', color='warning', on_click=edit_reset)
                     ui.button('Confirmar', icon='check', color='positive', on_click=edit_confirm)

        def save_edit():
            if not edit_name.value or not edit_pin.value:
                ui.notify('Preencha tudo', type='negative'); return
            
            updates = {
                'name': edit_name.value,
                'pin': edit_pin.value,
                'access_level': edit_access.value
            }

            # Check if photo update required
            if edit_capture_state['confirmed'] and edit_capture_state['frame'] is not None:
                try:
                     ui.notify('Atualizando biometria...', type='info')
                     embedding_objs = DeepFace.represent(
                        img_path=edit_capture_state['frame'],
                        model_name="Facenet",
                        detector_backend="opencv",
                        enforce_detection=True
                    )
                     updates['embedding'] = embedding_objs[0]['embedding']
                     updates['frame'] = edit_capture_state['frame']
                except Exception as e:
                    ui.notify(f'Erro na foto: {e}', type='negative')
                    return

            db_manager.update_user(current_edit_id[0], **updates)
            
            if 'embedding' in updates:
                engine.load_model()
                
            ui.notify('Usuário atualizado')
            edit_dialog.close()
            ui.navigate.reload()

        with ui.row().classes('w-full justify-end mt-4 gap-2'):
            ui.button('Cancelar', on_click=edit_dialog.close).props('flat')
            ui.button('Salvar', on_click=save_edit).classes('w11-btn bg-blue-600 text-white')

    def open_edit_dialog(user):
        current_edit_id[0] = user['id']
        edit_name.value = user['name']
        edit_pin.value = user['pin']
        edit_access.value = user['access_level']
        edit_dialog.open()

    # --- Add User Dialog ---
    add_user_dialog = ui.dialog().props('maximized')
    with add_user_dialog, ui.card().classes('w-full h-full p-8 items-center justify-center'):
        ui.label('Novo Usuário').classes('text-2xl font-bold mb-6')
        
        with ui.row().classes('w-full max-w-4xl gap-8'):
            # Form
            with ui.column().classes('flex-1 gap-4'):
                name_input = ui.input('Nome Completo').classes('w-full')
                pin_setup = ui.input('PIN (Numérico)').classes('w-full')
                access_select = ui.select(['Admin', 'Funcionario', 'Visitante'], value='Visitante', label='Nível de Acesso').classes('w-full')
            
            # Camera Capture
            with ui.column().classes('flex-1 h-[400px] bg-black rounded-lg overflow-hidden relative'):
                capture_img = ui.interactive_image().classes('w-full h-full object-cover')
                
    
        # Logic for Capture
        capture_state = {
            'frame': None,
            'confirmed': False,
            'paused': False
        }
        
        async def capture_loop():
            if not add_user_dialog.value: return # Don't run if closed
            if capture_state['paused']: return

            ret, frame = camera_manager.read()
            if ret:
                capture_state['frame'] = frame.copy()
                _, buffer = cv2.imencode('.jpg', frame)
                capture_img.set_source(f'data:image/jpeg;base64,{base64.b64encode(buffer).decode("utf-8")}')
        
        capture_timer = ui.timer(0.05, capture_loop, active=False)
        
        def reset_capture_state(e):
            if e.value:
                capture_timer.activate()
                # reset
                capture_state['paused'] = False
                capture_state['confirmed'] = False
                capture_state['frame'] = None
                capture_btn.visible = True
                confirm_row.visible = False
            else:
                capture_timer.deactivate()

        add_user_dialog.on_value_change(reset_capture_state)

        def do_capture():
            if capture_state['frame'] is not None:
                capture_state['paused'] = True
                capture_btn.visible = False
                confirm_row.visible = True
        
        def do_retake():
            capture_state['paused'] = False
            capture_state['confirmed'] = False
            capture_btn.visible = True
            confirm_row.visible = False
            
        def do_confirm():
            capture_state['confirmed'] = True
            ui.notify('Foto confirmada', type='positive')

        # Capture Buttons
        with ui.column().classes('mt-4 w-full items-center'):
            capture_btn = ui.button('Capturar Foto', icon='camera_alt', on_click=do_capture).classes('w11-btn w-full max-w-md')
            with ui.row().classes('gap-4 hidden') as confirm_row:
                ui.button('Tentar Novamente', icon='refresh', color='warning', on_click=do_retake)
                ui.button('Confirmar Foto', icon='check', color='positive', on_click=do_confirm)

        async def save_user():
            if not name_input.value or not pin_setup.value:
                ui.notify('Preencha todos os campos', type='negative')
                return
            if not capture_state['confirmed'] or capture_state['frame'] is None:
                ui.notify('Você deve capturar e CONFIRMAR a foto.', type='warning')
                return
            
            ui.notify('Processando Face... Aguarde.', type='info')
            
            # Use the confirmed frame
            final_frame = capture_state['frame']
            
            try:
                embedding_objs = DeepFace.represent(
                    img_path=final_frame,
                    model_name="Facenet",
                    detector_backend="opencv",
                    enforce_detection=True
                )
                
                if not embedding_objs:
                     ui.notify('Nenhum rosto detectado!', type='warning')
                     return
                
                embedding = embedding_objs[0]['embedding']
                
                success, msg = db_manager.create_user(
                    name=name_input.value,
                    frame=final_frame,
                    embedding=embedding,
                    pin=pin_setup.value,
                    access_level=access_select.value
                )
                
                if success:
                    ui.notify(f'Usuário {name_input.value} criado!')
                    engine.load_model()
                    add_user_dialog.close()
                    ui.navigate.reload()
                else:
                    ui.notify(f'Erro: {msg}', type='negative')
                    
            except Exception as e:
                ui.notify(f'Erro ao processar face: {str(e)}', type='negative')

        with ui.row().classes('mt-8 gap-4'):
            ui.button('Cancelar', on_click=add_user_dialog.close).props('flat')
            ui.button('Salvar Usuário', on_click=save_user).classes('w11-btn bg-blue-600 text-white')
