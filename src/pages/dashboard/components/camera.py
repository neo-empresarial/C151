from nicegui import ui

def render_view():
    card = ui.element('div').classes('w-full h-full relative overflow-hidden rounded-2xl shadow-xl')
    
    with card:
        cam_view = ui.interactive_image().classes('w-full h-full object-cover')
        
        with ui.element('div').classes('absolute inset-0 pointer-events-none flex items-center justify-center'):
            ui.element('div').classes('w-[280px] h-[380px] border border-white/40 rounded-[3rem] shadow-[0_0_20px_rgba(0,0,0,0.2)]')
            
    return card, cam_view
