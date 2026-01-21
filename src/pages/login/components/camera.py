from nicegui import ui
from .face_overlay import FaceOverlay

def render_view():
    with ui.column().classes('w-full aspect-video bg-black items-center justify-center relative overflow-hidden rounded-lg shadow-inner'):
        video_image = ui.interactive_image().classes('w-full h-full object-fill')
        face_overlay = FaceOverlay()
    return video_image, None, face_overlay
