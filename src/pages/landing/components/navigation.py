from nicegui import ui

def render_cards():
    with ui.row().classes('gap-8'):
        with ui.card().classes('w11-card w-64 h-64 items-center justify-center cursor-pointer hover:bg-blue-50 transition-colors') \
            .on('click', lambda: ui.navigate.to('/recognition')):
            ui.icon('face', size='64px').classes('text-blue-600 mb-4')
            ui.label('Reconhecimento Facial').classes('text-xl font-semibold text-center')
        
        with ui.card().classes('w11-card w-64 h-64 items-center justify-center cursor-pointer hover:bg-green-50 transition-colors') \
            .on('click', lambda: ui.navigate.to('/dashboard')):
            ui.icon('admin_panel_settings', size='64px').classes('text-green-600 mb-4')
            ui.label('Gerenciar Usuários').classes('text-xl font-semibold text-center')
