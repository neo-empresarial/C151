from nicegui import ui

def render_inputs():
    ui.label('Configuração Inicial').classes('text-2xl font-bold mb-2')
    ui.label('Nenhum usuário encontrado. Crie o Administrador.').classes('text-gray-600 mb-6')
    name_input = ui.input('Nome do Admin').classes('w-full mb-4')
    pin_input = ui.input('PIN do Admin').classes('w-full mb-6')
    ui.label('Posicione-se para foto:').classes('font-bold mb-2')
    return name_input, pin_input
