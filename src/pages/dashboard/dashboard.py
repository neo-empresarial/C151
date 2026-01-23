from nicegui import ui
from . import functions as f
from .components import header, user_list
from .components.edit_dialog import EditDialog
from .components.add_dialog import AddDialog
from src.common import theme
from src.language.manager import language_manager as lm

def dashboard_page():
    f.pause_engine()
    ui.timer(0.5, lambda: f.pause_engine(), once=True)
    with ui.column().classes('w-full h-screen p-0 relative overflow-y-auto bg-surface'):
        theme.render_theme_toggle_button()
        theme.render_window_controls()
        ui.label(lm.t('demo_footer')).classes('absolute bottom-4 left-8 opacity-50 text-white')

        header.render(lambda: ui.navigate.to('/'))

        with ui.column().classes('w-full p-8 gap-4'):
            users_card = ui.card().classes('w11-card w-full p-4 shrink-0')
            with users_card:
                ui.label(lm.t('registered_users')).classes('text-lg font-semibold mb-4')
                users = f.get_all_users()
                user_list.render(users, lambda u: edit_dialog.open(u), lambda uid: open_confirm_delete(uid))
            
            with ui.row().classes('w-full justify-end mt-4 mb-20'):
                 ui.button(lm.t('add_user'), on_click=lambda: add_dialog.open()).classes('w11-btn bg-primary text-white shadow-xl')

    confirm_dialog = ui.dialog()
    confirm_uid = {'value': None}

    with confirm_dialog, ui.card().classes('w11-card p-6 items-center text-center'):
        ui.label(lm.t('confirm_delete_user')).classes('text-xl font-bold mb-4')
        ui.label(lm.t('action_irreversible')).classes('text-sm opacity-70 mb-6')
        with ui.row().classes('w-full justify-center gap-4'):
            ui.button(lm.t('cancel'), on_click=confirm_dialog.close).classes('w11-btn')
            ui.button(lm.t('delete'), color='red', on_click=lambda: do_delete()).classes('w11-btn bg-red-500 text-white')

    async def do_delete():
        if confirm_uid['value']:
             confirm_dialog.close()
             f.delete_user_from_db(confirm_uid['value'])
             await f.reload_model_logic()
             ui.notify(lm.t('user_removed'), type='positive')
             ui.navigate.reload()

    def open_confirm_delete(uid):
        confirm_uid['value'] = uid
        confirm_dialog.open()
             
    ui.button(lm.t('add_user'), on_click=lambda: add_dialog.open()).classes('w11-btn bg-primary text-white mt-4 shadow-xl')

    edit_dialog = EditDialog(on_user_updated=lambda: ui.navigate.reload())
    add_dialog = AddDialog(on_user_added=lambda: ui.navigate.reload())
