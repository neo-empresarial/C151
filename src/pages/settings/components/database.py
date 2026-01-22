from nicegui import ui
from src.common.config import db_config

def render():
    with ui.column().classes('w-full p-2'):
        ui.label('Banco de Dados').classes('text-2xl font-bold text-gray-800 dark:text-gray-100 mb-6')
        
        # Connection Status Indicator
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
        
        db_type = ui.select(
            options=['sqlite', 'postgres'],
            value=config.get('type', 'sqlite'),
            label='Tipo de Banco'
        ).classes('w-full mb-4').props('outlined dense rounded options-dense behavior=menu input-class="text-gray-800 dark:text-gray-100" popup-content-class="bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-100"')
        
        sqlite_container = ui.column().classes('w-full')
        with sqlite_container:
            host_input = ui.input(
                label='Arquivo do Banco',
                value=config.get('host', 'users.db')
            ).classes('w-full').props('outlined dense rounded')

        postgres_container = ui.column().classes('w-full').bind_visibility_from(db_type, 'value', value='postgres')
        with postgres_container:
            pg_host = ui.input(
                label='Host',
                value=config.get('host', 'localhost')
            ).classes('w-full').props('outlined dense rounded')
            pg_port = ui.number(
                label='Porta',
                value=config.get('port', 5432),
                format='%.0f'
            ).classes('w-full').props('outlined dense rounded')
            pg_db = ui.input(
                label='Database',
                value=config.get('database', 'face_recognition_db')
            ).classes('w-full').props('outlined dense rounded')
            pg_user = ui.input(
                label='Usuário',
                value=config.get('user', 'postgres')
            ).classes('w-full').props('outlined dense rounded')
            pg_password = ui.input(
                label='Senha',
                password=True,
                value=config.get('password', '')
            ).classes('w-full').props('outlined dense rounded')

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

            from src.common.database import DatabaseManager
            ui.notify('Verificando conexão e schema...', type='info')
            
            # Use verify_and_setup_database to check connection AND init schema/migrations
            success, msg = DatabaseManager.verify_and_setup_database(new_config)
            
            if success:
                db_config.save_config(new_config)
                
                # HOT RELOAD: Reload the database manager instance to use the new config
                # The user query was "shit everything is being incorrectly selected", implying
                # the old engine was persisting. This fixes it.
                db_manager.reload_engine()
                
                ui.notify(f'Sucesso! {msg}', type='positive')
                
                # Optional: Force a page reload to refresh status indicators visually immediately
                # ui.open(ui.page.path) 
            else:
                ui.notify(f'Erro: {msg}', type='negative', multi_line=True, close_button=True)

        with ui.row().classes('fixed bottom-0 left-64 right-0 p-4 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 shadow-xl z-50 justify-end items-center'):
            ui.button('Salvar Banco de Dados', on_click=save_db_settings, icon='save').classes('bg-blue-600 hover:bg-blue-700 text-white font-bold px-6 py-2').props('rounded')
