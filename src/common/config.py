
import os

# Database Configuration
# Use absolute path to ensure reliability across different execution contexts
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "users.db")

# Camera Configuration
CAMERA_INDEX = 0

# UI Configuration (Windows 11 inspired colors)
THEME_COLORS = {
    'background': '#f3f3f3', # Mica-like light gray
    'surface': '#ffffff',
    'primary': '#0067c0',    # Windows Blue
    'text_primary': '#202020',
    'text_secondary': '#5d5d5d',
    'border': '#e5e5e5',
    'success': '#107c10',
    'error': '#c42b1c'
}
