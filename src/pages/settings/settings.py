from nicegui import ui
from src.common import theme
from src.language.manager import language_manager as lm
from src.pages.settings.components import database, face_recognition

def settings_page():
    lm.set_language('pt-br')
    with ui.row().classes('w-full h-screen relative overflow-hidden bg-transparent'):  
        with ui.column().classes('w-64 h-full bg-transparent border-r border-gray-200 dark:border-gray-700 p-4 flex-shrink-0 z-10 text-gray-900 dark:text-gray-100 transition-colors duration-300 gap-2'):  
            with ui.row().classes('w-full items-center mb-6'):
                ui.button(icon='arrow_back', on_click=lambda: ui.navigate.to('/')).classes('p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-600 dark:text-gray-300').props('flat round dense')
                ui.label(lm.t('settings')).classes('text-xl font-bold text-gray-800 dark:text-white ml-2')
            menu_container = ui.column().classes('w-full gap-2')
            ui.space()
            with ui.row().classes('w-full justify-center mb-4'):
                theme.render_theme_toggle_button()
                
        content_area = ui.column().classes('flex-1 h-full overflow-y-auto p-8 relative scroll-smooth')
        menu_buttons = []

        def show_content(component, btn_id):
            content_area.clear()    
            for btn in menu_buttons:
                if btn._id == btn_id:
                     btn.classes('bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300', remove='text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700')
                else:
                     btn.classes('text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700', remove='bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300')
            with content_area:
                component.render()
        
        def create_menu_item(label, icon, component, default=False):
            with menu_container:
                    btn = ui.button(label, icon=icon, on_click=lambda b: show_content(component, b.sender._id)).props('flat align=left no-caps').classes('w-full rounded-lg px-4 py-2 font-medium text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors')
                    btn._id = btn.id 
                    menu_buttons.append(btn)                   
            if default:
                ui.timer(0.0, lambda: show_content(component, btn.id), once=True)
        create_menu_item(lm.t('face_recognition'), 'face', face_recognition, default=True)
        create_menu_item(lm.t('configure_database'), 'dns', database)    
