from nicegui import ui
from .components import header, navigation, footer

def landing_page():
    with ui.column().classes('w-full h-screen items-center justify-center bg-gray-50 gap-8 relative'):
        header.render()
        navigation.render_cards()
        footer.render()
