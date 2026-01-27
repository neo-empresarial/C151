from nicegui import ui

def render_view():
    with ui.card().classes('w-full aspect-video p-0 mb-6 bg-black relative overflow-hidden group shadow-xl rounded-2xl border-0'):
        cam_view = ui.interactive_image().classes('w-full h-full object-cover')
        with ui.element('div').classes('absolute inset-0 pointer-events-none flex items-center justify-center'):
            with ui.element('div').classes('relative w-48 h-64 border-2 border-white/30 rounded-[3rem] overflow-hidden'):
                ui.element('div').classes('w-full h-1 bg-blue-500/50 shadow-[0_0_15px_rgba(59,130,246,0.5)] animate-scan top-0 absolute')
            
    return cam_view
