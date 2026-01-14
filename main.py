import sys
import os
from nicegui import ui, app

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

ui.run(title='DeepFace Access Control', favicon='🛡️', port=8080, reload=False, native=True)
