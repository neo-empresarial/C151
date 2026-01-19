

BG_COLOR = "#f9f9f9"      
PANEL_COLOR = "#ffffff"   
TEXT_COLOR = "#1a1a1a"    
ACCENT_COLOR = "#0067c0"  
SUCCESS_COLOR = "#107c10"
DANGER_COLOR = "#c42b1c"
BORDER_COLOR = "#e5e5e5"
SIDEBAR_COLOR = "#f3f3f3" 

MAIN_FONT = "Segoe UI Variable Display, Segoe UI, sans-serif"
FONT_SIZE_NORMAL = "14px"
FONT_SIZE_HEADER = "20px"
FONT_SIZE_TITLE = "28px"

STYLESHEET = f"""
    QWidget {{
        background-color: {BG_COLOR};
        color: {TEXT_COLOR};
        font-family: "{MAIN_FONT}";
        font-size: {FONT_SIZE_NORMAL};
    }}

    QLabel {{
        color: {TEXT_COLOR};
    }}
    
    QLabel#h1 {{
        font-size: {FONT_SIZE_TITLE};
        font-weight: 600;
    }}

    /* Card / Panel Look */
    QFrame, QGroupBox, QListWidget {{
        background-color: {PANEL_COLOR};
        border: 1px solid {BORDER_COLOR};
        border-radius: 8px;
    }}
    
    /* Remove border for specific containers if needed */
    QWidget#transparent {{
        background-color: transparent;
        border: none;
    }}

    QGroupBox {{
        margin-top: 25px; /* Leave space for title */
        padding-top: 10px;
    }}

    QGroupBox::title {{
        subcontrol-origin: margin;
        top: 0px;
        left: 10px;
        padding: 0 5px;
        color: {TEXT_COLOR};
        font-weight: 600;
    }}

    /* Modern Buttons */
    QPushButton {{
        background-color: {PANEL_COLOR};
        border: 1px solid {BORDER_COLOR};
        border-bottom: 1px solid #cccccc; /* Slight depth */
        border-radius: 4px;
        padding: 6px 20px;
        color: {{TEXT_COLOR}};
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
        padding-top: 7px; /* pressed effect */
        padding-bottom: 5px;
    }}

    /* Primary Action Button (Accent) */
    QPushButton#primary {{
        background-color: {ACCENT_COLOR};
        color: white;
        border: 1px solid {ACCENT_COLOR};
    }}
    
    QPushButton#primary:hover {{
        background-color: #187bcd; /* Slightly lighter */
    }}
    
    QPushButton#primary:pressed {{
        background-color: #005a9e; /* Slightly darker */
        border-color: #005a9e;
    }}

    /* Danger Button */
    QPushButton#danger {{
        background-color: white;
        color: {DANGER_COLOR};
        border: 1px solid {BORDER_COLOR};
    }}
    QPushButton#danger:hover {{
        background-color: #fff0f0;
        border-color: {DANGER_COLOR};
    }}

    /* Inputs */
    QLineEdit {{
        background-color: {PANEL_COLOR};
        border: 1px solid {BORDER_COLOR};
        border-bottom: 2px solid {BORDER_COLOR}; /* Windows 11 input style */
        border-radius: 4px;
        padding: 6px 10px;
        selection-background-color: {ACCENT_COLOR};
    }}
    
    QLineEdit:focus {{
        border-bottom-color: {ACCENT_COLOR};
        background-color: white;
    }}

    QListWidget {{
        outline: none;
        padding: 5px;
    }}
    
    QListWidget::item {{
        border-radius: 4px;
        padding: 8px;
        margin-bottom: 4px;
    }}
    
    QListWidget::item:selected {{
        background-color: #e5f1fb; /* Light blue selection */
        color: {TEXT_COLOR};
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
        background-color: {ACCENT_COLOR};
        border-radius: 2px;
    }}
"""
