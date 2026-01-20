
class Colors:
    MICA_BG = "#FFFFFF" # Pure white for light mode
    MICA_ALT = "#F8F9FA" 
    # Translucent Surface for Glassmorphism
    SURFACE = "rgba(255, 255, 255, 0.65)" 
    
    PRIMARY = "#121317" 
    PRIMARY_HOVER = "#3C4043" 
    PRIMARY_PRESSED = "#000000"
    TEXT_ON_PRIMARY = "#FFFFFF"
    
    SUCCESS = "#1E8E3E"
    WARNING = "#F9AB00"
    ERROR = "#D93025"
    INFO = "#1A73E8"
    
    TEXT_PRIMARY = "#121317"
    TEXT_SECONDARY = "#5F6368"
    TEXT_DISABLED = "#BDC1C6"
    
    # Very subtle, hairline borders
    BORDER = "rgba(0, 0, 0, 0.08)"
    BORDER_FOCUS = "#1A73E8"
    
    GLASS_WHITE = "rgba(255, 255, 255, 0.8)"
    GLASS_BLACK = "rgba(0, 0, 0, 0.6)"
    
    ACRYLIC_BG = "rgba(255, 255, 255, 0.65)"

class DarkColors:
    MICA_BG = "#101010" # Deeper black for high contrast
    MICA_ALT = "#1C1C1C"
    # Translucent Dark Surface
    SURFACE = "rgba(30, 30, 30, 0.60)" 
    
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#E8EAED"
    TEXT_DISABLED = "#9AA0A6"
    
    # Subtle dark mode border
    BORDER = "rgba(255, 255, 255, 0.08)"
    
    ACRYLIC_BG = "rgba(20, 20, 20, 0.7)"
    
    GLASS_WHITE = "rgba(255, 255, 255, 0.08)"
    GLASS_BLACK = "rgba(0, 0, 0, 0.8)"

class Fonts:
    # Prefer Google Sans if available, then Inter, then Segoe UI
    MAIN = '"Google Sans", "Inter", "Segoe UI Variable Display", "Segoe UI", sans-serif'
    MONO = '"Roboto Mono", "Consolas", monospace'
    
    SIZE_SM = "12px"
    SIZE_MD = "14px"
    SIZE_LG = "18px"
    SIZE_XL = "24px"
    SIZE_XXL = "48px" # Even Larger headers
    SIZE_DISPLAY = "80px"

class Shapes:
    RADIUS_SM = "8px"
    RADIUS_MD = "16px"
    RADIUS_LG = "24px" 
    RADIUS_XL = "32px"
    RADIUS_FULL = "9999px"

STYLESHEET = f"""
    QWidget {{
        background-color: {Colors.MICA_BG};
        color: {Colors.TEXT_PRIMARY};
        font-family: {Fonts.MAIN};
        font-size: {Fonts.SIZE_MD};
    }}

    /* Global Animations */
    QWidget {{
        /* Qt Stylesheets don't support full CSS transitions, but we can set properties */
    }}

    QLabel {{
        color: {Colors.TEXT_PRIMARY};
    }}
    
    QLabel#h1 {{
        font-size: {Fonts.SIZE_XXL};
        font-weight: 450; 
        letter-spacing: -1px;
    }}

    /* Card / Panel Look */
    /* Note: Glassmorphism is handled via CSS in theme.py, this is fallback/base */
    QFrame, QGroupBox, QListWidget {{
        background-color: {Colors.SURFACE};
        border: 1px solid {Colors.BORDER};
        border-radius: {Shapes.RADIUS_LG};
    }}
    
    QWidget#transparent {{
        background-color: transparent;
        border: none;
    }}

    QGroupBox {{
        margin-top: 30px; 
        padding-top: 15px;
    }}

    QGroupBox::title {{
        subcontrol-origin: margin;
        top: 0px;
        left: 15px;
        padding: 0 5px;
        color: {Colors.TEXT_PRIMARY};
        font-weight: 500;
    }}

    /* Modern Buttons - Pill Shape & Physics */
    QPushButton {{
        background-color: {Colors.SURFACE};
        border: 1px solid {Colors.BORDER};
        border-radius: {Shapes.RADIUS_FULL};
        padding: 8px 24px;
        color: {Colors.TEXT_PRIMARY};
        font-weight: 500;
        min-height: 48px; /* Taller clickable area */
    }}

    QPushButton:hover {{
        background-color: rgba(0, 0, 0, 0.05);
        border-color: {Colors.BORDER};
    }}

    QPushButton:pressed {{
        background-color: rgba(0, 0, 0, 0.1);
        padding-top: 9px;
        padding-bottom: 7px;
    }}

    /* Primary Action Button */
    QPushButton#primary {{
        background-color: {Colors.PRIMARY};
        color: {Colors.TEXT_ON_PRIMARY};
        border: 1px solid {Colors.PRIMARY};
    }}
    
    QPushButton#primary:hover {{
        background-color: {Colors.PRIMARY_HOVER};
        border-color: {Colors.PRIMARY_HOVER};
    }}
    
    QPushButton#primary:pressed {{
        background-color: {Colors.PRIMARY_PRESSED};
        border-color: {Colors.PRIMARY_PRESSED};
    }}

    /* Danger Button */
    QPushButton#danger {{
        background-color: {Colors.SURFACE};
        color: {Colors.ERROR};
        border: 1px solid {Colors.BORDER};
    }}
    QPushButton#danger:hover {{
        background-color: #FEF7F7;
        border-color: {Colors.ERROR};
    }}

    /* Inputs */
    QLineEdit {{
        background-color: rgba(255, 255, 255, 0.5); /* Semi-transparent input */
        border: 1px solid {Colors.BORDER};
        border-radius: {Shapes.RADIUS_FULL}; /* Fully rounded inputs matching buttons */
        padding: 10px 20px;
        selection-background-color: {Colors.INFO};
    }}
    
    QLineEdit:focus {{
        border: 1px solid {Colors.BORDER_FOCUS};
        background-color: #FFFFFF;
    }}

    QListWidget {{
        outline: none;
        padding: 8px;
    }}
    
    QListWidget::item {{
        border-radius: {Shapes.RADIUS_MD};
        padding: 12px;
        margin-bottom: 4px;
    }}
    
    QListWidget::item:selected {{
        background-color: rgba(26, 115, 232, 0.1); 
        color: {Colors.INFO};
    }}
    QListWidget::item:hover {{
        background-color: rgba(0, 0, 0, 0.03);
    }}
    
    QProgressBar {{
        border: none;
        background-color: rgba(0, 0, 0, 0.1);
        border-radius: 4px;
        height: 6px;
        text-align: center;
    }}
    QProgressBar::chunk {{
        background-color: {Colors.INFO};
        border-radius: 4px;
    }}
"""
