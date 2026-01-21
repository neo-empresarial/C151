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

def startup_wrapper():
    start_services()

app.on_startup(startup_wrapper)
app.on_shutdown(stop_services)

load_theme()

app.add_static_files('/src', static_src_path)
app.add_static_files('/public', os.path.join(static_src_path, 'public'))

START_MODE = 'default'

@ui.page('/')
def index_page():
    loading_overlay()
    
    if START_MODE == 'dashboard':
        dashboard_page()
    elif START_MODE == 'recognition':
        login_page()
    else:
        landing_page()

@ui.page('/recognition')
def recognition():
    loading_overlay()
    login_page()

@ui.page('/dashboard')
def dashboard():
    loading_overlay()
    dashboard_page()

@ui.page('/setup')
def setup():
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
    favicon_path = os.path.join(static_src_path, 'public/images/certi/logo-certi.png')

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
