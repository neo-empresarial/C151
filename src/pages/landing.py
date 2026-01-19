from nicegui import ui

def landing_page():
    with ui.column().classes('w-full h-screen items-center justify-center bg-gray-50 gap-8 relative'):
        ui.image('src/public/images/certi/logo-certi.png').classes('w-48 mb-4')
        
        ui.label('DeepFace Access Control').classes('text-4xl font-bold text-gray-800 mb-8')
        
        with ui.row().classes('gap-8'):
            with ui.card().classes('w11-card w-64 h-64 items-center justify-center cursor-pointer hover:bg-blue-50 transition-colors') \
                .on('click', lambda: ui.navigate.to('/recognition')):
                ui.icon('face', size='64px').classes('text-blue-600 mb-4')
                ui.label('Reconhecimento Facial').classes('text-xl font-semibold text-center')
            
            with ui.card().classes('w11-card w-64 h-64 items-center justify-center cursor-pointer hover:bg-green-50 transition-colors') \
                .on('click', lambda: ui.navigate.to('/dashboard')):
                ui.icon('admin_panel_settings', size='64px').classes('text-green-600 mb-4')
                ui.label('Gerenciar Usuários').classes('text-xl font-semibold text-center')

        ui.label("Demo Version | © Fundação Certi 2026").classes('absolute bottom-4 text-gray-500 text-sm')
