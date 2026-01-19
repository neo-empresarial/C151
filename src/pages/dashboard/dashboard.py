from nicegui import ui
from . import functions as f
from .components import header, user_list
from .components.edit_dialog import EditDialog
from .components.add_dialog import AddDialog

def dashboard_page():
    with ui.column().classes('w-full h-screen bg-gray-100 p-8 relative'):
        ui.label("Demo Version | © Fundação Certi 2026").classes('absolute bottom-4 text-gray-400 text-xs')

        header.render(lambda: ui.navigate.to('/'))

        users_card = ui.card().classes('w11-card w-full p-4')
        with users_card:
            ui.label('Usuários Cadastrados').classes('text-lg font-semibold mb-4')
            users = f.get_all_users()
            user_list.render(users, lambda u: edit_dialog.open(u), lambda uid: delete_user(uid))

        ui.button('Adicionar Usuário', on_click=lambda: add_dialog.open()).classes('w11-btn bg-blue-600 text-white mt-4')

    async def delete_user(uid):
        f.delete_user_from_db(uid)
        ui.notify('Usuário removido')
        ui.navigate.reload()

    edit_dialog = EditDialog(on_user_updated=lambda: ui.navigate.reload())
    add_dialog = AddDialog(on_user_added=lambda: ui.navigate.reload())
