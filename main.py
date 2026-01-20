import sys
import os
print("DEBUG: Imports starting...")
from nicegui import ui, app
print("DEBUG: NiceGUI imported")
import socket
from src.common.logger import AppLogger
print("DEBUG: Logger imported")

AppLogger.setup()

if getattr(sys, 'frozen', False):
    from src.common.loading_screen import show_loading, update_loading, close_loading
    loading = show_loading()
    update_loading("Inicializando aplicação...")

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

if getattr(sys, 'frozen', False):
    update_loading("Carregando componentes...")

from src.common.theme import load_theme
from src.services.services import start_services, stop_services
from src.pages.login.login import login_page
from src.pages.dashboard.dashboard import dashboard_page
from src.pages.setup.setup import setup_page
from src.pages.landing.landing import landing_page

if getattr(sys, 'frozen', False):
    update_loading("Iniciando serviços...")

def startup_wrapper():
    """Wrapper to start services"""
    start_services()

app.on_startup(startup_wrapper)
app.on_shutdown(stop_services)

def close_splash():
    pass

app.on_startup(close_splash)

load_theme()

print(f"Static Src Path: {static_src_path}")
if os.path.exists(static_src_path):
    print(f"Contents of src: {os.listdir(static_src_path)}")
    public_path = os.path.join(static_src_path, 'public')
    if os.path.exists(public_path):
         print(f"Contents of src/public: {os.listdir(public_path)}")

app.add_static_files('/src', static_src_path)

@ui.page('/')
def index():
    landing_page()

@ui.page('/recognition')
def recognition():
    login_page()

@ui.page('/dashboard')
def dashboard():
    dashboard_page()

@ui.page('/setup')
def setup():
    setup_page()

if getattr(sys, 'frozen', False):
    update_loading("Abrindo interface...")
    import time
    time.sleep(0.3) 
    close_loading()


def find_free_port(start_port=8080, max_tries=100):
    for port in range(start_port, start_port + max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', port))
                return port
            except OSError:
                continue
    raise OSError("No free ports found")

if __name__ in {"__main__", "__mp_main__"}:
    port = find_free_port()
    print(f"Starting UI on port {port}")
    favicon_path = os.path.join(static_src_path, 'public/images/certi/logo-certi.png')
    ui.run(title='DeepFace Access Control', favicon=favicon_path, port=port, reload=False, native=True, storage_secret='deepface_secret')
