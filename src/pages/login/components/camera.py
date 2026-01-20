from nicegui import ui
from .face_overlay import FaceOverlay

def render_view():
    with ui.column().classes('w-full aspect-video bg-black items-center justify-center relative overflow-hidden rounded-lg shadow-inner'):
        # Video Feed
        # Note: We don't flip the video here via CSS because it complicates the overlay positioning calculation.
        # We will flip the frame in Python before sending to UI, OR we handle the flip logic in the overlay.
        # Decision: Let's keep the video element simple. The python loop usually sends FLIPPED frames (mirror effect).
        video_image = ui.interactive_image().classes('w-full h-full object-fill')
        
        # New Overlay Component
        face_overlay = FaceOverlay()
        
        # Static Guide / Viewfinder
        # Centered box to indicate where the user should position their face
        # The shadow creates the dimmed background effect (mask)
        ui.element('div').classes(
            'absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 '
            'w-[280px] h-[350px] border-2 border-dashed border-white/30 rounded-[40%] pointer-events-none z-0 '
            'shadow-[0_0_0_9999px_rgba(0,0,0,0.45)]'
        )
        
        # Bottom Feedback Label (Floating pill)
        feedback_label = ui.label('Inicializando...').classes(
            'absolute bottom-6 left-1/2 transform -translate-x-1/2 '
            'px-6 py-2 rounded-full text-lg font-medium backdrop-blur-md z-10 '
            'transition-colors duration-300 shadow-lg'
        ).style('background-color: rgba(0,0,0,0.6); color: white;')
        
    return video_image, feedback_label, face_overlay
