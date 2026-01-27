import sys
import os
from nicegui import ui, app
import socket
from src.common.logger import AppLogger

AppLogger.setup()

if getattr(sys, 'frozen', False):
    exe_dir = os.path.dirname(sys.executable)
    os.chdir(exe_dir)
    
    base_path = getattr(sys, '_MEIPASS', exe_dir)
    static_src_path = os.path.join(base_path, 'src')
    
    if os.path.exists('users.db'):
        print("Database found in executable directory")
    else:
        print("WARNING: users.db not found in executable directory")
else:
    static_src_path = 'src'

sys.path.append(".") 

from src.common.theme import load_theme, loading_overlay
from src.services.services import start_services, stop_services
from src.pages.login.login import login_page
from src.pages.dashboard.dashboard import dashboard_page
from src.pages.setup.setup import setup_page
from src.pages.landing.landing import landing_page
from src.pages.settings.settings import settings_page

def startup_wrapper():
    start_services()
    if getattr(sys, 'frozen', False):
        try:
            import pyi_splash
            pyi_splash.close()
        except ImportError:
            pass

app.on_startup(startup_wrapper)
app.on_shutdown(stop_services)

load_theme()

app.add_static_files('/src', static_src_path)
app.add_static_files('/public', os.path.join(static_src_path, 'public'))

START_MODE = 'default'


def ensure_security():
    from src.common.security import is_key_configured, save_secret_key
    from src.language.manager import language_manager as lm

    if is_key_configured():
        return True

    loading_overlay()
    with ui.dialog().props('persistent') as dialog, ui.card().classes('w-96 p-6'):
        ui.label(lm.t('security_config_title')).classes('text-xl font-bold mb-4 text-red-600')
        ui.label(lm.t('security_config_desc')).classes('mb-4 text-gray-700')
        
        ui.label(lm.t('enter_secret_key')).classes('text-sm font-bold text-gray-600')
        key_input = ui.input(placeholder='Ex: min-ha-cha-ve-se-cre-ta-123').classes('w-full mb-6').props('outlined dense')
        
        def save_key():
            if not key_input.value:
                ui.notify(lm.t('key_cannot_be_empty'), type='warning')
                return
            
            if save_secret_key(key_input.value):
                ui.notify(lm.t('key_saved_success'), type='positive')
                dialog.close()
                ui.run_javascript('window.location.href = "/"')
            else:
                ui.notify(lm.t('error_saving_key'), type='negative')

        ui.button(lm.t('save_and_start'), on_click=save_key).classes('w-full bg-red-600 text-white font-bold')
    
    dialog.open()
    return False

@ui.page('/')
def index_page():
    if not ensure_security(): return
    loading_overlay()
    
    if START_MODE == 'dashboard':
        dashboard_page()
    elif START_MODE == 'recognition':
        login_page()
    else:
        landing_page()

@ui.page('/recognition')
def recognition():
    if not ensure_security(): return
    loading_overlay()
    login_page()

@ui.page('/settings')
def settings():
    if not ensure_security(): return
    loading_overlay()
    settings_page()

@ui.page('/dashboard')
def dashboard():
    if not ensure_security(): return
    loading_overlay()
    dashboard_page()

@ui.page('/setup')
def setup():
    if not ensure_security(): return
    setup_page()

def find_free_port(start_port=8080, max_tries=100):
    for port in range(start_port, start_port + max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', port))
                return port
            except OSError:
                continue
    raise OSError("No free ports found")

def run_app(start_mode='default'):
    global START_MODE
    START_MODE = start_mode

    port = find_free_port()
    print(f"Starting UI on port {port} with mode {start_mode}")
    # Use absolute path for window icon (native mode often requires file path)
    favicon_path = os.path.join(static_src_path, 'public', 'icons', 'certi-icon.ico')

    ui.run(title='DeepFace Access Control', 
            favicon=favicon_path, 
            port=port, 
            reload=False, 
            native=True, 
            fullscreen=True, 
            window_size=(1280, 800), 
            storage_secret='deepface_secret')

if __name__ in {"__main__", "__mp_main__"}:
    run_app()
