from nicegui import ui
from .. import functions as f
from . import camera
import cv2

class AddDialog:
    def __init__(self, on_user_added):
        self.dialog = ui.dialog().props('maximized')
        self.on_user_added = on_user_added
        self.captured_photos = [] 
        self.capture_state = {'frame': None, 'paused': False}
        
        with self.dialog, ui.card().classes('w-full h-full p-8 flex flex-col items-center'):
            ui.label('Novo Usuário').classes('text-2xl font-bold mb-6')
            with ui.row().classes('w-full max-w-6xl gap-8 h-full'):
                self.render_left_column()
                self.render_right_column()
            
            with ui.row().classes('mt-4 gap-4'):
                ui.button('Cancelar', on_click=self.dialog.close).props('flat')
                ui.button('Salvar Usuário', on_click=self.save_new_user).classes('w11-btn bg-blue-600 text-white')

        self.capture_timer = ui.timer(0.05, self.capture_loop, active=False)
        self.dialog.on_value_change(self.on_dialog_change)

    def render_left_column(self):
        with ui.column().classes('w-1/3 gap-4'):
            self.name_input = ui.input('Nome Completo').classes('w-full')
            self.pin_setup = ui.input('PIN (Numérico)', password=True, password_toggle_button=True).classes('w-full')
            self.access_select = ui.select(['Admin', 'Funcionario', 'Visitante'], value='Visitante', label='Nível de Acesso').classes('w-full')
            ui.separator().classes('my-4')
            ui.label('Fotos Capturadas:').classes('font-bold')
            self.capture_gallery = ui.grid(columns=3).classes('w-full gap-2')

    def render_right_column(self):
        with ui.column().classes('flex-1 h-full bg-black rounded-lg overflow-hidden relative justify-center items-center'):
            self.capture_img = ui.interactive_image().classes('w-full h-full object-cover')
            camera.render_overlay()              
            with ui.column().classes('absolute bottom-8 items-center gap-4 z-10'):
                self.capture_btn = ui.button('Capturar Foto', icon='camera_alt', on_click=self.do_capture).classes('w11-btn scale-125')
                ui.label('Capture pelo menos 1 foto (recomendado: 3)').classes('text-white bg-black/50 px-3 rounded shadow')

    def open(self):
        self.dialog.open()

    def on_dialog_change(self, e):
        if e.value:
            self.capture_timer.activate()
            self.captured_photos.clear()
            self.update_capture_gallery()
            self.name_input.value = ''
            self.pin_setup.value = ''
            self.capture_state['paused'] = False
        else:
            self.capture_timer.deactivate()

    async def capture_loop(self):
        if not self.dialog.value: return 
        if self.capture_state['paused']: return
        ret, frame = f.read_camera_frame()
        if ret:
            self.capture_state['frame'] = frame.copy()
            jpg_as_text = f.process_frame_for_display(frame)
            self.capture_img.set_source(f'data:image/jpeg;base64,{jpg_as_text}')

    async def do_capture(self):
        if self.capture_state['frame'] is not None:
            current_frame = self.capture_state['frame'].copy()
            n = ui.notify('Processando...', type='ongoing', timeout=1.0)
            self.capture_state['paused'] = True
            try:
                embedding_objs = await f.generate_embedding_logic(current_frame)
                if embedding_objs:
                    emb = embedding_objs[0]['embedding']
                    self.captured_photos.append((current_frame, emb))
                    self.update_capture_gallery()
                    ui.notify(f'Foto {len(self.captured_photos)} capturada!', type='positive')
                else:
                    ui.notify('Rosto não detectado. Tente novamente.', type='warning')
            except Exception as e:
                ui.notify(f'Erro: {e}', type='negative')
            finally:
                self.capture_state['paused'] = False
                if n: n.dismiss()

    def update_capture_gallery(self):
        self.capture_gallery.clear()
        with self.capture_gallery:
            for idx, (frame, _) in enumerate(self.captured_photos):
                with ui.card().classes('p-0 relative group'):
                    jpg_as_text = f.process_frame_for_display(frame)
                    ui.image(f'data:image/jpeg;base64,{jpg_as_text}').classes('w-full h-20 object-cover')
                    with ui.element('div').classes('absolute inset-0 bg-black/50 hidden group-hover:flex items-center justify-center'):
                            ui.button(icon='close', color='negative', on_click=lambda _, i=idx: self.remove_captured(i)).props('round dense flat')

    def remove_captured(self, index):
        if 0 <= index < len(self.captured_photos):
            self.captured_photos.pop(index)
            self.update_capture_gallery()

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
            ui.notify(f'Erro ao criar usuário: {user_id}', type='negative'); return
            
        count = 0
        for frame, emb in self.captured_photos:
            ok, _ = f.add_user_photo_db(user_id, frame, emb)
            if ok: count += 1
        
        ui.notify(f'Usuário criado com {count} fotos!')
        await f.reload_model_logic()
        self.dialog.close()
        self.on_user_added()
