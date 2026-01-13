BG_COLOR = "#1e1e1e"
SIDEBAR_COLOR = "#252526"
ACCENT_COLOR = "#007acc"
ACCENT_HOVER = "#0062a3"
TEXT_COLOR = "#cccccc"
TEXT_DIM = "#858585"
BORDER_COLOR = "#454545"
INPUT_BG = "#3c3c3c"
SUCCESS_COLOR = "#198754"
DANGER_COLOR = "#dc3545"
WARNING_COLOR = "#ffc107"

STYLESHEET = f"""
    QWidget {{
        background-color: {BG_COLOR};
        color: {TEXT_COLOR};
        font-family: 'Segoe UI', 'Roboto', sans-serif;
        font-size: 14px;
    }}
    
    QPushButton {{
        background-color: {ACCENT_COLOR};
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 2px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: {ACCENT_HOVER};
    }}
    QPushButton:pressed {{
        background-color: {BG_COLOR};
        border: 1px solid {ACCENT_COLOR};
    }}
    
    QLineEdit {{
        background-color: {INPUT_BG};
        border: 1px solid {BORDER_COLOR};
        color: {TEXT_COLOR};
        padding: 6px;
    }}
    QLineEdit:focus {{
        border: 1px solid {ACCENT_COLOR};
    }}
    
    QListWidget {{
        background-color: {SIDEBAR_COLOR};
        border: none;
        outline: none;
    }}
    QListWidget::item {{
        padding: 8px;
        color: {TEXT_COLOR};
    }}
    QListWidget::item:selected {{
        background-color: {ACCENT_COLOR};
        color: white;
    }}
    QListWidget::item:hover {{
        background-color: #2a2d2e;
    }}
    
    QLabel#h1 {{
        font-size: 24px;
        font-weight: bold;
        color: {TEXT_COLOR};
    }}
    QLabel#h2 {{
        font-size: 18px;
        font-weight: bold;
        color: {TEXT_COLOR};
    }}
    
    .danger-btn {{ background-color: {DANGER_COLOR}; }}
    .danger-btn:hover {{ background-color: #bb2d3b; }}
    
    .success-btn {{ background-color: {SUCCESS_COLOR}; }}
    .success-btn:hover {{ background-color: #157347; }}
    
    .sidebar {{ background-color: {SIDEBAR_COLOR}; }}
"""
