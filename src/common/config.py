
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "users.db")

CAMERA_INDEX = 0

THEME_COLORS = {
    'background': '#f3f3f3', 
    'surface': '#ffffff',
    'primary': '#0067c0',    
    'text_primary': '#202020',
    'text_secondary': '#5d5d5d',
    'border': '#e5e5e5',
    'success': '#107c10',
    'error': '#c42b1c'
}
