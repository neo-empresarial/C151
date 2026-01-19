from nicegui import ui, app
from src.common.styles import Colors, DarkColors, Fonts, Shapes

def load_theme():
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
            --radius-sm: {Shapes.RADIUS_SM}; /* 4px */
            --radius-md: {Shapes.RADIUS_MD}; /* 8px */
            --radius-lg: {Shapes.RADIUS_LG}; /* 12px */
            --radius-full: {Shapes.RADIUS_FULL};
        }}
    
        body {{
            font-family: var(--font-main);
            background-color: var(--bg-mica);
            color: var(--text-primary);
            margin: 0;
            overflow: hidden; /* Prevent body scroll if using full layout */
            transition: background-color 0.3s ease, color 0.3s ease;
        }}
        
        /* Dark Mode Overrides */
        body.body--dark {{
            --bg-mica: {DarkColors.MICA_BG};
            --bg-mica-alt: {DarkColors.MICA_ALT};
            --surface: {DarkColors.SURFACE};
            --text-primary: {DarkColors.TEXT_PRIMARY};
            --text-secondary: {DarkColors.TEXT_SECONDARY};
            --border: {DarkColors.BORDER};
            --acrylic-bg: {DarkColors.ACRYLIC_BG};
        }}
        
        /* --- UTILITY CLASSES --- */
        
        /* Windows 11 Card */
        /* rounded corners: 8px for main windows (though we use 12px for standalone cards which looks nice) */
        .w11-card {{
            background-color: var(--surface);
            color: var(--text-primary);
            border-radius: var(--radius-md); /* Standard 8px for containers */
            box-shadow: 0 4px 12px rgba(0,0,0,0.08); /* Soft shadow */
            border: 1px solid var(--border);
            transition: transform 0.1s ease, box-shadow 0.1s ease, background-color 0.3s ease;
        }}
        
        .w11-card:hover {{
            box-shadow: 0 8px 16px rgba(0,0,0,0.12); /* Lift effect */
        }}
        
        /* Glassmorphism / Acrylic Effect */
        .glass {{
            background: var(--acrylic-bg); 
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--border);
        }}

        /* Typography */
        h1, h2, h3, .text-h1, .text-h2, .text-h3 {{ 
            margin: 0; 
            font-weight: 600; 
            font-family: "Segoe UI Variable Display", "Segoe UI", sans-serif;
        }}
        
        /* --- BUTTONS (Fluent Design) --- */
        /* Geometry: 4px radius */
        /* State Changes: Rest, Hover, Pressed */
        
        .w11-btn {{
            border-radius: var(--radius-sm) !important; /* 4px */
            transition: all 0.1s ease-in-out;
            font-weight: 500;
            text-transform: none !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }}
        
        /* Primary Button */
        .w11-btn.bg-primary {{
            background-color: var(--primary) !important;
            color: white !important;
            border: 1px solid var(--primary);
        }}
        
        .w11-btn.bg-primary:hover {{
            background-color: var(--primary-hover) !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .w11-btn.bg-primary:active {{
            background-color: var(--primary-pressed) !important;
            transform: scale(0.98); /* Slight shrink */
        }}
        
        /* Standard/Secondary Button */
        .w11-btn.bg-white, .w11-btn:not(.bg-primary):not(.bg-red-600):not(.bg-green-600) {{
            background-color: var(--surface) !important;
            border: 1px solid var(--border) !important;
            color: var(--text-primary) !important;
            border-bottom: 1px solid var(--border) !important; /* Slight depth */
        }}
        
        .w11-btn.bg-white:hover, .w11-btn:not(.bg-primary):not(.bg-red-600):not(.bg-green-600):hover {{
            background-color: var(--bg-mica-alt) !important;
        }}
        
        .w11-btn.bg-white:active, .w11-btn:not(.bg-primary):not(.bg-red-600):not(.bg-green-600):active {{
            background-color: var(--border) !important;
            transform: scale(0.98);
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
        
        /* Input Field Styling (NiceGUI/Quasar Overrides) */
        
        /* Radius 4px */
        .q-field__control {{
            border-radius: var(--radius-sm) !important; 
            border: 1px solid var(--border);
            padding: 0 12px;
            background-color: var(--surface);
            color: var(--text-primary);
        }}
        
        .q-field__native {{
            color: var(--text-primary) !important;
        }}
        
        .q-field__control:before {{
             border-bottom: 1px solid var(--text-secondary); /* Rest state */
        }}
        
        .q-field__control:hover:before {{
             border-bottom: 1px solid var(--text-primary); /* Hover state */
        }}
        
        .q-field__control:after {{
            border-bottom: 2px solid var(--primary); /* Focus state */
        }}
        
        /* Dialogs */
        .q-dialog__inner > div {{
            border-radius: var(--radius-md) !important; /* 8px */
            box-shadow: 0 8px 32px rgba(0,0,0,0.15) !important; /* Diffused shadow */
            background-color: var(--surface) !important;
            border: 1px solid var(--border);
            color: var(--text-primary);
        }}
        
        /* Input Field Label Styling */
        .q-field__label {{
            color: var(--text-secondary) !important;
        }}
        .q-field__control:hover .q-field__label,
        .q-field__control.q-field--focused .q-field__label {{
            color: var(--text-primary) !important;
        }}

        /* Checkbox/Radio Labels */
        .q-checkbox__label, .q-radio__label {{
            color: var(--text-primary) !important;
        }}

        /* Dropdown/Menu (Select) */
        .q-menu {{
            background-color: var(--surface) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border);
        }}
        
        .q-item {{
            color: var(--text-primary);
        }}
        
        .q-item--active, .q-item:hover, .q-manual-focusable--focused {{
            background-color: var(--bg-mica-alt) !important;
        }}

        /* Text Color Global Override for Quasar components */
        .text-gray-800, .text-gray-600, .text-gray-500, .text-gray-400 {{
            color: var(--text-primary) !important;
        }}
        
    </style>
    ''', shared=True)

def render_theme_toggle_button():
    """
    Renders a fixed floating action button to toggle dark mode.
    Place this in the layout of every page.
    """
    # Initialize from storage or default to False
    is_dark = app.storage.user.get('dark_mode', False)
    
    # Apply initial state
    if is_dark:
        ui.run_javascript("document.body.classList.add('body--dark')")
    else:
        ui.run_javascript("document.body.classList.remove('body--dark')")

    def toggle_mode():
        # Get current state
        new_state = not app.storage.user.get('dark_mode', False)
        # Update storage
        app.storage.user['dark_mode'] = new_state
        
        # Apply changes
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
        btn.style('width: 48px; height: 48px; background-color: var(--surface); color: var(--text-primary); border: 1px solid var(--border);')
        tooltip = ui.tooltip(tooltip_text)
