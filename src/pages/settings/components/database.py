from nicegui import ui
from src.common.config import db_config

def render():
    with ui.column().classes('w-full p-2'):
        ui.label('Banco de Dados').classes('text-2xl font-bold text-gray-800 dark:text-gray-100 mb-6')
        
        config = db_config.config
        
        db_type = ui.select(
            options=['sqlite', 'postgres'],
            value=config.get('type', 'sqlite'),
            label='Tipo de Banco'
        ).classes('w-full mb-4').props('outlined dense rounded')
        
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

            db_config.save_config(new_config)
            ui.notify('Configurações de Banco de Dados salvas!', type='positive')

        ui.button('Salvar Banco de Dados', on_click=save_db_settings).classes('w-full mt-4 bg-blue-600 hover:bg-blue-700 text-white')
