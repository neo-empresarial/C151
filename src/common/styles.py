
class Colors:
    MICA_BG = "#FFFFFF" 
    MICA_ALT = "#F8F9FA" 
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
    
    BORDER = "rgba(0, 0, 0, 0.08)"
    BORDER_FOCUS = "#1A73E8"
    
    GLASS_WHITE = "rgba(255, 255, 255, 0.8)"
    GLASS_BLACK = "rgba(0, 0, 0, 0.6)"
    
    ACRYLIC_BG = "rgba(255, 255, 255, 0.65)"

class DarkColors:
    MICA_BG = "#101010" 
    MICA_ALT = "#1C1C1C"
    SURFACE = "rgba(30, 30, 30, 0.60)" 
    
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#E8EAED"
    TEXT_DISABLED = "#9AA0A6"
    
    BORDER = "rgba(255, 255, 255, 0.08)"
    
    ACRYLIC_BG = "rgba(20, 20, 20, 0.7)"
    
    GLASS_WHITE = "rgba(255, 255, 255, 0.08)"
    GLASS_BLACK = "rgba(0, 0, 0, 0.8)"

class Fonts:
    MAIN = '"Google Sans", "Inter", "Segoe UI Variable Display", "Segoe UI", sans-serif'
    MONO = '"Roboto Mono", "Consolas", monospace'
    
    SIZE_SM = "12px"
    SIZE_MD = "14px"
    SIZE_LG = "18px"
    SIZE_XL = "24px"
    SIZE_XXL = "48px" 
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

