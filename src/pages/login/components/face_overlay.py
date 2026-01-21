from nicegui import ui
from src.common.styles import Colors

class FaceOverlay:
    def __init__(self):
        self.box = ui.element('div').classes('absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 transition-all duration-300 ease-out').style(
            'width: 280px; height: 350px; border-radius: 45%; border: 4px solid transparent; box-shadow: 0 0 0 9999px rgba(0,0,0,0.5); pointer-events: none;'
        )
        
        with self.box:
            self.label_container = ui.row().classes('absolute -bottom-16 left-1/2 transform -translate-x-1/2 shadow-lg rounded-full px-6 py-2 transition-colors duration-300').style(
                'background-color: rgba(0,0,0,0.7); min-width: 200px; justify-content: center; align-items: center;'
            )
            with self.label_container:
                self.label_text = ui.label('Posicione a face no centro').classes('text-lg font-bold text-white text-center')

        self.visible = True 

    def _apply_style(self, color):
        self.box.style(
            f'width: 280px; height: 350px; border-radius: 45%; border: 4px solid {color}; box-shadow: 0 0 0 9999px rgba(0,0,0,0.6);'
        )
        self.label_container.style(f'background-color: {color};')

    def set_state(self, text, color):
        self.label_text.text = text
        self._apply_style(color)
        self.visible = True

    def update(self, result, text=None, color=None, mirror=False):
        final_text = text if text else "Posicione a face no centro"
        final_color = color if color else Colors.WARNING
        
        self.label_text.text = final_text
        self._apply_style(final_color)

    def hide(self):
        pass
