from nicegui import ui

def render_overlay():
    ui.element('div').classes('absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[220px] h-[320px] border-2 border-white/50 rounded-[50%] pointer-events-none shadow-[0_0_0_9999px_rgba(0,0,0,0.5)]')
    ui.element('div').classes('absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[220px] h-[320px] border-2 border-white/50 rounded-[50%] pointer-events-none shadow-[0_0_0_9999px_rgba(0,0,0,0.5)]')

def render_view():
    with ui.column().classes('w-full h-[500px] bg-black items-center justify-center relative overflow-hidden'):
        video_image = ui.interactive_image().classes('w-full h-full object-cover')
        render_overlay()
        feedback_label = ui.label('Inicializando...').classes('absolute bottom-4 left-1/2 transform -translate-x-1/2 bg-black/60 text-white px-6 py-2 rounded-full text-lg font-medium backdrop-blur-sm z-10')
    return video_image, feedback_label
