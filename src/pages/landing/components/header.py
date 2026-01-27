from nicegui import ui
from src.common.theme import theme_state

def render():
    img = ui.image().classes('w-64 mb-1')
    
    def update_logo(is_dark):
        if img.is_deleted:
            try:
                theme_state.remove_listener(update_logo)
            except ValueError:
                pass
            return
        img.source = 'src/public/images/certi/logo-certi-2.png' if is_dark else 'src/public/images/certi/logo-certi.png'
        img.update()

    theme_state.add_listener(update_logo)


