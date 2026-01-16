import sys
import os
from nicegui import ui, app
import socket

if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))
    
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    static_src_path = os.path.join(base_path, 'src')
else:
    static_src_path = 'src'

sys.path.append(".") 
from src.common.theme import load_theme
from src.services.services import start_services, stop_services
from src.pages.login import login_page
from src.pages.dashboard import dashboard_page
from src.pages.setup import setup_page
from src.pages.landing import landing_page

app.on_startup(start_services)
app.on_shutdown(stop_services)

def close_splash():
    try:
        import pyi_splash
        pyi_splash.update_text('UI Loaded...')
        pyi_splash.close()
    except:
        pass

app.on_startup(close_splash)

load_theme()

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


def find_free_port(start_port=8080, max_tries=100):
    for port in range(start_port, start_port + max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', port))
                return port
            except OSError:
                continue
    raise OSError("No free ports found")

port = find_free_port()
print(f"Starting UI on port {port}")
ui.run(title='DeepFace Access Control', favicon='🛡️', port=port, reload=False, native=True)
