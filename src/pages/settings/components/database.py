from nicegui import ui
from src.common.config import db_config
from src.language.manager import language_manager as lm

def render():
    with ui.column().classes('w-full p-2 pb-24'):
        ui.label('Banco de Dados').classes('text-2xl font-bold text-gray-800 dark:text-gray-100 mb-6')
        
        from src.services.services import db_manager
        status = getattr(db_manager, 'active_db_type', 'unknown')
        
        status_color = 'green' if status == 'postgres' else 'orange' if status == 'sqlite' else 'red'
        status_text = 'Conectado: PostgreSQL (Nuvem)' if status == 'postgres' else 'Conectado: SQLite (Local)' if status == 'sqlite' else 'Modo de Segurança (Fallback)'
        
        with ui.card().classes(f'w-full mb-6 bg-{status_color}-100 dark:bg-{status_color}-900 border-{status_color}-500 border'):
            with ui.row().classes('items-center gap-2 p-2'):
                ui.icon('dns', size='md').classes(f'text-{status_color}-700 dark:text-{status_color}-300')
                with ui.column().classes('gap-0'):
                    ui.label('Status da Conexão').classes(f'text-xs font-bold text-{status_color}-800 dark:text-{status_color}-200')
                    ui.label(status_text).classes(f'text-sm text-{status_color}-900 dark:text-{status_color}-100')

        config = db_config.config
        
        input_props = 'outlined dense rounded input-class="text-gray-800 dark:text-gray-100"'
        select_props = 'outlined dense rounded options-dense behavior=menu input-class="text-gray-800 dark:text-gray-100" popup-content-class="bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-100"'


        from src.common.security import load_key
        try:
            current_key = load_key().decode()
        except:
             current_key = ""

        with ui.row().classes('items-center gap-2 mb-1 mt-4'):
             ui.label(lm.t('secret_key'))
             with ui.icon('help', size='xs').classes('text-gray-400 cursor-help'):
                    ui.tooltip(lm.t('desc_secret_key')).classes('bg-gray-800 text-white text-xs')
        
        secret_key_input = ui.input(
            value=current_key,
            password=True,
            password_toggle_button=True
        ).classes('w-full mb-6').props(input_props)

        with ui.row().classes('items-center gap-2 mb-1'):
             ui.label(lm.t('db_type'))

             with ui.icon('help', size='xs').classes('text-gray-400 cursor-help'):
                    ui.tooltip(lm.t('desc_db_type')).classes('bg-gray-800 text-white text-xs')
        db_type = ui.select(
            options=['sqlite', 'postgres'],
            value=config.get('type', 'sqlite'),
        ).classes('w-full mb-4').props(select_props)
        
        sqlite_container = ui.column().classes('w-full')
        with sqlite_container:
            with ui.row().classes('items-center gap-2 mb-1'):
                ui.label(lm.t('db_file'))
                with ui.icon('help', size='xs').classes('text-gray-400 cursor-help'):
                        ui.tooltip(lm.t('desc_db_file')).classes('bg-gray-800 text-white text-xs')
            host_input = ui.input(
                value=config.get('host', 'users.db')
            ).classes('w-full').props(input_props)

        postgres_container = ui.column().classes('w-full').bind_visibility_from(db_type, 'value', value='postgres')
        with postgres_container:
            with ui.row().classes('items-center gap-2 mb-1'):
                ui.label(lm.t('db_host'))
                with ui.icon('help', size='xs').classes('text-gray-400 cursor-help'):
                        ui.tooltip(lm.t('desc_db_host')).classes('bg-gray-800 text-white text-xs')
            pg_host = ui.input(
                value=config.get('host', 'localhost')
            ).classes('w-full').props(input_props)
            
            with ui.row().classes('items-center gap-2 mb-1'):
                ui.label(lm.t('db_port'))
                with ui.icon('help', size='xs').classes('text-gray-400 cursor-help'):
                        ui.tooltip(lm.t('desc_db_port')).classes('bg-gray-800 text-white text-xs')
            pg_port = ui.number(
                value=config.get('port', 5432),
                format='%.0f'
            ).classes('w-full').props(input_props)
            
            with ui.row().classes('items-center gap-2 mb-1'):
                ui.label(lm.t('db_name'))
                with ui.icon('help', size='xs').classes('text-gray-400 cursor-help'):
                        ui.tooltip(lm.t('desc_db_name')).classes('bg-gray-800 text-white text-xs')
            pg_db = ui.input(
                value=config.get('database', 'face_recognition_db')
            ).classes('w-full').props(input_props)

            with ui.row().classes('items-center gap-2 mb-1'):
                ui.label(lm.t('db_user'))
                with ui.icon('help', size='xs').classes('text-gray-400 cursor-help'):
                        ui.tooltip(lm.t('desc_db_user')).classes('bg-gray-800 text-white text-xs')
            pg_user = ui.input(
                value=config.get('user', 'postgres')
            ).classes('w-full').props(input_props)

            with ui.row().classes('items-center gap-2 mb-1'):
                ui.label(lm.t('db_pass'))
                with ui.icon('help', size='xs').classes('text-gray-400 cursor-help'):
                        ui.tooltip(lm.t('desc_db_pass')).classes('bg-gray-800 text-white text-xs')
            pg_password = ui.input(
                password=True,
                value=config.get('password', '')
            ).classes('w-full').props(input_props)

        def update_visibility():
            sqlite_container.set_visibility(db_type.value == 'sqlite')
            postgres_container.set_visibility(db_type.value == 'postgres')
        
        db_type.on_value_change(update_visibility)
        update_visibility()


        def save_db_settings():
            new_config = config.copy()
            new_config['type'] = db_type.value
            

            if db_type.value == 'sqlite':
                new_config['host'] = host_input.value
            else:
                new_config['host'] = pg_host.value
                new_config['port'] = int(pg_port.value)
                new_config['database'] = pg_db.value
                new_config['user'] = pg_user.value
                new_config['password'] = pg_password.value


            # Save Secret Key
            from src.common.security import save_secret_key
            if secret_key_input.value:
                 if not save_secret_key(secret_key_input.value):
                     ui.notify(lm.t('secret_key_invalid'), type='negative')
                     return


            from src.common.database import DatabaseManager
            ui.notify('Verificando conexão e schema...', type='info')
            
            success, msg = DatabaseManager.verify_and_setup_database(new_config)
            
            if success:
                db_config.save_config(new_config)
                db_manager.reload_engine() 
                ui.notify(f'Sucesso! {msg}', type='positive')
            else:
                ui.notify(f'Erro: {msg}', type='negative', multi_line=True, close_button=True)

        with ui.row().classes('fixed bottom-0 left-64 right-0 p-4 bg-transparent backdrop-blur-sm border-t border-gray-200 dark:border-gray-700 shadow-xl z-50 justify-center items-center'):
            ui.button(lm.t('save_database'), on_click=save_db_settings, icon='save').classes('bg-blue-600 hover:bg-blue-700 text-white font-bold px-6 py-2 shadow-lg').props('rounded')