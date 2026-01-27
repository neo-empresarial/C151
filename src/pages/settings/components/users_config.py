from nicegui import ui
from src.common.config import db_config
from src.language.manager import language_manager as lm

def render():
    with ui.column().classes('w-full p-2 pb-24'):
        config = db_config.config
        face_tech = config.get('face_tech', {})
        
        def save_settings():
            new_config = config.copy()
            current_tech = new_config.get('face_tech', {})
            current_tech['check_similarity'] = switch_similarity.value
            
            new_config['face_tech'] = current_tech
            db_config.save_config(new_config)
            ui.notify(lm.t('data_updated'), type='positive')
            
        with ui.row().classes('w-full flex justify-between items-center mb-6'):
            ui.label(lm.t('user_management')).classes('text-2xl font-bold text-gray-800 dark:text-gray-100')
        
        ui.label(lm.t('security_settings')).classes('text-lg font-bold text-gray-700 dark:text-gray-300 mb-4')

        with ui.card().classes('w-full p-4 mb-4 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700'):
            with ui.row().classes('w-full flex justify-between items-center'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('verified_user').classes('text-blue-600 dark:text-blue-400')
                    ui.label(lm.t('verify_similarity')).classes('text-base font-medium text-gray-800 dark:text-gray-200')
                    with ui.icon('help', size='sm').classes('text-gray-400 cursor-help'):
                         ui.tooltip(lm.t('desc_verify_similarity')).classes('bg-gray-800 text-white text-xs')
                
                switch_similarity = ui.switch(value=face_tech.get('check_similarity', False)).props('color=blue')

        with ui.row().classes('fixed bottom-0 left-64 right-0 p-4 bg-transparent backdrop-blur-sm border-t border-gray-200 dark:border-gray-700 shadow-xl z-50 justify-center items-center'):
            ui.button(lm.t('save_settings'), on_click=save_settings, icon='save').classes('bg-blue-600 hover:bg-blue-700 text-white font-bold px-6 py-2 shadow-lg').props('rounded')
