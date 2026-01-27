from nicegui import ui, app
from src.common.styles import Colors, DarkColors, Fonts, Shapes, ANTIGRAVITY_THEME

def load_theme():
    ui.add_head_html(ANTIGRAVITY_THEME, shared=True)

class ThemeState:
    def __init__(self):
        self._is_dark = False
        self._listeners = []

    @property
    def is_dark(self):
        return self._is_dark

    @is_dark.setter
    def is_dark(self, value):
        if self._is_dark != value:
            self._is_dark = value
            for listener in list(self._listeners):
                try:
                    listener(value)
                except Exception:
                    pass 

    def add_listener(self, listener):
        self._listeners.append(listener)
        listener(self._is_dark)

    def remove_listener(self, listener):
        if listener in self._listeners:
            self._listeners.remove(listener)

theme_state = ThemeState()

def apply_theme():
    if theme_state.is_dark:
        ui.run_javascript("document.body.classList.add('body--dark')")
    else:
        ui.run_javascript("document.body.classList.remove('body--dark')")

def render_theme_toggle_button():
    def toggle_mode():
        theme_state.is_dark = not theme_state.is_dark
        if theme_state.is_dark:
            btn.props('icon=light_mode')
            tooltip.text = "Modo Claro"
        else:
            btn.props('icon=dark_mode')
            tooltip.text = "Modo Escuro"
        
        apply_theme()
        btn.update()

    apply_theme()

    icon_name = 'light_mode' if theme_state.is_dark else 'dark_mode'
    tooltip_text = "Modo Claro" if theme_state.is_dark else "Modo Escuro"

    with ui.button(icon=icon_name, on_click=toggle_mode).classes('fixed bottom-8 right-8 z-50 rounded-full anim-enter delay-300').props('round flat type=a') as btn:
        btn.style('width: 64px; height: 64px; background: rgba(125,125,125,0.1); backdrop-filter: blur(20px); color: var(--text-primary); box-shadow: 0 8px 32px rgba(0,0,0,0.1); transition: transform 0.3s ease;')
        tooltip = ui.tooltip(tooltip_text)

def render_window_controls():
    with ui.row().classes('fixed top-6 right-6 z-50 gap-2 items-center anim-enter delay-300'):
        async def toggle_fullscreen():
            if app.native.main_window:
                app.native.main_window.toggle_fullscreen()
            else:
                 await ui.run_javascript('''
                    if (!document.fullscreenElement) {
                        document.documentElement.requestFullscreen();
                    } else {
                        if (document.exitFullscreen) {
                            document.exitFullscreen();
                        }
                    }
                ''')
            
        with ui.button(icon='fullscreen', on_click=toggle_fullscreen).classes('rounded-full').props('round flat'):
            ui.tooltip('Alternar Tela Cheia')
            
        with ui.button(icon='close', on_click=app.shutdown).classes('rounded-full').props('round flat'):
             ui.tooltip('Sair do Sistema')

def render_back_button(target_url: str):
    with ui.button(icon='arrow_back', on_click=lambda: ui.navigate.to(target_url)).classes('fixed top-6 left-6 z-50 rounded-full w-12 h-12 bg-white/10 hover:bg-white/20 text-white backdrop-blur-md transition-colors'):
        ui.tooltip('Voltar')

render_close_button = render_window_controls

def loading_overlay():
    with ui.element('div').classes('fixed inset-0 z-[10000] flex flex-col items-center justify-center bg-slate-50 transition-opacity duration-1000') as overlay:
        overlay.style('opacity: 1;') 
        
        img = ui.image().classes('w-64 animate-pulse mb-4')
        
        ui.label('Carregando...').classes('text-gray-500 font-medium animate-pulse')
        
        def update_logo_overlay(is_dark):
            img.source = '/src/public/images/certi/logo-certi-2.png' if is_dark else '/src/public/images/certi/logo-certi.png'
            if is_dark:
                overlay.classes(remove='bg-slate-50', add='bg-gray-900')
            else:
                overlay.classes(remove='bg-gray-900', add='bg-slate-50')
            img.update()
            
        theme_state.add_listener(update_logo_overlay)
        
    def fade_out():
        overlay.style('opacity: 0;')
        def safe_delete():
            try:
                theme_state.remove_listener(update_logo_overlay)
                overlay.delete()
            except Exception:
                pass
        ui.timer(0.7, safe_delete)

    ui.timer(2.0, fade_out)




