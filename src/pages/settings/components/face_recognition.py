from nicegui import ui
from src.common.config import db_config
from src.language.manager import language_manager as lm

def render():
    with ui.column().classes('w-full p-2 pb-24'):
        config = db_config.config
        face_tech = config.get('face_tech', {})
        
        def save_settings():
            new_config = config.copy()
            save_tech = {
                "required_hits": int(slider_hits.value),
                "threshold": float(slider_thresh.value),
                "min_face_width": float(slider_width.value),
                "max_offset": float(slider_offset.value),
                "metric": face_tech['metric'],
                "model_name": face_tech['model_name']
            }
            new_config['face_tech'] = save_tech
            db_config.save_config(new_config)
            ui.notify(lm.t('data_updated'), type='positive')
            
        with ui.row().classes('w-full flex justify-between items-center mb-6'):
            ui.label(lm.t('face_recognition')).classes('text-2xl font-bold text-gray-800 dark:text-gray-100')
        
        select_props = 'outlined dense rounded options-dense behavior=menu input-class="text-gray-800 dark:text-gray-100" popup-content-class="bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-100"'
        
        with ui.row().classes('w-full gap-4 mb-6'):
            with ui.column().classes('flex-1'):
                ui.select(
                    options=['ArcFace', 'FaceNet', 'VGG-Face', 'OpenFace'],
                    value=face_tech.get('model_name', 'ArcFace'),
                    label=lm.t('model_name')
                ).classes('w-full').bind_value_to(face_tech, 'model_name').props(select_props).disable()
                
            with ui.column().classes('flex-1'):
                ui.select(
                    options=['cosine', 'euclidean', 'euclidean_l2'],
                    value=face_tech.get('metric', 'cosine'),
                    label=lm.t('metric')
                ).classes('w-full').bind_value_to(face_tech, 'metric').props(select_props).disable()

        ui.separator().classes('mb-6 opacity-30')

        ui.label(lm.t('required_hits')).classes('text-sm text-gray-600 dark:text-gray-400 font-medium')
        with ui.row().classes('w-full items-center gap-4 mb-6'):
            slider_hits = ui.slider(min=1, max=10, step=1, value=face_tech.get('required_hits', 1)).classes('flex-grow')
            slider_hits.bind_value_to(face_tech, 'required_hits')
            ui.label().bind_text_from(slider_hits, 'value').classes('w-8 font-bold')

        ui.label(lm.t('threshold')).classes('text-sm text-gray-600 dark:text-gray-400 font-medium')
        with ui.row().classes('w-full items-center gap-4 mb-6'):
            slider_thresh = ui.slider(min=0.0, max=1.0, step=0.01, value=face_tech.get('threshold', 0.28)).classes('flex-grow')
            slider_thresh.bind_value_to(face_tech, 'threshold')
            ui.label().bind_text_from(slider_thresh, 'value', backward=lambda x: f'{x:.2f}').classes('w-12 font-bold')

        ui.label(lm.t('min_face_width')).classes('text-sm text-gray-600 dark:text-gray-400 font-medium')
        with ui.row().classes('w-full items-center gap-4 mb-6'):
            slider_width = ui.slider(min=0.05, max=0.8, step=0.05, value=face_tech.get('min_face_width', 0.15)).classes('flex-grow')
            slider_width.bind_value_to(face_tech, 'min_face_width')
            ui.label().bind_text_from(slider_width, 'value', backward=lambda x: f'{x:.2f}').classes('w-12 font-bold')

        ui.label(lm.t('max_offset')).classes('text-sm text-gray-600 dark:text-gray-400 font-medium')
        with ui.row().classes('w-full items-center gap-4 mb-6'):
            slider_offset = ui.slider(min=0.05, max=0.5, step=0.01, value=face_tech.get('max_offset', 0.15)).classes('flex-grow')
            slider_offset.bind_value_to(face_tech, 'max_offset')
            ui.label().bind_text_from(slider_offset, 'value', backward=lambda x: f'{x:.2f}').classes('w-12 font-bold')

        
        
        ui.separator().classes('mb-6 opacity-30')

        ui.label(lm.t('access_levels')).classes('text-lg font-bold text-gray-800 dark:text-gray-100 mb-4')
        
        access_container = ui.row().classes('w-full gap-2 mb-4')
        access_levels = config.setdefault('access_levels', ["Admin", "Funcionário", "Visitante"])

        def remove_level(level):
            if level in access_levels:
                access_levels.remove(level)
                render_levels()

        def render_levels():
            access_container.clear()
            with access_container:
                for level in access_levels:
                    ui.chip(level, icon='person', on_click=lambda l=level: remove_level(l), removable=True).props('outline')

        render_levels()

        with ui.row().classes('w-full gap-2 items-center mb-6'):
            level_input = ui.input(placeholder=lm.t('access_levels')).classes('flex-grow').props('outlined dense rounded input-class="text-gray-800 dark:text-gray-100"')
            
            def add_level():
                val = level_input.value.strip()
                if val and val not in access_levels:
                    access_levels.append(val)
                    level_input.value = ''
                    render_levels()
            
            ui.button(icon='add', on_click=add_level).classes('bg-green-600 text-white').props('round dense un-elevated')

        with ui.row().classes('fixed bottom-0 left-64 right-0 p-4 bg-transparent backdrop-blur-sm border-t border-gray-200 dark:border-gray-700 shadow-xl z-50 justify-center items-center'):
            ui.button(lm.t('save_settings'), on_click=save_settings, icon='save').classes('bg-blue-600 hover:bg-blue-700 text-white font-bold px-6 py-2 shadow-lg').props('rounded')