from nicegui import ui
from src.common.styles import Colors

# New Header Layout
def render(on_back):
    with ui.row().classes('w-full justify-between items-center mb-8 shrink-0'):
        # Left Side: Back Arrow + Title
        with ui.row().classes('items-center gap-4'):
            ui.button(icon='arrow_back', on_click=on_back).props('round flat').classes('text-2xl opacity-70 hover:opacity-100 transition-opacity')
            ui.label('Painel Administrativo').classes('text-3xl font-light tracking-tight')

        # Right Side: Empty for now (or could add minimal actions)
        with ui.row().classes('items-center gap-4'):
             pass
