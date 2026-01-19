from nicegui import ui
from .components import header, navigation, footer
from src.common import theme

def landing_page():
    with ui.column().classes('w-full h-screen items-center justify-center gap-8 relative'):
        theme.render_theme_toggle_button()
        header.render()
        navigation.render_cards()
        footer.render()
