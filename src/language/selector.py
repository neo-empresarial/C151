from nicegui import ui
from src.common.state import state
from src.language.manager import language_manager as lm

def set_lang(lang):
    state.language = lang
    lm.set_language(lang)
    ui.navigate.reload()

def render():
    languages = [
        {'code': 'pt', 'name': 'Português', 'flag': 'src/public/images/country flags/Brazil.png'},
        {'code': 'en', 'name': 'English', 'flag': 'src/public/images/country flags/USA.svg'},
        {'code': 'es', 'name': 'Español', 'flag': 'src/public/images/country flags/Mexico.png'}
    ]

    current_flag = next((l['flag'] for l in languages if l['code'] == state.language), languages[0]['flag'])

    with ui.row().classes('fixed top-6 right-32 z-50 items-center'):
        with ui.button(icon='expand_more').props('flat round').classes('text-white opacity-80 hover:opacity-100 transition-opacity'):
                ui.image(current_flag).classes('w-6 h-4 object-contain mr-1')
                
                with ui.menu().classes('bg-black/90 border border-white/10 text-white shadow-xl backdrop-blur-md'):
                    for lang in languages:
                        with ui.menu_item(on_click=lambda l=lang['code']: set_lang(l)).classes('hover:bg-white/20 transition-colors gap-3'):
                            ui.image(lang['flag']).classes('w-6 h-4 object-contain')
                            ui.label(lang['name']).classes('text-sm font-light')
