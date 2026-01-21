from nicegui import ui
from .components import header, navigation, footer
from src.common import theme
from src.common.state import state
from src.language.manager import language_manager as lm
from src.language import selector

def landing_page():
    lm.set_language(state.language)

    with ui.column().classes('w-full h-screen relative overflow-hidden bg-transparent justify-between'):
        theme.render_theme_toggle_button()
        theme.render_close_button()
        
        selector.render()

        with ui.row().classes('w-full justify-center pt-[10vh] anim-enter'):
            header.render()
            
        with ui.column().classes('w-full items-center justify-center anim-enter delay-200'):
            navigation.render_cards()
            
        with ui.row().classes('w-full justify-center pb-8 anim-enter delay-300'):
            footer.render()
