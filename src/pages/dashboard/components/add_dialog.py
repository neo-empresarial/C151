from nicegui import ui
import asyncio
from .. import functions as f
from . import camera
from src.language.manager import language_manager as lm

class AddDialog:
    def __init__(self, on_user_added):
        self.dialog = ui.dialog().props('maximized')
        self.on_user_added = on_user_added
        
        self.captured_photos = []
        self.capture_state = {'frame': None, 'paused': False, 'confirmed': False}
        self.loading_visible = False
        
        with self.dialog, ui.card().classes('w-full h-full p-8 overflow-hidden relative'):
             self.render_header()
             with ui.row().classes('w-full h-full flex-nowrap max-w-full gap-8'):
                self.render_left_column()
                self.render_right_column()

             with ui.column().classes('absolute inset-0 z-[9999] bg-black/80 justify-center items-center backdrop-blur-sm').bind_visibility_from(self, 'loading_visible') as self.loading_overlay:
                 ui.spinner(size='4rem').classes('text-primary')
                 ui.label('Criando sistema...').classes('text-white text-2xl font-bold mt-4 animate-pulse')

        self.setup_capture_dialog()

    def render_header(self):
        with ui.row().classes('w-full items-center justify-between mb-6'):
            ui.label(lm.t('new_user')).classes('text-2xl font-bold')
            ui.button(icon='close', on_click=self.dialog.close).props('round dense flat')

    def render_left_column(self):
        with ui.column().classes('w-1/3 min-w-[350px] h-full gap-6'):
            ui.label(lm.t('personal_data')).classes('text-xl font-semibold opacity-80')
            with ui.card().classes('w11-card w-full p-6 gap-4'):
                self.name_input = ui.input(lm.t('full_name')).classes('w-full')
                self.pin_setup = ui.input(lm.t('pin_numeric'), password=True, password_toggle_button=True).classes('w-full')
                self.access_select = ui.select(['Admin', 'Funcionario', 'Visitante'], value='Visitante', label=lm.t('access_level')) \
                    .classes('w-full').props('outlined behavior=menu')

            with ui.row().classes('w-full gap-4 mt-6'):
                ui.button(lm.t('cancel'), on_click=self.dialog.close).classes('flex-1 w11-btn')
                ui.button(lm.t('create_user'), on_click=self.save_new_user).classes('flex-1 w11-btn bg-primary')

    def render_right_column(self):
         with ui.column().classes('flex-1 h-full gap-4 overflow-hidden'):
            ui.label(lm.t('biometrics_photos')).classes('text-xl font-semibold opacity-80')
            with ui.card().classes('w11-card w-full h-full p-6 flex flex-col gap-4 overflow-hidden'):
                with ui.row().classes('w-full justify-between items-center'):
                    ui.label(lm.t('captured_photos')).classes('text-sm font-bold opacity-60')
                    ui.button(lm.t('capture_photo'), icon='add_a_photo', on_click=self.open_capture_dialog).classes('px-4 w11-btn bg-primary')
                
                self.gallery_container = ui.element('div').classes('w-full flex-1 overflow-y-auto p-4 rounded border flex flex-wrap content-start gap-4 transition-all')
                self.gallery_container.style('border-color: var(--border)')

    def update_gallery(self):
        self.gallery_container.clear()
        with self.gallery_container:
            if not self.captured_photos:
                 ui.label(lm.t('no_photos_captured')).classes('w-full text-center opacity-50 italic mt-10')
            
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
        with self.capture_dialog, ui.card().classes('w-[800px] max-w-full p-0 overflow-hidden flex flex-col w11-card'):
            with ui.row().classes('w-full p-3 justify-between items-center z-20 absolute top-0 left-0'):
                ui.label(lm.t('capture_photo')).classes('text-white font-bold ml-2 shadow-black drop-shadow-md')
                ui.button(icon='close', on_click=self.capture_dialog.close).props('round dense flat color=white').classes('shadow-black drop-shadow-md')

            self.cam_card, self.cam_view = camera.render_view()
            with self.cam_card:
                 with ui.row().classes('absolute bottom-0 w-full p-6 justify-center items-center gap-6 z-30'):
                      self.c_btn = ui.button('Capturar', icon='camera_alt', on_click=self.do_capture_frame).classes('w11-btn scale-110 bg-white text-black shadow-xl')
                      with ui.row().classes('gap-4 hidden') as row:
                         self.c_confirm_row = row
                         ui.button('Refazer', icon='refresh', color='white', on_click=self.reset_capture).props('outline text-color=white').classes('w11-btn')
                         ui.button('Confirmar', icon='check', color='positive', on_click=self.confirm_capture).classes('w11-btn shadow-lg')

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
        async with f.loading_state():
            if self.capture_state['frame'] is not None:
                try:
                    result = await f.verify_enrollment_logic(self.capture_state['frame'])
                    
                    if not result['success']:
                        ui.notify(result['message'], type='negative')
                        self.reset_capture()
                        return

                    matched_user = result.get('matched_user')
                    if matched_user:
                        ui.notify(lm.t('error_face_exists', name=matched_user['name']), type='negative')
                        self.reset_capture()
                        return

                    emb = result['embedding']
                    self.captured_photos.append((self.capture_state['frame'], emb))
                    
                    ui.notify(lm.t('photo_validated'), type='positive')
                    self.update_gallery()
                    self.capture_dialog.close()
                    
                except Exception as e:
                    ui.notify(lm.t('internal_error', error=str(e)), type='negative')

    async def save_new_user(self):
        if not self.name_input.value or not self.pin_setup.value:
            ui.notify(lm.t('fill_name_pin'), type='negative'); return
        if not self.captured_photos:
            ui.notify(lm.t('capture_one_photo'), type='warning'); return
        
        self.loading_visible = True
        await asyncio.sleep(0.1)

        try:
            success, user_id = await f.run.io_bound(f.create_user_db, 
                name=self.name_input.value,
                pin=self.pin_setup.value,
                access_level=self.access_select.value
            )
            
            if not success:
                ui.notify(f'Erro: {user_id}', type='negative')
                self.loading_visible = False
                return
                
            count = 0
            for frame, emb in self.captured_photos:
                ok, _ = await f.run.io_bound(f.add_user_photo_db, user_id, frame, emb)
                if ok: count += 1
            
            ui.notify(lm.t('user_created', count=count))
            await f.reload_model_logic()
            self.dialog.close()
            self.on_user_added()
        except Exception as e:
            ui.notify(f'Error: {str(e)}', type='negative')
        finally:
            self.loading_visible = False
