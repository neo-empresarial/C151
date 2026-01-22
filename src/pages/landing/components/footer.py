from nicegui import ui
from src.language.manager import language_manager as lm

def render():
    ui.label(lm.t('demo_footer')).classes('absolute bottom-4 text-gray-500 text-white')