ANTIGRAVITY_THEME = f'''
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
        
        :root {{
            /* Colors */
            --bg-mica: {Colors.MICA_BG};
            --surface: rgba(255, 255, 255, 0.65); /* High transparency glass */
            
            --primary: {Colors.PRIMARY};
            --primary-hover: {Colors.PRIMARY_HOVER};
            
            --text-primary: {Colors.TEXT_PRIMARY};
            --text-secondary: {Colors.TEXT_SECONDARY};
            
            /* Border is now very subtle/invisible */
            --border: rgba(255, 255, 255, 0.4);
            --border-light: rgba(255, 255, 255, 0.6);
            
            /* Typography */
            --font-main: 'Outfit', 'Inter', sans-serif;
            
            /* Shapes */
            --radius-lg: 32px; 
            --radius-full: 9999px;
            
            /* Effects */
            --shadow-card: 0 10px 40px -10px rgba(0,0,0,0.05);
            --shadow-float: 0 20px 60px -10px rgba(0,0,0,0.1);
            --glass-blur: blur(30px);
            
            /* Physics */
            --ease-elastic: cubic-bezier(0.34, 1.56, 0.64, 1);
            --ease-smooth: cubic-bezier(0.2, 0.8, 0.2, 1);
        }}
    
        body {{
            font-family: var(--font-main);
            background-color: #F0F2F5;
            color: var(--text-primary);
            margin: 0;
            overflow: hidden;
            transition: background 0.5s ease;
            
            /* Light Mode Gradient Mesh - Moving Aurora (ENHANCED VISIBILITY) */
            background-image: 
                radial-gradient(at 0% 0%, rgba(255, 255, 255, 0.5) 0, transparent 50%), 
                radial-gradient(at 50% 100%, rgba(99, 102, 241, 0.4) 0, transparent 50%), 
                radial-gradient(at 100% 0%, rgba(236, 72, 153, 0.4) 0, transparent 50%),
                radial-gradient(at 0% 100%, rgba(34, 197, 94, 0.3) 0, transparent 50%);
            background-size: 150% 150%;
            animation: gradient-move 20s ease infinite;
        }}
        
        /* Dark Mode - Deep Space Aurora */
        body.body--dark {{
            --bg-mica: #050505;
            --text-primary: #ffffff;
            --text-secondary: rgba(255,255,255,0.7);
            
            --surface: rgba(20, 20, 20, 0.6);
            --border: rgba(255, 255, 255, 0.08);
            --border-light: rgba(255, 255, 255, 0.15);
            --primary: #5c8afa; /* Brighter blue for dark mode */
            
            --shadow-card: 0 20px 80px -10px rgba(0,0,0,0.6);
            --shadow-float: 0 30px 100px -10px rgba(0,0,0,0.8);
            
            background-color: #050505;
            
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(76, 29, 149, 0.25), transparent 40%),
                radial-gradient(circle at 85% 30%, rgba(59, 130, 246, 0.2), transparent 40%),
                radial-gradient(circle at 50% 90%, rgba(16, 185, 129, 0.15), transparent 45%);
        }}

        @keyframes gradient-move {{
            0% {{ background-position: 0% 50% }}
            50% {{ background-position: 100% 50% }}
            100% {{ background-position: 0% 50% }}
        }}
        
        /* --- GLASS CARD --- */
        .w11-card {{
            background: var(--surface);
            backdrop-filter: var(--glass-blur);
            -webkit-backdrop-filter: var(--glass-blur);
            border: 1px solid var(--border);
            border-top: 1px solid var(--border-light); 
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-card);
            color: var(--text-primary);
            position: relative;
            overflow: hidden;
            transition: transform 0.4s var(--ease-elastic), box-shadow 0.4s var(--ease-smooth);
        }}
        
        .w11-card:hover {{
            transform: translateY(-4px) scale(1.005);
            box-shadow: var(--shadow-float);
        }}
        
        /* --- TYPOGRAPHY --- */
        h1, h2, h3, .text-h1, .text-h2, .text-h3 {{
            font-weight: 500;
            letter-spacing: -0.03em;
        }}
        
        /* --- FLUID INPUTS (AND SELECTS) --- */
        /* Updated selector to include q-field--filled etc if needed, but control is main one */
        .q-field__control {{
            border-radius: var(--radius-full) !important;
            border: 1px solid var(--border);
            background: rgba(255,255,255,0.1); 
            height: 56px;
            padding: 0 24px;
            transition: all 0.3s var(--ease-smooth);
        }}
        
        .q-field__control:hover {{
            background: rgba(255,255,255,0.2);
        }}
        
        .q-field--focused .q-field__control {{
            background: rgba(255,255,255,0.25);
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 4px rgba(66, 133, 244, 0.2);
        }}
        
        .q-field__native, .q-field__prefix, .q-field__suffix, .q-field__input {{
            color: var(--text-primary) !important;
            font-size: 16px;
            font-weight: 500;
        }}
        
        .q-field__label {{
            color: var(--text-secondary);
            font-weight: 400;
            top: 18px;
        }}
        
        /* Fix for Select Dropdown Arrow Color */
        .q-field__append i {{
            color: var(--text-secondary) !important;
        }}

        .q-field__control:before, .q-field__control:after {{
            content: none !important;
        }}
        
        /* --- BORDERLESS LIQUID BUTTONS --- */
        .w11-btn {{
            border-radius: var(--radius-full) !important;
            font-weight: 600;
            letter-spacing: 0.02em;
            text-transform: none !important;
            padding: 12px 32px;
            transition: all 0.4s var(--ease-elastic);
            position: relative;
            overflow: hidden;
            border: none !important; /* NO BORDERS */
        }}
        
        .w11-btn:active {{
            transform: scale(0.92);
        }}
        
        /* Primary - GLASS GRADIENT Style */
        .w11-btn.bg-primary {{
            background: linear-gradient(135deg, rgba(79, 70, 229, 0.8), rgba(67, 56, 202, 0.6)) !important; /* Glassy Gradient */
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            color: white !important;
            box-shadow: 0 8px 32px rgba(79, 70, 229, 0.3);
        }}
        
        .w11-btn.bg-primary:hover {{
            box-shadow: 0 12px 40px rgba(79, 70, 229, 0.5);
            transform: translateY(-2px);
            filter: brightness(1.2);
            border-color: rgba(255, 255, 255, 0.4) !important;
        }}
        
        /* Secondary / White - Ghost Style */
        /* Use background with low opacity instead of border */
        .w11-btn.bg-white, .w11-btn:not(.bg-primary):not(.bg-red-600):not(.bg-green-600) {{
            background: rgba(255, 255, 255, 0.4) !important; 
            color: var(--text-primary) !important;
            box-shadow: none;
        }}
        
        body.body--dark .w11-btn.bg-white {{
           background: rgba(255, 255, 255, 0.1) !important; 
        }}
        
        .w11-btn.bg-white:hover, .w11-btn:not(.bg-primary):not(.bg-red-600):not(.bg-green-600):hover {{
            background: rgba(255, 255, 255, 0.6) !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }}
        
        body.body--dark .w11-btn.bg-white:hover {{
            background: rgba(255, 255, 255, 0.2) !important;
        }}
        
        /* --- ANIMATION UTILS --- */
        @keyframes float-up {{
            0% {{ opacity: 0; transform: translateY(40px) scale(0.95); }}
            100% {{ opacity: 1; transform: translateY(0) scale(1); }}
        }}
        
        .anim-enter {{
            animation: float-up 0.8s var(--ease-elastic) forwards;
            opacity: 0; 
        }}
        
        .delay-100 {{ animation-delay: 0.1s; }}
        .delay-200 {{ animation-delay: 0.2s; }}
        .delay-300 {{ animation-delay: 0.3s; }}
        
        /* --- QUASAR OVERRIDES --- */
        .q-dialog__inner > div {{
            border-radius: var(--radius-lg);
            background: var(--surface) !important;
            backdrop-filter: blur(40px) !important;
            box-shadow: 0 40px 100px -20px rgba(0,0,0,0.5);
            border: 1px solid var(--border-light);
            overflow: visible; /* Allow glows to bleed */
        }}
        
        /* Hide Scrollbars */
        ::-webkit-scrollbar {{
            width: 0px; 
            background: transparent;
        }}
        
        /* Force Text Colors */
        .text-gray-800, .text-gray-600, .text-gray-500, .text-gray-400 {{
            color: var(--text-primary) !important;
        }}
        
    </style>
'''
