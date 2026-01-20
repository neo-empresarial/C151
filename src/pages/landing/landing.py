from nicegui import ui
from .components import header, navigation, footer
from src.common import theme

def landing_page():
    # Use flex-col with justify-between for better vertical spacing
    with ui.column().classes('w-full h-screen relative overflow-hidden bg-mica'):
        theme.render_theme_toggle_button()
        theme.render_close_button()
        
        # Header Section
        with ui.row().classes('w-full justify-center pt-16 pb-8 anim-enter'):
            header.render()
            
        # Main Navigation Cards - Centered
        with ui.column().classes('w-full flex-grow items-center justify-center'):
            navigation.render_cards()
            
        # Footer Section
        with ui.row().classes('w-full justify-center pb-6 anim-enter delay-300'):
            footer.render()
