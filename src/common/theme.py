from nicegui import ui, app
from src.common.styles import Colors, DarkColors, Fonts, Shapes

def load_theme():
    ui.add_head_html(f'''
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
        
        :root {{
            /* Colors */
            --bg-mica: {Colors.MICA_BG};
            --bg-mica-alt: {Colors.MICA_ALT};
            --surface: {Colors.SURFACE};
            --primary: {Colors.PRIMARY};
            --primary-hover: {Colors.PRIMARY_HOVER};
            --primary-pressed: {Colors.PRIMARY_PRESSED}; 
            --text-primary: {Colors.TEXT_PRIMARY};
            --text-secondary: {Colors.TEXT_SECONDARY};
            --border: {Colors.BORDER};
            --acrylic-bg: {Colors.ACRYLIC_BG};
            
            /* Status */
            --success: {Colors.SUCCESS};
            --warning: {Colors.WARNING};
            --error: {Colors.ERROR};
            
            /* Typography */
            --font-main: {Fonts.MAIN};
            
            /* Shapes */
            --radius-sm: {Shapes.RADIUS_SM}; 
            --radius-md: {Shapes.RADIUS_MD}; 
            --radius-lg: {Shapes.RADIUS_LG}; 
            --radius-xl: {Shapes.RADIUS_XL};
            --radius-full: {Shapes.RADIUS_FULL};
            
            /* Effects - Refined Shadows and Glows */
            --shadow-card: 0 8px 32px rgba(0, 0, 0, 0.04);
            --shadow-hover: 0 16px 48px rgba(0, 0, 0, 0.08);
            --glow-color: rgba(66, 133, 244, 0.0);
            
            /* Physics Constants */
            --ease-physics: cubic-bezier(0.2, 0.8, 0.2, 1);
        }}
    
        body {{
            font-family: var(--font-main);
            background-color: var(--bg-mica);
            color: var(--text-primary);
            margin: 0;
            overflow: hidden;
            transition: background-color 0.5s var(--ease-physics), color 0.5s ease;
        }}
        
        /* Dark Mode - Antigravity Aurora Style */
        body.body--dark {{
            --bg-mica: {DarkColors.MICA_BG};
            --bg-mica-alt: {DarkColors.MICA_ALT};
            --surface: {DarkColors.SURFACE};
            --text-primary: {DarkColors.TEXT_PRIMARY};
            --text-secondary: {DarkColors.TEXT_SECONDARY};
            --border: {DarkColors.BORDER};
            --acrylic-bg: {DarkColors.ACRYLIC_BG};
            --glow-color: rgba(66, 133, 244, 0.15); 
            --shadow-card: 0 12px 40px rgba(0, 0, 0, 0.4);
            
            /* Subtle Gradient Background for Depth */
            background-image: radial-gradient(circle at 10% 20%, rgba(66, 133, 244, 0.08) 0%, transparent 40%),
                              radial-gradient(circle at 90% 80%, rgba(147, 52, 230, 0.08) 0%, transparent 40%);
        }}
        
        /* --- UTILITY CLASSES --- */
        
        /* Glassmorphism Card */
        .w11-card {{
            background-color: var(--surface);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            color: var(--text-primary);
            border-radius: var(--radius-lg); 
            box-shadow: var(--shadow-card);
            border: 1px solid var(--border);
            transition: all 0.4s var(--ease-physics);
            position: relative;
            overflow: hidden;
        }}
        
        /* Interactive Card Physics */
        .w11-card:hover {{
            box-shadow: var(--shadow-hover);
            transform: translateY(-4px) scale(1.002);
            border-color: rgba(66, 133, 244, 0.2); /* Subtle blue hint */
        }}
        
        /* Typography */
        h1, h2, h3, .text-h1, .text-h2, .text-h3 {{ 
            margin: 0; 
            font-weight: 400; 
            letter-spacing: -0.8px; 
            font-family: var(--font-main);
        }}
        
        /* --- BUTTONS (Antigravity Physics) --- */
        
        .w11-btn {{
            border-radius: var(--radius-full) !important;
            transition: all 0.3s var(--ease-physics);
            font-weight: 500;
            text-transform: none !important;
            box-shadow: none;
            padding: 12px 28px;
            font-size: 15px;
            letter-spacing: 0.2px;
            position: relative;
            overflow: hidden;
        }}
        
        /* Click Physics - Shrink */
        .w11-btn:active {{
            transform: scale(0.95);
        }}
        
        /* Primary Button */
        .w11-btn.bg-primary {{
            background-color: var(--primary) !important;
            color: white !important;
            border: 1px solid var(--primary);
        }}
        
        .w11-btn.bg-primary:hover {{
            background-color: var(--primary-hover) !important;
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            transform: translateY(-2px);
        }}
        
        .w11-btn.bg-primary:active {{
            background-color: var(--primary-pressed) !important;
            transform: scale(0.95) translateY(0);
        }}
        
        /* Standard/White Button */
        .w11-btn.bg-white, .w11-btn:not(.bg-primary):not(.bg-red-600):not(.bg-green-600) {{
            background-color: var(--surface) !important;
            border: 1px solid var(--border) !important;
            color: var(--text-primary) !important;
        }}
        
        .w11-btn.bg-white:hover {{
            background-color: var(--bg-mica-alt) !important;
            border-color: var(--text-primary) !important;
            transform: translateY(-1px);
        }}

        /* --- INPUTS --- */
        
        .q-field__control {{
            border-radius: var(--radius-full) !important; /* Rounded inputs */
            border: 1px solid var(--border);
            padding: 0 20px;
            background-color: var(--surface); 
            backdrop-filter: blur(10px);
            color: var(--text-primary);
            height: 52px;
            transition: all 0.3s var(--ease-physics);
        }}
        
        .q-field__control:hover {{
             border-color: var(--text-secondary);
             background-color: rgba(255,255,255,0.05);
        }}
        
        .q-field--focused .q-field__control {{
             border: 1px solid var(--primary) !important;
             box-shadow: 0 0 0 4px rgba(66, 133, 244, 0.1); /* Focus Ring */
        }}
        
        .q-field__control:before, .q-field__control:after {{
             border: none !important; 
        }}
        
        .q-field__label {{
            color: var(--text-secondary) !important;
            top: 16px;
        }}
        
        /* --- ANIMATIONS --- */
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: scale(0.96); filter: blur(4px); }}
            to {{ opacity: 1; transform: scale(1); filter: blur(0); }}
        }}
        
        @keyframes slideUp {{
            from {{ transform: translateY(40px); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}
        
        .anim-fade-in {{ animation: fadeIn 0.8s var(--ease-physics) forwards; }}
        .anim-slide-up {{ animation: slideUp 0.8s var(--ease-physics) forwards; }}
        
        /* Staggered Delays for Children */
        .stagger-1 {{ animation-delay: 0.1s; }}
        .stagger-2 {{ animation-delay: 0.2s; }}
        .stagger-3 {{ animation-delay: 0.3s; }}
        
        /* Dialogs - Glassy */
        .q-dialog__inner > div {{
            border-radius: var(--radius-lg) !important;
            background-color: var(--surface) !important;
            backdrop-filter: blur(32px) !important;
            -webkit-backdrop-filter: blur(32px) !important;
            box-shadow: 0 24px 80px rgba(0,0,0,0.3) !important;
            border: 1px solid var(--border);
            color: var(--text-primary);
        }}

        /* Text Color Global Override */
        .text-gray-800, .text-gray-600, .text-gray-500, .text-gray-400 {{
            color: var(--text-primary) !important;
        }}
        
    </style>
    ''', shared=True)


