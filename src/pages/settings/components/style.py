from nicegui import ui

def render():
    with ui.card().classes('w-full p-6 bg-white/5 border border-white/10'):
        ui.label('Aparência e Estilo').classes('text-xl font-bold text-white mb-4')
        
        ui.switch('Modo Escuro (Forçado)', value=True).classes('text-white mb-4')
        
        ui.label('Tema de Cores').classes('text-white mb-2')
        ui.select(
            options=['Padrão (Azul)', 'Roxo', 'Verde', 'Vermelho', 'Laranja'],
            value='Padrão (Azul)',
            label='Selecione o tema'
        ).classes('w-full mb-4 text-white')
        
        ui.button('Salvar Aparência', on_click=lambda: ui.notify('Configurações de Estilo salvas (Simulado)')).classes('w-full mt-6 bg-purple-600 hover:bg-purple-700 text-white')
