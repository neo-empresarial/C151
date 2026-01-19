import base64
import cv2
import time
from nicegui import ui, run

from src.services.services import camera_manager, db_manager, engine
from src.common.state import state

def dashboard_page():
    with ui.column().classes('w-full h-screen bg-gray-100 p-8 relative'):
        
        ui.label("Demo Version | © Fundação Certi 2026").classes('absolute bottom-4 text-gray-400 text-xs')

        with ui.row().classes('w-full justify-between items-center mb-6'):
            with ui.row().classes('items-center gap-4'):
                ui.image('src/public/images/certi/logo-certi.png').classes('h-12 w-auto object-contain')
                ui.label('Painel Administrativo').classes('text-2xl font-bold text-gray-800')
            ui.button('Sair', on_click=lambda: ui.navigate.to('/')).classes('w11-btn bg-red-600 text-white')

        users_card = ui.card().classes('w11-card w-full p-4')
        with users_card:
            ui.label('Usuários Cadastrados').classes('text-lg font-semibold mb-4')
            
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

        ui.button('Adicionar Usuário', on_click=lambda: add_user_dialog.open()).classes('w11-btn bg-blue-600 text-white mt-4')

    async def delete_user(uid):
        db_manager.delete_user(uid)
        ui.notify('Usuário removido')
        ui.navigate.reload()

    edit_dialog = ui.dialog().props('maximized')
    with edit_dialog, ui.card().classes('w-full h-full p-8 overflow-hidden'):
        
        with ui.row().classes('w-full items-center justify-between mb-6'):
            ui.label('Editar Usuário').classes('text-2xl font-bold')
            ui.button(icon='close', on_click=edit_dialog.close).props('round dense flat')

        with ui.row().classes('w-full h-full flex-nowrap max-w-full gap-8'):
            
            # --- Left Column: User Data ---
            with ui.column().classes('w-1/3 min-w-[350px] h-full gap-6'):
                ui.label('Dados Pessoais').classes('text-xl font-semibold text-gray-600')
                
                with ui.card().classes('w-full p-6 gap-4'):
                    edit_name = ui.input('Nome Completo').classes('w-full')
                    edit_pin = ui.input('PIN de Acesso', password=True, password_toggle_button=True).classes('w-full')
                    edit_access = ui.select(['Admin', 'Funcionario', 'Visitante'], label='Nível de Acesso').classes('w-full')

                with ui.row().classes('w-full gap-4 mt-6'):
                    ui.button('Cancelar', on_click=edit_dialog.close).classes('flex-1').props('flat')
                    ui.button('Salvar', on_click=lambda: save_edit_info()).classes('flex-1 bg-blue-600 text-white')

            # --- Right Column: Photos & Biometrics ---
            with ui.column().classes('flex-1 h-full gap-4 overflow-hidden'):
                ui.label('Biometria e Fotos').classes('text-xl font-semibold text-gray-600')
                
                # Container for Gallery
                with ui.card().classes('w-full h-full p-6 flex flex-col gap-4 overflow-hidden'):
                    
                    with ui.row().classes('w-full justify-between items-center'):
                        ui.label('Fotos Cadastradas').classes('text-sm font-bold text-gray-400')
                        # Button opens the modal
                        add_photo_btn = ui.button('Adicionar Nova Foto', icon='add_a_photo', on_click=lambda: open_capture_dialog()).classes('px-4')
                    
                    # Gallery Grid
                    # Use standard flex wrap to allow items to size themselves
                    photos_container = ui.element('div').classes('w-full flex-1 overflow-y-auto p-2 bg-gray-50 rounded border border-gray-100 flex flex-wrap content-start gap-4 transition-all')

    # --- Capture Modal (Camera) ---
    capture_dialog = ui.dialog()
    with capture_dialog, ui.card().classes('w-[500px] p-0 overflow-hidden flex flex-col'):
        
        # Header
        with ui.row().classes('w-full bg-black p-2 justify-between items-center'):
            ui.label('Capturar Foto').classes('text-white font-bold ml-2')
            ui.button(icon='close', on_click=capture_dialog.close).props('round dense flat color=white')

        # Camera View
        with ui.element('div').classes('relative w-full h-[400px] bg-black overflow-hidden justify-center items-center'):
             edit_cam_view = ui.interactive_image().classes('w-full h-full object-cover')
             # Overlay
             ui.element('div').classes('absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[220px] h-[300px] border-2 border-white/50 rounded-[50%] pointer-events-none shadow-[0_0_0_9999px_rgba(0,0,0,0.5)]')
             
             # Capture Controls
             with ui.column().classes('absolute bottom-6 left-0 right-0 items-center gap-3 z-10 w-full'):
                  e_capture_btn = ui.button('Capturar', icon='camera_alt', on_click=lambda: edit_capture()).classes('w11-btn scale-125')
                  with ui.row().classes('gap-3 hidden') as e_confirm_row:
                     ui.button('Refazer', icon='refresh', color='white', on_click=lambda: edit_reset()).props('text-color=black')
                     ui.button('Salvar', icon='check', color='positive', on_click=lambda: edit_confirm_add())

    # --- Logic Variables ---
    current_edit_id = [None] 
    edit_capture_state = {'frame': None, 'confirmed': False, 'paused': False}

    def refresh_edit_gallery(user_id):
        photos_container.clear()
        user_photos = db_manager.get_user_photos(user_id)
        
        with photos_container:
            for photo in user_photos:
                # Individual Photo Card
                with ui.card().classes('p-2 flex flex-col gap-2 items-center bg-white shadow-sm hover:shadow-md transition-all'):
                    b64_img = base64.b64encode(photo['image_blob']).decode('utf-8')
                    # Fixed height, min-width to prevent collapse
                    ui.image(f'data:image/jpeg;base64,{b64_img}').style('height: 150px; width: auto; min-width: 100px; object-fit: contain;').classes('rounded border border-gray-200')
                    
                    # Explicit Delete Button
                    ui.button('Remover', icon='delete', color='negative', on_click=lambda _, pid=photo['id']: delete_photo(pid)).props('flat dense size=sm w-full')

    async def delete_photo(photo_id):
        success, msg = db_manager.delete_user_photo(photo_id)
        if success:
            ui.notify('Foto removida')
            refresh_edit_gallery(current_edit_id[0])
            await run.io_bound(engine.load_model)
        else:
            ui.notify(f'Erro: {msg}', type='negative')

    def open_capture_dialog():
        edit_reset()
        capture_dialog.open()
        edit_cam_timer.activate()

    # Handle dialog closing to stop camera
    def on_capture_close(e):
        if not e.value: # Closing
            edit_cam_timer.deactivate()
    capture_dialog.on_value_change(on_capture_close)

    async def edit_cam_loop():
        # Only run if capture dialog is open
        if not capture_dialog.value: return
        if edit_capture_state['paused']: return
        
        ret, frame = camera_manager.read()
        if ret:
            edit_capture_state['frame'] = frame.copy()
            flipped_frame = cv2.flip(frame, 1)
            _, buffer = cv2.imencode('.jpg', flipped_frame)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')
            edit_cam_view.set_source(f'data:image/jpeg;base64,{jpg_as_text}')
    
    edit_cam_timer = ui.timer(0.05, edit_cam_loop, active=False)

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

    async def edit_confirm_add():
        if edit_capture_state['frame'] is not None:
            n = ui.notify('Processando nova foto...', type='ongoing', timeout=0)
            try:
                engine.paused = True
                # Small yield to ensure UI updates
                await run.io_bound(lambda: time.sleep(0.01))
                
                embedding_objs = await run.io_bound(
                    engine.generate_embedding,
                    edit_capture_state['frame']
                )
                
                if embedding_objs:
                    emb = embedding_objs[0]['embedding']
                    success, _ = db_manager.add_user_photo(current_edit_id[0], edit_capture_state['frame'], emb)
                    if success:
                        ui.notify('Foto adicionada com sucesso!', type='positive')
                        refresh_edit_gallery(current_edit_id[0])
                        
                        # Reload model in background
                        await run.io_bound(engine.load_model)
                        
                        capture_dialog.close()
                    else:
                        ui.notify('Erro ao salvar foto no banco', type='negative')
                else:
                    ui.notify('Nenhum rosto detectado', type='warning')
                    edit_reset()
                    
            except Exception as e:
                ui.notify(f'Erro ao processar: {str(e)}', type='negative')
                print(f"Error in edit_confirm_add: {e}")
            finally:
                engine.paused = False
                if n:
                    n.dismiss()

    async def save_edit_info():
        if not edit_name.value or not edit_pin.value:
            ui.notify('Preencha nome e PIN', type='negative'); return
        
        updates = {
            'name': edit_name.value,
            'pin': edit_pin.value,
            'access_level': edit_access.value
        }

        success, msg = db_manager.update_user(current_edit_id[0], **updates)
        if success:
             ui.notify('Dados atualizados')
             engine.load_model() 
             edit_dialog.close()
             ui.navigate.reload()
        else:
             ui.notify(f'Erro: {msg}')

    def open_edit_dialog(user):
        current_edit_id[0] = user['id']
        edit_name.value = user['name']
        edit_pin.value = user['pin']
        edit_access.value = user['access_level']
        
        refresh_edit_gallery(user['id'])

        edit_capture_state['frame'] = None
        edit_capture_state['confirmed'] = False
        edit_capture_state['paused'] = False
        
        edit_cam_timer.deactivate()

        edit_dialog.open()

    add_user_dialog = ui.dialog().props('maximized')
    with add_user_dialog, ui.card().classes('w-full h-full p-8 flex flex-col items-center'):
        ui.label('Novo Usuário').classes('text-2xl font-bold mb-6')
        
        with ui.row().classes('w-full max-w-6xl gap-8 h-full'):
            # Left Column: Inputs
            with ui.column().classes('w-1/3 gap-4'):
                name_input = ui.input('Nome Completo').classes('w-full')
                pin_setup = ui.input('PIN (Numérico)', password=True, password_toggle_button=True).classes('w-full')
                access_select = ui.select(['Admin', 'Funcionario', 'Visitante'], value='Visitante', label='Nível de Acesso').classes('w-full')
                
                ui.separator().classes('my-4')
                ui.label('Fotos Capturadas:').classes('font-bold')
                
                captured_photos = [] 
                capture_gallery = ui.grid(columns=3).classes('w-full gap-2')
                
                def update_capture_gallery():
                    capture_gallery.clear()
                    with capture_gallery:
                        for idx, (frame, _) in enumerate(captured_photos):
                            with ui.card().classes('p-0 relative group'):
                                _, buffer = cv2.imencode('.jpg', frame)
                                b64 = base64.b64encode(buffer).decode('utf-8')
                                ui.image(f'data:image/jpeg;base64,{b64}').classes('w-full h-20 object-cover')
                                with ui.element('div').classes('absolute inset-0 bg-black/50 hidden group-hover:flex items-center justify-center'):
                                     ui.button(icon='close', color='negative', on_click=lambda _, i=idx: remove_captured(i)).props('round dense flat')
                
                def remove_captured(index):
                    if 0 <= index < len(captured_photos):
                        captured_photos.pop(index)
                        update_capture_gallery()

            with ui.column().classes('flex-1 h-full bg-black rounded-lg overflow-hidden relative justify-center items-center'):
                capture_img = ui.interactive_image().classes('w-full h-full object-cover')
                ui.element('div').classes('absolute w-[220px] h-[320px] border-2 border-white/50 rounded-[50%] pointer-events-none shadow-[0_0_0_9999px_rgba(0,0,0,0.5)]')                
                
                with ui.column().classes('absolute bottom-8 items-center gap-4 z-10'):
                    capture_btn = ui.button('Capturar Foto', icon='camera_alt', on_click=lambda: do_capture()).classes('w11-btn scale-125')
                    ui.label('Capture pelo menos 1 foto (recomendado: 3)').classes('text-white bg-black/50 px-3 rounded shadow')

        capture_state = {'frame': None, 'paused': False}
        
        async def capture_loop():
            if not add_user_dialog.value: return 
            if capture_state['paused']: return

            ret, frame = camera_manager.read()
            if ret:
                capture_state['frame'] = frame.copy()
                flipped_frame = cv2.flip(frame, 1) 
                _, buffer = cv2.imencode('.jpg', flipped_frame)
                capture_img.set_source(f'data:image/jpeg;base64,{base64.b64encode(buffer).decode("utf-8")}')
        
        capture_timer = ui.timer(0.05, capture_loop, active=False)
        
        def reset_add_dialog(e):
            if e.value:
                capture_timer.activate()
                captured_photos.clear()
                update_capture_gallery()
                name_input.value = ''
                pin_setup.value = ''
                capture_state['paused'] = False
            else:
                capture_timer.deactivate()

        add_user_dialog.on_value_change(reset_add_dialog)

        async def do_capture():
            if capture_state['frame'] is not None:
                current_frame = capture_state['frame'].copy()
                
                n = ui.notify('Processando...', type='ongoing', timeout=1.0)
                
                capture_state['paused'] = True
                engine.paused = True
                await run.io_bound(lambda: time.sleep(0.1))
                
                try:
                    embedding_objs = await run.io_bound(
                        engine.generate_embedding,
                        current_frame
                    )
                    
                    if embedding_objs:
                        emb = embedding_objs[0]['embedding']
                        captured_photos.append((current_frame, emb))
                        update_capture_gallery()
                        ui.notify(f'Foto {len(captured_photos)} capturada!', type='positive')
                    else:
                        ui.notify('Rosto não detectado. Tente novamente.', type='warning')
                        
                except Exception as e:
                    ui.notify(f'Erro: {e}', type='negative')
                finally:
                    engine.paused = False
                    capture_state['paused'] = False
                    if n: n.dismiss()

        async def save_new_user():
            if not name_input.value or not pin_setup.value:
                ui.notify('Preencha Nome e PIN', type='negative')
                return
            if not captured_photos:
                ui.notify('Capture pelo menos uma foto.', type='warning')
                return
            
            success, user_id = db_manager.create_user(
                name=name_input.value,
                pin=pin_setup.value,
                access_level=access_select.value
            )
            
            if not success:
                ui.notify(f'Erro ao criar usuário: {user_id}', type='negative')
                return
                
            count = 0
            for frame, emb in captured_photos:
                ok, _ = db_manager.add_user_photo(user_id, frame, emb)
                if ok: count += 1
            
            ui.notify(f'Usuário criado com {count} fotos!')
            await run.io_bound(engine.load_model)
            add_user_dialog.close()
            ui.navigate.reload()

        with ui.row().classes('mt-4 gap-4'):
            ui.button('Cancelar', on_click=add_user_dialog.close).props('flat')
            ui.button('Salvar Usuário', on_click=save_new_user).classes('w11-btn bg-blue-600 text-white')
