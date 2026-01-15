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

    edit_dialog = ui.dialog()
    with edit_dialog, ui.card().classes('w11-card w-[500px] p-6'):
        ui.label('Editar Usuário').classes('text-xl font-bold mb-4')
        
        edit_name = ui.input('Nome').classes('w-full')
        edit_pin = ui.input('PIN', password=True, password_toggle_button=True).classes('w-full')
        edit_access = ui.select(['Admin', 'Funcionario', 'Visitante'], label='Acesso').classes('w-full')
        
        current_edit_id = [None] 

        edit_capture_state = {'frame': None, 'confirmed': False, 'paused': False}
        
        ui.label('Foto Atual').classes('font-bold mt-2')
        current_user_img = ui.image().classes('w-[150px] h-[150px] object-cover rounded-lg bg-gray-200 mb-2')
        
        with ui.column().classes('w-full') as camera_container:
            camera_container.visible = False
            
            with ui.element('div').classes('relative w-full h-[300px] bg-black rounded overflow-hidden'):
                 edit_cam_view = ui.interactive_image().classes('w-full h-full object-cover')
                 ui.element('div').classes('absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[200px] h-[280px] border-2 border-white/50 rounded-[50%] pointer-events-none shadow-[0_0_0_9999px_rgba(0,0,0,0.5)]')

            with ui.row().classes('w-full justify-center mt-2'):
                e_capture_btn = ui.button('Capturar', icon='camera_alt', on_click=lambda: edit_capture()).classes('w11-btn')
                with ui.row().classes('gap-2') as e_confirm_row:
                     ui.button('Tentar Novamente', icon='refresh', color='warning', on_click=lambda: edit_reset())
                     ui.button('Confirmar Foto', icon='check', color='positive', on_click=lambda: edit_confirm())
                e_confirm_row.visible = False

        def toggle_camera():
            if camera_container.visible:
                camera_container.visible = False
                edit_cam_timer.deactivate()
                update_photo_btn.text = 'Alterar Foto'
                update_photo_btn.props('icon=face')
                edit_capture_state['paused'] = False
                edit_capture_state['confirmed'] = False
                edit_capture_state['frame'] = None
                e_capture_btn.visible = True
                e_confirm_row.visible = False
            else:
                camera_container.visible = True
                edit_cam_timer.activate()
                update_photo_btn.text = 'Cancelar Alteração'
                update_photo_btn.props('icon=close')

        update_photo_btn = ui.button('Alterar Foto', icon='face', on_click=toggle_camera).classes('w11-btn w-full mb-4')

        async def edit_cam_loop():
            if not edit_dialog.value or not camera_container.visible: return
            if edit_capture_state['paused']: return
            
            ret, frame = camera_manager.read()
            if ret:
                edit_capture_state['frame'] = frame.copy()
                _, buffer = cv2.imencode('.jpg', frame)
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
                edit_capture_state['confirmed'] = False
                e_capture_btn.visible = False
                e_confirm_row.visible = True

        def edit_confirm():
            edit_capture_state['confirmed'] = True
            ui.notify('Foto confirmada', type='positive')

        async def save_edit():
            if not edit_name.value or not edit_pin.value:
                ui.notify('Preencha tudo', type='negative'); return
            
            updates = {
                'name': edit_name.value,
                'pin': edit_pin.value,
                'access_level': edit_access.value
            }

            if edit_capture_state['frame'] is not None and not edit_capture_state['confirmed']:
                ui.notify('Confirme a nova foto antes de salvar!', type='warning')
                return

            n = None
            engine.paused = True 
            await run.io_bound(lambda: time.sleep(0.5)) 
            try:
                if edit_capture_state['confirmed'] and edit_capture_state['frame'] is not None:
                     n = ui.notify('Atualizando biometria...', type='ongoing', timeout=0)
                     
                     embedding_objs = await run.io_bound(
                        engine.generate_embedding,
                        edit_capture_state['frame']
                    )
                     updates['embedding'] = embedding_objs[0]['embedding']
                     updates['frame'] = edit_capture_state['frame']

                success, msg = db_manager.update_user(current_edit_id[0], **updates)
                
                if not success:
                     ui.notify(f'Erro ao atualizar: {msg}', type='negative')
                     return
                
                if 'embedding' in updates:
                    await run.io_bound(engine.load_model)
                    
                ui.notify('Usuário atualizado')
                edit_dialog.close()
                ui.navigate.reload()

            except Exception as e:
                ui.notify(f'Erro: {e}', type='negative')
            finally:
                engine.paused = False
                if n: 
                    try: n.dismiss() 
                    except: pass

        with ui.row().classes('w-full justify-end mt-4 gap-2'):
            ui.button('Cancelar', on_click=edit_dialog.close).props('flat')
            ui.button('Salvar', on_click=save_edit).classes('w11-btn bg-blue-600 text-white')

    def open_edit_dialog(user):
        current_edit_id[0] = user['id']
        edit_name.value = user['name']
        edit_pin.value = user['pin']
        edit_access.value = user['access_level']
        
        img_blob = db_manager.get_user_image(user['id'])
        if img_blob:
            b64_img = base64.b64encode(img_blob).decode('utf-8')
            current_user_img.set_source(f'data:image/jpeg;base64,{b64_img}')
        else:
             current_user_img.set_source('')

        edit_capture_state['frame'] = None
        edit_capture_state['confirmed'] = False
        edit_capture_state['paused'] = False
        
        camera_container.visible = False
        e_capture_btn.visible = True
        e_confirm_row.visible = False
        update_photo_btn.text = 'Alterar Foto'
        update_photo_btn.props('icon=face')
        edit_cam_timer.deactivate()

        edit_dialog.open()

    add_user_dialog = ui.dialog().props('maximized')
    with add_user_dialog, ui.card().classes('w-full h-full p-8 items-center justify-center'):
        ui.label('Novo Usuário').classes('text-2xl font-bold mb-6')
        
        with ui.row().classes('w-full max-w-4xl gap-8'):
            with ui.column().classes('flex-1 gap-4'):
                name_input = ui.input('Nome Completo').classes('w-full')
                pin_setup = ui.input('PIN (Numérico)', password=True, password_toggle_button=True).classes('w-full')
                access_select = ui.select(['Admin', 'Funcionario', 'Visitante'], value='Visitante', label='Nível de Acesso').classes('w-full')
            
            with ui.column().classes('flex-1 h-[400px] bg-black rounded-lg overflow-hidden relative justify-center items-center'):
                capture_img = ui.interactive_image().classes('w-full h-full object-cover')
                ui.element('div').classes('absolute w-[220px] h-[320px] border-2 border-white/50 rounded-[50%] pointer-events-none shadow-[0_0_0_9999px_rgba(0,0,0,0.5)]')                
    
        capture_state = {
            'frame': None,
            'confirmed': False,
            'paused': False
        }
        
        async def capture_loop():
            if not add_user_dialog.value: return 
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
            
            n = None
            engine.paused = True
            await run.io_bound(lambda: time.sleep(0.5)) # allow loop to yield

            try:
                n = ui.notify('Processando Face... Isso pode levar 10-20s. Aguarde.', type='ongoing', timeout=0)
                
                final_frame = capture_state['frame']
                
                embedding_objs = await run.io_bound(
                    engine.generate_embedding,
                    final_frame
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
                    await run.io_bound(engine.load_model)
                    add_user_dialog.close()
                    ui.navigate.reload()
                else:
                    ui.notify(f'Erro: {msg}', type='negative')
                    
            except Exception as e:
                ui.notify(f'Erro ao processar face: {str(e)}', type='negative')
            finally:
                engine.paused = False
                if n:
                    try: n.dismiss() 
                    except: pass

        with ui.row().classes('mt-8 gap-4'):
            ui.button('Cancelar', on_click=add_user_dialog.close).props('flat')
            ui.button('Salvar Usuário', on_click=save_user).classes('w11-btn bg-blue-600 text-white')
