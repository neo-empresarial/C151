from nicegui import ui

def render(users, on_edit, on_delete):
    with ui.grid(columns=4).classes('w-full gap-4'):
        ui.label('Nome').classes('font-bold opacity-60')
        ui.label('Nível').classes('font-bold opacity-60')
        ui.label('ID').classes('font-bold opacity-60')
        ui.label('Ações').classes('font-bold opacity-60')
        
        for u in users:
            ui.label(u['name'])
            ui.label(u['access_level'])
            ui.label(u['id'][:8] + '...')
            with ui.row():
                ui.button(icon='edit', on_click=lambda _, user=u: on_edit(user)).props('round flat dense').classes('text-blue-500 hover:bg-blue-500/10')
                ui.button(icon='delete', on_click=lambda _, uid=u['id']: on_delete(uid)).props('round flat dense').classes('text-red-500 hover:bg-red-500/10')
