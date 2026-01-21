from nicegui import ui
from src.common import theme
from src.language.manager import language_manager as lm

def render(on_pin_click=None, on_back=None):
    with ui.row().classes('w-full h-[80px] items-center px-8 justify-between shrink-0').style('background: transparent; border-bottom: 1px solid var(--border);'):
        with ui.row().classes('items-center gap-6'):
             action = on_back if on_back else lambda: ui.navigate.to('/')
             ui.button(icon='arrow_back', on_click=action).props('round flat').classes('text-2xl text-[var(--text-primary)] opacity-70 hover:opacity-100 transition-opacity')
             ui.label(lm.t('face_recognition')).classes('text-2xl font-light tracking-wide text-[var(--text-primary)]')
        
        with ui.row().classes('items-center gap-4'):
             if on_pin_click:
                ui.button(lm.t('enter_with_pin'), on_click=on_pin_click).classes('w11-btn bg-white/10 text-white hover:bg-white/20 backdrop-blur-md text-sm px-6 py-2')
