import tkinter as tk
from tkinter import ttk
import threading

class LoadingScreen:
    def __init__(self):
        self.root = None
        self.label = None
        self.progress = None
        self.running = False
        
    def show(self, title="DeepFace Access Control"):
        def _show():
            self.root = tk.Tk()
            self.root.title(title)
            self.root.geometry("400x200")
            self.root.resizable(False, False)
            
            self.root.update_idletasks()
            x = (self.root.winfo_screenwidth() // 2) - (400 // 2)
            y = (self.root.winfo_screenheight() // 2) - (200 // 2)
            self.root.geometry(f'+{x}+{y}')
            
            self.root.overrideredirect(True)
            
            frame = tk.Frame(self.root, bg='white', relief='solid', borderwidth=2)
            frame.pack(fill='both', expand=True, padx=2, pady=2)
            
            title_label = tk.Label(
                frame, 
                text="🛡️ DeepFace Access Control",
                font=('Arial', 16, 'bold'),
                bg='white',
                fg='#1f2937'
            )
            title_label.pack(pady=(30, 10))
            
            self.label = tk.Label(
                frame,
                text="Inicializando...",
                font=('Arial', 11),
                bg='white',
                fg='#6b7280'
            )
            self.label.pack(pady=10)
            
            self.progress = ttk.Progressbar(
                frame,
                mode='indeterminate',
                length=300
            )
            self.progress.pack(pady=10)
            self.progress.start(10)
            
            version_label = tk.Label(
                frame,
                text="Carregando modelos...",
                font=('Arial', 9),
                bg='white',
                fg='#9ca3af'
            )
            version_label.pack(pady=(10, 30))
            
            self.running = True
            self.root.mainloop()
        
        thread = threading.Thread(target=_show, daemon=True)
        thread.start()
        
        import time
        while self.root is None:
            time.sleep(0.01)
    
    def update_status(self, message):
        if self.root and self.label:
            try:
                self.label.config(text=message)
                self.root.update()
            except:
                pass
    
    def close(self):
        if self.root and self.running:
            try:
                self.root.quit()
                self.root.destroy()
                self.running = False
            except:
                pass

_loading_screen = None

def show_loading():
    global _loading_screen
    _loading_screen = LoadingScreen()
    _loading_screen.show()
    return _loading_screen

def update_loading(message):
    global _loading_screen
    if _loading_screen:
        _loading_screen.update_status(message)

def close_loading():
    global _loading_screen
    if _loading_screen:
        _loading_screen.close()
        _loading_screen = None
