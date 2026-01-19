from nicegui import ui

def render(users, on_edit, on_delete):
    with ui.grid(columns=4).classes('w-full gap-4'):
        ui.label('Nome').classes('font-bold text-gray-500')
        ui.label('Nível').classes('font-bold text-gray-500')
        ui.label('ID').classes('font-bold text-gray-500')
        ui.label('Ações').classes('font-bold text-gray-500')
        
        for u in users:
            ui.label(u['name'])
            ui.label(u['access_level'])
            ui.label(u['id'][:8] + '...')
            with ui.row():
                ui.button(icon='edit', on_click=lambda _, user=u: on_edit(user)).props('flat dense')
                ui.button(icon='delete', color='negative', on_click=lambda _, uid=u['id']: on_delete(uid)).props('flat dense')
