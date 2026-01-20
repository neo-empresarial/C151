from nicegui import ui
from .. import functions as f
from . import camera

class AddDialog:
    def __init__(self, on_user_added):
        self.dialog = ui.dialog().props('maximized')
        self.on_user_added = on_user_added
        
        # State
        self.captured_photos = [] # List of tuples: (frame, embedding)
        self.capture_state = {'frame': None, 'paused': False, 'confirmed': False}
        
        # UI Structure
        with self.dialog, ui.card().classes('w-full h-full p-8 overflow-hidden'):
             self.render_header()
             with ui.row().classes('w-full h-full flex-nowrap max-w-full gap-8'):
                self.render_left_column()
                self.render_right_column()

        self.setup_capture_dialog()

    def render_header(self):
        with ui.row().classes('w-full items-center justify-between mb-6'):
            ui.label('Novo Usuário').classes('text-2xl font-bold')
            ui.button(icon='close', on_click=self.dialog.close).props('round dense flat')

    def render_left_column(self):
        with ui.column().classes('w-1/3 min-w-[350px] h-full gap-6'):
            ui.label('Dados Pessoais').classes('text-xl font-semibold opacity-80')
            with ui.card().classes('w11-card w-full p-6 gap-4'):
                self.name_input = ui.input('Nome Completo').classes('w-full')
                self.pin_setup = ui.input('PIN (Numérico)', password=True, password_toggle_button=True).classes('w-full')
                self.access_select = ui.select(['Admin', 'Funcionario', 'Visitante'], value='Visitante', label='Nível de Acesso').classes('w-full')

            with ui.row().classes('w-full gap-4 mt-6'):
                ui.button('Cancelar', on_click=self.dialog.close).classes('flex-1 w11-btn')
                ui.button('Criar Usuário', on_click=self.save_new_user).classes('flex-1 w11-btn bg-primary')

    def render_right_column(self):
         with ui.column().classes('flex-1 h-full gap-4 overflow-hidden'):
            ui.label('Biometria e Fotos').classes('text-xl font-semibold opacity-80')
            with ui.card().classes('w11-card w-full h-full p-6 flex flex-col gap-4 overflow-hidden'):
                with ui.row().classes('w-full justify-between items-center'):
                    ui.label('Fotos Capturadas').classes('text-sm font-bold opacity-60')
                    ui.button('Capturar Foto', icon='add_a_photo', on_click=self.open_capture_dialog).classes('px-4 w11-btn bg-primary')
                
                # Gallery Container
                self.gallery_container = ui.element('div').classes('w-full flex-1 overflow-y-auto p-4 rounded border flex flex-wrap content-start gap-4 transition-all')
                self.gallery_container.style('border-color: var(--border)')

    def update_gallery(self):
        self.gallery_container.clear()
        with self.gallery_container:
            if not self.captured_photos:
                 ui.label('Nenhuma foto capturada.').classes('w-full text-center opacity-50 italic mt-10')
            
            for index, (frame, _) in enumerate(self.captured_photos):
                with ui.card().classes('w11-card p-2 flex flex-col gap-2 items-center'):
                    jpg_as_text = f.process_frame_for_display(frame)
                    ui.image(f'data:image/jpeg;base64,{jpg_as_text}').style('width: 120px; height: 120px; object-fit: cover;').classes('rounded')
                    ui.button(icon='close', color='negative', on_click=lambda _, i=index: self.remove_photo(i)).props('round flat dense size=sm')

    def remove_photo(self, index):
        if 0 <= index < len(self.captured_photos):
            self.captured_photos.pop(index)
            self.update_gallery()

    def setup_capture_dialog(self):
        self.capture_dialog = ui.dialog()
        with self.capture_dialog, ui.card().classes('w-[500px] p-0 overflow-hidden flex flex-col w11-card'):
            with ui.row().classes('w-full bg-black p-2 justify-between items-center'):
                ui.label('Capturar Foto').classes('text-white font-bold ml-2')
                ui.button(icon='close', on_click=self.capture_dialog.close).props('round dense flat color=white')

            with ui.element('div').classes('relative w-full h-[400px] bg-black overflow-hidden justify-center items-center'):
                 self.cam_view = ui.interactive_image().classes('w-full h-full object-cover')
                 camera.render_overlay()
                 with ui.column().classes('absolute bottom-6 left-0 right-0 items-center gap-3 z-10 w-full'):
                      self.c_btn = ui.button('Capturar', icon='camera_alt', on_click=self.do_capture_frame).classes('w11-btn scale-125 bg-white text-black')
                      with ui.row().classes('gap-3 hidden') as row:
                         self.c_confirm_row = row
                         ui.button('Refazer', icon='refresh', color='white', on_click=self.reset_capture).props('text-color=black')
                         ui.button('Confirmar', icon='check', color='positive', on_click=self.confirm_capture)

        self.cam_timer = ui.timer(0.05, self.cam_loop, active=False)
        self.capture_dialog.on_value_change(lambda e: self.cam_timer.deactivate() if not e.value else None)

    def open(self):
        self.name_input.value = ''
        self.pin_setup.value = ''
        self.captured_photos.clear()
        self.update_gallery()
        self.dialog.open()

    def open_capture_dialog(self):
        self.reset_capture()
        self.capture_dialog.open()
        self.cam_timer.activate()

    async def cam_loop(self):
        if not self.capture_dialog.value: return
        if self.capture_state['paused']: return
        ret, frame = f.read_camera_frame()
        if ret:
            self.capture_state['frame'] = frame.copy()
            jpg_as_text = f.process_frame_for_display(frame)
            self.cam_view.set_source(f'data:image/jpeg;base64,{jpg_as_text}')

    def reset_capture(self):
        self.capture_state['paused'] = False
        self.capture_state['confirmed'] = False
        self.capture_state['frame'] = None
        self.c_btn.visible = True
        self.c_confirm_row.visible = False

    def do_capture_frame(self):
        if self.capture_state['frame'] is not None:
            self.capture_state['paused'] = True
            self.c_btn.visible = False
            self.c_confirm_row.visible = True

    async def confirm_capture(self):
        if self.capture_state['frame'] is not None:
            try:
                result = await f.verify_enrollment_logic(self.capture_state['frame'])
                
                if not result['success']:
                    ui.notify(result['message'], type='negative')
                    self.reset_capture()
                    return

                matched_user = result.get('matched_user')
                if matched_user:
                    ui.notify(f"Erro: Rosto já pertence a {matched_user['name']}", type='negative')
                    self.reset_capture()
                    return

                emb = result['embedding']
                self.captured_photos.append((self.capture_state['frame'], emb))
                
                ui.notify('Foto validada e adicionada!', type='positive')
                self.update_gallery()
                self.capture_dialog.close()
                
            except Exception as e:
                ui.notify(f'Erro interno: {e}', type='negative')

    async def save_new_user(self):
        if not self.name_input.value or not self.pin_setup.value:
            ui.notify('Preencha Nome e PIN', type='negative'); return
        if not self.captured_photos:
            ui.notify('Capture pelo menos uma foto.', type='warning'); return
        
        success, user_id = f.create_user_db(
            name=self.name_input.value,
            pin=self.pin_setup.value,
            access_level=self.access_select.value
        )
        if not success:
            ui.notify(f'Erro: {user_id}', type='negative'); return
            
        count = 0
        for frame, emb in self.captured_photos:
            ok, _ = f.add_user_photo_db(user_id, frame, emb)
            if ok: count += 1
        
        ui.notify(f'Usuário criado com {count} fotos!')
        await f.reload_model_logic()
        self.dialog.close()
        self.on_user_added()
