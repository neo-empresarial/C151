from nicegui import ui

def render_cards():
    with ui.row().classes('gap-8'):
        with ui.card().classes('w11-card w-64 h-64 items-center justify-center cursor-pointer') \
            .on('click', lambda: ui.navigate.to('/recognition')):
            ui.icon('face', size='64px', color='primary').classes('mb-4')
            ui.label('Reconhecimento Facial').classes('text-xl font-semibold text-center')
        
        with ui.card().classes('w11-card w-64 h-64 items-center justify-center cursor-pointer') \
            .on('click', lambda: ui.navigate.to('/dashboard')):
            ui.icon('admin_panel_settings', size='64px', color='positive').classes('mb-4')
            ui.label('Gerenciar Usuários').classes('text-xl font-semibold text-center')
