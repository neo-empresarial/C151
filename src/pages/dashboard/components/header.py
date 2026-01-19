from nicegui import ui

def render(on_logout):
    with ui.row().classes('w-full justify-between items-center mb-6'):
        with ui.row().classes('items-center gap-4'):
            ui.image('src/public/images/certi/logo-certi.png').classes('h-12 w-auto object-contain')
            ui.label('Painel Administrativo').classes('text-2xl font-bold text-gray-800')
        ui.button('Sair', on_click=on_logout).classes('w11-btn bg-red-600 text-white')
