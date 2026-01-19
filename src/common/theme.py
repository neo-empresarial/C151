from nicegui import ui
from src.common.styles import Colors, Fonts, Shapes

def load_theme():
    """
    Injects Windows 11 style variables and classes into the application using specific tokens.
    """
    ui.add_head_html(f'''
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600&display=swap');
        
        :root {{
            /* Colors */
            --bg-mica: {Colors.MICA_BG};
            --bg-mica-alt: {Colors.MICA_ALT};
            --surface: {Colors.SURFACE};
            --primary: {Colors.PRIMARY};
            --primary-hover: {Colors.PRIMARY_HOVER};
            --text-primary: {Colors.TEXT_PRIMARY};
            --text-secondary: {Colors.TEXT_SECONDARY};
            --border: {Colors.BORDER};
            
            /* Status */
            --success: {Colors.SUCCESS};
            --warning: {Colors.WARNING};
            --error: {Colors.ERROR};
            
            /* Typography */
            --font-main: {Fonts.MAIN};
            
            /* Shapes */
            --radius-md: {Shapes.RADIUS_MD};
            --radius-lg: {Shapes.RADIUS_LG};
            --radius-full: {Shapes.RADIUS_FULL};
        }}
    
        body {{
            font-family: var(--font-main);
            background-color: var(--bg-mica);
            color: var(--text-primary);
            margin: 0;
            overflow: hidden; /* Prevent body scroll if using full layout */
        }}
        
        /* --- UTILITY CLASSES --- */
        
        /* Windows 11 Card */
        .w11-card {{
            background-color: var(--surface);
            border-radius: var(--radius-lg);
            box-shadow: 0 4px 12px rgba(0,0,0,0.08); /* Softer shadow */
            border: 1px solid var(--border);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        
        .w11-card:hover {{
            box-shadow: 0 6px 16px rgba(0,0,0,0.12);
        }}
        
        /* Glassmorphism / Acrylic Effect */
        .glass {{
            background: rgba(255, 255, 255, 0.75);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255,255,255,0.5);
        }}

        /* Typography */
        h1, h2, h3 {{ margin: 0; font-weight: 600; }}
        
        /* Primary Button Override */
        .q-btn.bg-primary {{
            background-color: var(--primary) !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
        }}
        
        /* --- ANIMATIONS --- */
        
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        
        @keyframes slideUp {{
            from {{ transform: translateY(20px); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}
        
        .anim-fade-in {{ animation: fadeIn 0.4s ease-out forwards; }}
        .anim-slide-up {{ animation: slideUp 0.5s cubic-bezier(0.2, 0.8, 0.2, 1) forwards; }}
        
        /* Input Field Styling Fixes for NiceGUI/Quasar */
        .q-field__control {{
            border-radius: var(--radius-md) !important;
        }}
        
        .q-dialog__inner > div {{
            border-radius: var(--radius-lg) !important;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2) !important;
        }}
        
    </style>
    ''', shared=True)
