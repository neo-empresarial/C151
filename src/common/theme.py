from nicegui import ui, app
from src.common.styles import Colors, DarkColors, Fonts, Shapes, ANTIGRAVITY_THEME

def load_theme():
    ui.add_head_html(ANTIGRAVITY_THEME, shared=True)

_is_dark_mode = False

def render_theme_toggle_button():
    global _is_dark_mode
    is_dark = _is_dark_mode
    if is_dark:
        ui.run_javascript("document.body.classList.add('body--dark')")
    else:
        ui.run_javascript("document.body.classList.remove('body--dark')")

    def toggle_mode():
        global _is_dark_mode
        _is_dark_mode = not _is_dark_mode
        new_state = _is_dark_mode
        if new_state:
            ui.run_javascript("document.body.classList.add('body--dark')")
            btn.props('icon=light_mode')
            tooltip.text = "Modo Claro"
        else:
            ui.run_javascript("document.body.classList.remove('body--dark')")
            btn.props('icon=dark_mode')
            tooltip.text = "Modo Escuro"

    icon_name = 'light_mode' if is_dark else 'dark_mode'
    tooltip_text = "Modo Claro" if is_dark else "Modo Escuro"

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
    with ui.element('div').classes('fixed inset-0 z-[9999] flex items-center justify-center bg-white transition-opacity duration-700 pointer-events-none') as overlay:
        overlay.style('opacity: 1;') 
        ui.image('/public/images/certi/logo-certi.png').classes('w-64 animate-pulse')

    def fade_out():
        overlay.style('opacity: 0;')
        def safe_delete():
            try:
                overlay.delete()
            except Exception:
                pass
        ui.timer(0.7, safe_delete)

    ui.timer(2.0, fade_out)




