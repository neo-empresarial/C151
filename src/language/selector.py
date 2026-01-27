import os
from nicegui import ui
from src.common.state import state
from src.language.manager import language_manager as lm

def set_lang(lang):
    state.language = lang
    lm.set_language(lang)
    ui.navigate.reload()

def render():
    languages = []
    url_base_path = '/public/images/country_flags'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    fs_base_path = os.path.join(os.path.dirname(current_dir), 'public', 'images', 'country_flags')
    
    for code, data in lm.languages.items():
        fs_path = os.path.join(fs_base_path, f'{code}.png')
        flag_url = f'{url_base_path}/{code}.png'
        
        if not os.path.exists(fs_path):
             fs_path = os.path.join(fs_base_path, f'{code}.svg')
             flag_url = f'{url_base_path}/{code}.svg'
             
             if not os.path.exists(fs_path):
                 flag_url = f'{url_base_path}/default.png'
        
        languages.append({
            'code': code,
            'name': data.get('language', code.upper()),
            'flag': flag_url
        })

    current_lang_obj = next((l for l in languages if l['code'] == state.language), None)
    if current_lang_obj:
        current_flag = current_lang_obj['flag']
    else:
        current_flag = languages[0]['flag'] if languages else f'{url_base_path}/default.png'

    with ui.row().classes('fixed top-6 right-32 z-50 items-center'):
        with ui.button(icon='expand_more').props('flat round').classes('text-white opacity-80 hover:opacity-100 transition-opacity'):
                ui.image(current_flag).classes('w-6 h-4 object-contain mr-1')
                
                with ui.menu().classes('bg-black/90 border border-white/10 text-white shadow-xl backdrop-blur-md'):
                    for lang in languages:
                        with ui.menu_item(on_click=lambda l=lang['code']: set_lang(l)).classes('hover:bg-white/20 transition-colors gap-3'):
                            ui.image(lang['flag']).classes('w-6 h-4 object-contain')
                            ui.label(lang['name']).classes('text-sm font-light')
