from nicegui import ui
from src.common.styles import Colors
from src.language.manager import language_manager as lm

def render(on_back):
    with ui.row().classes('w-full h-[80px] items-center px-8 justify-between shrink-0').style('background: transparent; border-bottom: 1px solid var(--border);'):
        with ui.row().classes('items-center gap-6'):
            ui.button(icon='arrow_back', on_click=on_back).props('round flat').classes('text-2xl text-[var(--text-primary)] opacity-70 hover:opacity-100 transition-opacity')
            ui.label(lm.t('admin_panel')).classes('text-2xl font-light tracking-wide text-[var(--text-primary)]')

        with ui.row().classes('items-center gap-4'):
             pass
