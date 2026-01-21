import json
import os
import sys

class LanguageManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LanguageManager, cls).__new__(cls)
            cls._instance.languages = {}
            cls._instance.current_lang = 'pt'
            cls._instance.load_languages()
        return cls._instance

    def load_languages(self):
        try:
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.getcwd()
            
            lang_path = os.path.join(base_path, 'src', 'language', 'languages.json')
            
            with open(lang_path, 'r', encoding='utf-8') as f:
                self.languages = json.load(f)
        except Exception as e:
            print(f"Error loading languages: {e}")
            self.languages = {}

    def set_language(self, lang_code):
        if lang_code in self.languages:
            self.current_lang = lang_code

    def t(self, key, **kwargs):
        lang_data = self.languages.get(self.current_lang, {})
        text = lang_data.get(key, key)
        if kwargs:
             try:
                 return text.format(**kwargs)
             except KeyError:
                 return text
        return text

language_manager = LanguageManager()
