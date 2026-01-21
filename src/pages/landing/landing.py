from nicegui import ui
from .components import header, navigation, footer
from src.common import theme
from src.common.state import state
from src.language.manager import language_manager as lm

def landing_page():
    # Sync manager with state
    lm.set_language(state.language)

    def set_lang(lang):
        state.language = lang
        lm.set_language(lang)
        ui.navigate.reload()

    # Languages data
    languages = [
        {'code': 'pt', 'name': 'Português', 'flag': 'src/public/images/country flags/Brazil.png'},
        {'code': 'en', 'name': 'English', 'flag': 'src/public/images/country flags/USA.svg'},
        {'code': 'es', 'name': 'Español', 'flag': 'src/public/images/country flags/Mexico.png'}
    ]

    current_flag = next((l['flag'] for l in languages if l['code'] == state.language), languages[0]['flag'])

    with ui.column().classes('w-full h-screen relative overflow-hidden bg-transparent justify-between'):
        theme.render_theme_toggle_button()
        theme.render_close_button()
        
        # Language Selector (Fixed Top Right, left of window controls)
        with ui.row().classes('fixed top-6 right-36 z-50 items-center'):
            with ui.button(icon='expand_more').props('flat round').classes('text-white opacity-80 hover:opacity-100 transition-opacity'):
                 ui.image(current_flag).classes('w-6 h-4 object-contain mr-1')
                 
                 with ui.menu().classes('bg-black/90 border border-white/10 text-white shadow-xl backdrop-blur-md'):
                     for lang in languages:
                         with ui.menu_item(on_click=lambda l=lang['code']: set_lang(l)).classes('hover:bg-white/20 transition-colors gap-3'):
                             ui.image(lang['flag']).classes('w-6 h-4 object-contain')
                             ui.label(lang['name']).classes('text-sm font-light')

        with ui.row().classes('w-full justify-center pt-[10vh] anim-enter'):
            header.render()
            
        with ui.column().classes('w-full items-center justify-center anim-enter delay-200'):
            navigation.render_cards()
            
        with ui.row().classes('w-full justify-center pb-8 anim-enter delay-300'):
            footer.render()
