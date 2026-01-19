from nicegui import ui
from src.common.styles import Colors

class FaceOverlay:
    def __init__(self):
        # Container for the box
        # We use absolute positioning. The parent must be relative.
        self.box = ui.element('div').classes('absolute border-2 transition-all duration-200 ease-out').style(
            'border-color: transparent; pointer-events: none; box-shadow: 0 0 15px rgba(0,0,0,0.2);'
        )
        
        # Label for the name/status
        with self.box:
            self.label_container = ui.row().classes('absolute -top-8 left-0 shadow-sm rounded px-2 py-1 transition-colors duration-200').style(
                'background-color: transparent;'
            )
            with self.label_container:
                self.label_text = ui.label('').classes('text-xs font-bold text-white')

        self.visible = False

    def update(self, result, mirror=False):
        """
        Updates the overlay position using percentage-based coordinates.
        This ensures alignment regardless of the video container's actual size (responsive).
        
        Args:
            result (dict): Inference result containing 'box' (x, y, w, h) normalized to 0.0-1.0 range.
                           The caller MUST normalize these before calling update.
            mirror (bool): Whether to mirror the X position (for selfie view).
        """
        if not result:
            self.hide()
            return

        # Expecting normalized coordinates (0.0 to 1.0)
        x_pct, y_pct, w_pct, h_pct = result['box']
        
        if mirror:
            # Mirror X: (1.0 - x - w)
            x_pct = 1.0 - x_pct - w_pct

        # Validate bounds
        if w_pct <= 0 or h_pct <= 0:
            self.hide()
            return
            
        color = Colors.WARNING # Default/Scanning
        bg_color = Colors.WARNING
        status_text = "Analisando..."

        if result.get('known'):
            color = Colors.SUCCESS
            bg_color = Colors.SUCCESS
            status_text = result.get('name', 'Desconhecido')
        else:
            if result.get('in_roi', False):
                 # In ROI but unknown -> RED
                 color = Colors.ERROR
                 bg_color = Colors.ERROR
                 status_text = "Desconhecido"
            else:
                 # Not in ROI -> Yellow/Scanning
                 color = Colors.WARNING 
                 bg_color = Colors.WARNING
                 status_text = "Centralize"

        # Apply styles using percentages
        self.box.style(f'''
            left: {x_pct * 100}%; 
            top: {y_pct * 100}%; 
            width: {w_pct * 100}%; 
            height: {h_pct * 100}%; 
            border-color: {color};
            display: block;
        ''')
        
        self.label_container.style(f'background-color: {color};')
        self.label_text.text = status_text
        self.visible = True

    def hide(self):
        if self.visible:
            self.box.style('display: none;')
            self.visible = False
