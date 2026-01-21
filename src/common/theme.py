from nicegui import ui, app
from src.common.styles import Colors, DarkColors, Fonts, Shapes

def load_theme():
    ui.add_head_html(f'''
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
        
        /* --- FLUID INPUTS --- */
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
        
        .q-field__native {{
            color: var(--text-primary) !important;
            font-size: 16px;
            font-weight: 500;
        }}
        
        .q-field__label {{
            color: var(--text-secondary);
            font-weight: 400;
            top: 18px;
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

    with ui.button(icon=icon_name, on_click=toggle_mode).classes('fixed bottom-8 right-8 z-50 rounded-full anim-enter delay-300').props('round flat type=a') as btn:
        btn.style('width: 64px; height: 64px; background: rgba(125,125,125,0.1); backdrop-filter: blur(20px); color: var(--text-primary); box-shadow: 0 8px 32px rgba(0,0,0,0.1); transition: transform 0.3s ease;')
        tooltip = ui.tooltip(tooltip_text)

def render_close_button():
    with ui.button(icon='close', on_click=app.shutdown).classes('fixed top-6 right-6 z-50 rounded-full anim-enter delay-300').props('round flat'):
         btn_style = 'color: var(--text-primary); background: rgba(0,0,0,0.05);'
         ui.tooltip('Sair do Sistema')




