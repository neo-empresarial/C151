from nicegui import ui

def load_theme():
    ui.add_head_html('''
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600&display=swap');
        
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f3f3f3; /* Mica */
            margin: 0;
        }
        
        .w11-card {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            border: 1px solid #e5e5e5;
        }
        .w11-btn {
            border-radius: 4px;
            font-weight: 600;
            text-transform: none; /* No caps */
        }
        
        /* Input Styling */
        .q-field__control {
            border-radius: 4px !important;
        }
    </style>
    ''', shared=True)
