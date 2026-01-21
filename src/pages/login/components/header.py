from nicegui import ui
from src.common import theme

def render(on_pin_click=None):
    with ui.row().classes('w-full h-[80px] items-center px-8 justify-between shrink-0').style('background: transparent; border-bottom: 1px solid var(--border);'):
        # Left: Back Arrow + Title
        with ui.row().classes('items-center gap-6'):
             ui.button(icon='arrow_back', on_click=lambda: ui.navigate.to('/')).props('round flat').classes('text-2xl text-white opacity-80 hover:opacity-100')
             ui.label('Reconhecimento Facial').classes('text-2xl font-light tracking-wide text-white')
        
        # Right: PIN Button
        with ui.row().classes('items-center gap-4'):
             if on_pin_click:
                ui.button('Entrar com PIN', on_click=on_pin_click).classes('w11-btn bg-white/10 text-white hover:bg-white/20 backdrop-blur-md text-sm px-6 py-2')
