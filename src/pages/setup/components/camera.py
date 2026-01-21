from nicegui import ui

def render_view():
    with ui.element('div').classes('relative w-full h-[300px] mb-6 bg-black rounded overflow-hidden'):
        cam_view = ui.interactive_image().classes('w-full h-full object-cover')
        ui.element('div').classes('absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[180px] h-[260px] border-2 border-white/50 rounded-[50%] pointer-events-none shadow-[0_0_0_9999px_rgba(0,0,0,0.5)]')
        return cam_view
