from nicegui import ui
from .. import functions as f
from . import gallery
from . import camera

class EditDialog:
    def __init__(self, on_user_updated):
        self.dialog = ui.dialog().props('maximized')
        self.current_edit_id = [None]
        self.edit_capture_state = {'frame': None, 'confirmed': False, 'paused': False}
        self.on_user_updated = on_user_updated
        
        with self.dialog, ui.card().classes('w11-card w-full h-full p-8 overflow-hidden'):
            self.render_header()
            with ui.row().classes('w-full h-full flex-nowrap max-w-full gap-8'):
                self.render_left_column()
                self.render_right_column()

        self.setup_capture_dialog()

    def render_header(self):
        with ui.row().classes('w-full items-center justify-between mb-6'):
            ui.label('Editar Usuário').classes('text-2xl font-bold')
            ui.button(icon='close', on_click=self.dialog.close).props('round dense flat')

    def render_left_column(self):
        with ui.column().classes('w-1/3 min-w-[350px] h-full gap-6'):
            ui.label('Dados Pessoais').classes('text-xl font-semibold opacity-80')
            with ui.card().classes('w11-card w-full p-6 gap-4'):
                self.edit_name = ui.input('Nome Completo').classes('w-full')
                self.edit_pin = ui.input('PIN de Acesso', password=True, password_toggle_button=True).classes('w-full')
                self.edit_access = ui.select(['Admin', 'Funcionario', 'Visitante'], label='Nível de Acesso').classes('w-full')

            with ui.row().classes('w-full gap-4 mt-6'):
                ui.button('Cancelar', on_click=self.dialog.close).classes('flex-1 w11-btn')
                ui.button('Salvar', on_click=self.save_edit_info).classes('flex-1 w11-btn bg-primary')

    def render_right_column(self):
         with ui.column().classes('flex-1 h-full gap-4 overflow-hidden'):
            ui.label('Biometria e Fotos').classes('text-xl font-semibold opacity-80')
            with ui.card().classes('w11-card w-full h-full p-6 flex flex-col gap-4 overflow-hidden'):
                with ui.row().classes('w-full justify-between items-center'):
                    ui.label('Fotos Cadastradas').classes('text-sm font-bold opacity-60')
                    ui.button('Adicionar Nova Foto', icon='add_a_photo', on_click=self.open_capture_dialog).classes('px-4 w11-btn bg-primary')
                self.photos_container = ui.element('div').classes('w-full flex-1 overflow-y-auto p-2 rounded border flex flex-wrap content-start gap-4 transition-all')
                self.photos_container.style('border-color: var(--border)')

    def setup_capture_dialog(self):
        self.capture_dialog = ui.dialog()
        with self.capture_dialog, ui.card().classes('w-[500px] p-0 overflow-hidden flex flex-col w11-card'):
            with ui.row().classes('w-full bg-black p-2 justify-between items-center'):
                ui.label('Capturar Foto').classes('text-white font-bold ml-2')
                ui.button(icon='close', on_click=self.capture_dialog.close).props('round dense flat color=white')

            with ui.element('div').classes('relative w-full h-[400px] bg-black overflow-hidden justify-center items-center'):
                 self.edit_cam_view = ui.interactive_image().classes('w-full h-full object-cover')
                 camera.render_overlay()
                 with ui.column().classes('absolute bottom-6 left-0 right-0 items-center gap-3 z-10 w-full'):
                      self.e_capture_btn = ui.button('Capturar', icon='camera_alt', on_click=self.edit_capture).classes('w11-btn scale-125 bg-white text-black')
                      with ui.row().classes('gap-3 hidden') as row:
                         self.e_confirm_row = row
                         ui.button('Refazer', icon='refresh', color='white', on_click=self.edit_reset).props('text-color=black')
                         ui.button('Salvar', icon='check', color='positive', on_click=self.edit_confirm_add)

        self.edit_cam_timer = ui.timer(0.05, self.edit_cam_loop, active=False)
        self.capture_dialog.on_value_change(lambda e: self.edit_cam_timer.deactivate() if not e.value else None)

    def open(self, user):
        self.current_edit_id[0] = user['id']
        self.edit_name.value = user['name']
        self.edit_pin.value = user['pin']
        self.edit_access.value = user['access_level']
        self.refresh_edit_gallery(user['id'])
        self.edit_reset()
        self.edit_cam_timer.deactivate()
        self.dialog.open()

    def refresh_edit_gallery(self, user_id):
        user_photos = f.get_user_photos(user_id)
        gallery.render(self.photos_container, user_photos, self.delete_photo)

    async def delete_photo(self, photo_id):
        success, msg = f.delete_photo_from_db(photo_id)
        if success:
            ui.notify('Foto removida')
            self.refresh_edit_gallery(self.current_edit_id[0])
            await f.reload_model_logic()
        else:
            ui.notify(f'Erro: {msg}', type='negative')

    def open_capture_dialog(self):
        self.edit_reset()
        self.capture_dialog.open()
        self.edit_cam_timer.activate()

    async def edit_cam_loop(self):
        if not self.capture_dialog.value: return
        if self.edit_capture_state['paused']: return
        ret, frame = f.read_camera_frame()
        if ret:
            self.edit_capture_state['frame'] = frame.copy()
            jpg_as_text = f.process_frame_for_display(frame)
            self.edit_cam_view.set_source(f'data:image/jpeg;base64,{jpg_as_text}')

    def edit_reset(self):
        self.edit_capture_state['paused'] = False
        self.edit_capture_state['confirmed'] = False
        self.edit_capture_state['frame'] = None
        self.e_capture_btn.visible = True
        self.e_confirm_row.visible = False

    def edit_capture(self):
        if self.edit_capture_state['frame'] is not None:
            self.edit_capture_state['paused'] = True
            self.e_capture_btn.visible = False
            self.e_confirm_row.visible = True

    async def edit_confirm_add(self):
        if self.edit_capture_state['frame'] is not None:
            try:
                result = await f.verify_enrollment_logic(self.edit_capture_state['frame'])
                
                if not result['success']:
                    ui.notify(result['message'], type='negative')
                    self.edit_reset()
                    return

                matched_user = result.get('matched_user')
                if matched_user:
                    if matched_user['id'] != self.current_edit_id[0]:
                        ui.notify(f"Erro: Rosto já pertence a {matched_user['name']}", type='negative')
                        self.edit_reset()
                        return
                
                emb = result['embedding']
                success, _ = f.add_user_photo_db(self.current_edit_id[0], self.edit_capture_state['frame'], emb)
                
                if success: 
                    ui.notify('Foto validada e adicionada!', type='positive')
                    self.refresh_edit_gallery(self.current_edit_id[0])
                    self.capture_dialog.close()
                    await f.reload_model_logic()
                else:
                    ui.notify('Erro ao salvar foto no banco', type='negative')
                    
            except Exception as e:
                ui.notify(f'Erro ao processar: {str(e)}', type='negative')

    async def save_edit_info(self):
        if not self.edit_name.value or not self.edit_pin.value:
            ui.notify('Preencha nome e PIN', type='negative'); return
        updates = {
            'name': self.edit_name.value,
            'pin': self.edit_pin.value,
            'access_level': self.edit_access.value
        }
        success, msg = f.update_user_db(self.current_edit_id[0], updates)
        if success:
             ui.notify('Dados atualizados')
             await f.reload_model_logic() 
             self.dialog.close()
             self.on_user_updated()
        else:
             ui.notify(f'Erro: {msg}')
