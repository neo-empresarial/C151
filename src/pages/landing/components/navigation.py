from nicegui import ui

def render_cards():
    with ui.row().classes('gap-12'):
        # Glass Card 1 - Recognition
        with ui.card().classes('w11-card w-[340px] h-[340px] items-center justify-center cursor-pointer group') \
            .on('click', lambda: ui.navigate.to('/recognition')):
            
            # Icon with Glow
            with ui.column().classes('items-center justify-center transition-transform duration-300 group-hover:-translate-y-2'):
                ui.icon('face', size='84px', color='white').classes('mb-6 opacity-90 drop-shadow-lg')
                ui.label('Reconhecimento Facial').classes('text-2xl font-light text-center tracking-wide')
                ui.label('Iniciar acesso seguro').classes('text-sm opacity-60 mt-2 font-light')

        # Glass Card 2 - Dashboard
        with ui.card().classes('w11-card w-[340px] h-[340px] items-center justify-center cursor-pointer group') \
            .on('click', lambda: ui.navigate.to('/dashboard')):
            
            with ui.column().classes('items-center justify-center transition-transform duration-300 group-hover:-translate-y-2'):
                ui.icon('space_dashboard', size='84px', color='white').classes('mb-6 opacity-90 drop-shadow-lg')
                ui.label('Painel de Controle').classes('text-2xl font-light text-center tracking-wide')
                ui.label('Gerenciar usuários e logs').classes('text-sm opacity-60 mt-2 font-light')