_is_dark_mode = False

def render_theme_toggle_button():
    global _is_dark_mode
    is_dark = _is_dark_mode
    if is_dark:
        ui.run_javascript("document.body.classList.add('body--dark')")
    else:
        ui.run_javascript("document.body.classList.remove('body--dark')")

    def toggle_mode():
        global _is_dark_mode
        _is_dark_mode = not _is_dark_mode
        new_state = _is_dark_mode
        if new_state:
            ui.run_javascript("document.body.classList.add('body--dark')")
            btn.props('icon=light_mode')
            tooltip.text = "Modo Claro"
        else:
            ui.run_javascript("document.body.classList.remove('body--dark')")
            btn.props('icon=dark_mode')
            tooltip.text = "Modo Escuro"

    icon_name = 'light_mode' if is_dark else 'dark_mode'
    tooltip_text = "Modo Claro" if is_dark else "Modo Escuro"

    with ui.button(icon=icon_name, on_click=toggle_mode).classes('fixed bottom-6 right-6 z-50 w11-btn rounded-full shadow-lg').props('round') as btn:
        btn.style('width: 64px; height: 64px; background-color: var(--surface); color: var(--text-primary); border: 1px solid var(--border); transition: transform 0.3s ease;')
        tooltip = ui.tooltip(tooltip_text)

def render_close_button():
    """
    Renders a fixed button at top-right to close the application.
    """
    with ui.button(icon='close', on_click=app.shutdown).classes('fixed top-4 right-4 z-50 w11-btn rounded-full shadow-none').props('round'):
         ui.tooltip('Sair do Sistema')




