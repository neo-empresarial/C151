from nicegui import ui

def render():
    with ui.row().classes('w-full h-[60px] items-center px-6 justify-between shrink-0').style('background-color: var(--surface); border-bottom: 1px solid var(--border); color: var(--text-primary);'):
        with ui.row().classes('items-center gap-4'):
                ui.image('/src/public/images/certi/logo-certi.png').classes('h-12 w-auto object-contain')
                ui.label('Reconhecimento Facial').classes('text-xl font-semibold')
        with ui.row().classes('gap-2'):
            ui.button(icon='home', on_click=lambda: ui.navigate.to('/')).props('flat round dense')
