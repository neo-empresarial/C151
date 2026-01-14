
import sys
from nicegui import ui, app

sys.path.append(".") 

from src.common.theme import load_theme
from src.services import start_services, stop_services

# Import Pages
from src.pages.login import login_page
from src.pages.dashboard import dashboard_page
from src.pages.setup import setup_page
from src.pages.landing import landing_page

# --- Lifecycle ---
app.on_startup(start_services)
app.on_shutdown(stop_services)

# --- Theme ---
load_theme()

# --- Routing ---
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

# --- Run ---
ui.run(title='DeepFace Access Control', favicon='🛡️', port=8080, reload=False, native=True)
