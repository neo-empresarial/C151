
class Colors:
    MICA_BG = "#f3f3f3"
    MICA_ALT = "#eeeeee"
    SURFACE = "#ffffff"
    
    PRIMARY = "#0067c0"
    PRIMARY_HOVER = "#187bcd"
    PRIMARY_PRESSED = "#005a9e"
    TEXT_ON_PRIMARY = "#ffffff"
    
    SUCCESS = "#107c10"
    WARNING = "#ffb900" 
    ERROR = "#c42b1c"   
    INFO = "#0067c0"
    
    TEXT_PRIMARY = "#202020"
    TEXT_SECONDARY = "#5d5d5d"
    TEXT_DISABLED = "#a19f9d"
    
    BORDER = "#e5e5e5"
    BORDER_FOCUS = "#0067c0"
    
    GLASS_WHITE = "rgba(255, 255, 255, 0.7)"
    GLASS_BLACK = "rgba(0, 0, 0, 0.6)"
    
    ACRYLIC_BG = "rgba(255, 255, 255, 0.5)"

class DarkColors:
    MICA_BG = "#202020"
    MICA_ALT = "#1a1a1a"
    SURFACE = "#2c2c2c"
    
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#d0d0d0"
    TEXT_DISABLED = "#707070"
    
    BORDER = "rgba(255, 255, 255, 0.08)"
    
    ACRYLIC_BG = "rgba(32, 32, 32, 0.6)"
    
    GLASS_WHITE = "rgba(255, 255, 255, 0.05)"
    GLASS_BLACK = "rgba(0, 0, 0, 0.8)"

class Fonts:
    MAIN = '"Segoe UI Variable Display", "Segoe UI", sans-serif'
    MONO = "Consolas, monospace"
    
    SIZE_SM = "12px"
    SIZE_MD = "14px"
    SIZE_LG = "18px"
    SIZE_XL = "24px"
    SIZE_XXL = "32px"

class Shapes:
    RADIUS_SM = "4px"
    RADIUS_MD = "8px"
    RADIUS_LG = "12px"
    RADIUS_XL = "16px"
    RADIUS_FULL = "9999px" 

STYLESHEET = f"""
    QWidget {{
        background-color: {Colors.MICA_BG};
        color: {Colors.TEXT_PRIMARY};
        font-family: "{Fonts.MAIN}";
        font-size: {Fonts.SIZE_MD};
    }}

    QLabel {{
        color: {Colors.TEXT_PRIMARY};
    }}
    
    QLabel#h1 {{
        font-size: {Fonts.SIZE_XXL};
        font-weight: 600;
    }}

    /* Card / Panel Look */
    QFrame, QGroupBox, QListWidget {{
        background-color: {Colors.SURFACE};
        border: 1px solid {Colors.BORDER};
        border-radius: {Shapes.RADIUS_MD};
    }}
    
    QWidget#transparent {{
        background-color: transparent;
        border: none;
    }}

    QGroupBox {{
        margin-top: 25px; 
        padding-top: 10px;
    }}

    QGroupBox::title {{
        subcontrol-origin: margin;
        top: 0px;
        left: 10px;
        padding: 0 5px;
        color: {Colors.TEXT_PRIMARY};
        font-weight: 600;
    }}

    /* Modern Buttons */
    QPushButton {{
        background-color: {Colors.SURFACE};
        border: 1px solid {Colors.BORDER};
        border-bottom: 1px solid #cccccc; 
        border-radius: {Shapes.RADIUS_SM};
        padding: 6px 20px;
        color: {Colors.TEXT_PRIMARY};
        font-weight: normal;
        min-height: 32px;
    }}

    QPushButton:hover {{
        background-color: #fbfbfb;
        border-color: #d0d0d0;
    }}

    QPushButton:pressed {{
        background-color: #f0f0f0;
        border-color: #c0c0c0;
        border-bottom-color: #c0c0c0;
        padding-top: 7px;
        padding-bottom: 5px;
    }}

    /* Primary Action Button */
    QPushButton#primary {{
        background-color: {Colors.PRIMARY};
        color: {Colors.TEXT_ON_PRIMARY};
        border: 1px solid {Colors.PRIMARY};
    }}
    
    QPushButton#primary:hover {{
        background-color: {Colors.PRIMARY_HOVER};
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
        background-color: #fff0f0;
        border-color: {Colors.ERROR};
    }}

    /* Inputs */
    QLineEdit {{
        background-color: {Colors.SURFACE};
        border: 1px solid {Colors.BORDER};
        border-bottom: 2px solid {Colors.BORDER}; 
        border-radius: {Shapes.RADIUS_SM};
        padding: 6px 10px;
        selection-background-color: {Colors.PRIMARY};
    }}
    
    QLineEdit:focus {{
        border-bottom-color: {Colors.PRIMARY};
        background-color: {Colors.SURFACE};
    }}

    QListWidget {{
        outline: none;
        padding: 5px;
    }}
    
    QListWidget::item {{
        border-radius: {Shapes.RADIUS_SM};
        padding: 8px;
        margin-bottom: 4px;
    }}
    
    QListWidget::item:selected {{
        background-color: #e5f1fb; 
        color: {Colors.TEXT_PRIMARY};
    }}
    QListWidget::item:hover {{
        background-color: #f0f0f0;
    }}
    
    QProgressBar {{
        border: none;
        background-color: #e0e0e0;
        border-radius: 2px;
        height: 4px;
        text-align: center;
    }}
    QProgressBar::chunk {{
        background-color: {Colors.PRIMARY};
        border-radius: 2px;
    }}
"""
