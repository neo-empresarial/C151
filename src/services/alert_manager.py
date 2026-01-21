from nicegui import app
import asyncio
import webview

class AlertManager:
    def __init__(self):
        self.local_state_fullscreen = False

    async def ensure_hidden_startup(self):
        try:
            print("DEBUG: AlertManager - Ensuring hidden startup...", flush=True)
            await asyncio.sleep(0.5)
            if app.native.main_window:
                app.native.main_window.hide()
                print("DEBUG: AlertManager - Window hidden on startup.", flush=True)
            else:
                print("DEBUG: AlertManager - No main window found on startup.", flush=True)
        except Exception as e:
            print(f"DEBUG: AlertManager - Error in hidden startup: {e}", flush=True)

    async def manage_window(self, is_denied):
        try:
            if not app.native.main_window:
                return

            window = app.native.main_window

            if is_denied:
                if not self.local_state_fullscreen:
                    print("DEBUG: AlertManager - ACCESS DENIED detected. Initiating window show sequence.", flush=True)
                    
                    try:
                        window.restore()
                    except:
                        pass
                        
                    try:
                        window.show()
                    except:
                        pass
                    window.on_top = True
                    
                    try:
                        screens = webview.screens
                        if screens:
                            screen = screens[0]
                            window.resize(screen.width, screen.height)
                            window.move(0, 0)
                    except:
                        pass
                    
                    try:
                        window.maximize()
                    except:
                        pass
                        
                    await asyncio.sleep(0.2)
                    
                    window.fullscreen = True
                    self.local_state_fullscreen = True
                    print("DEBUG: AlertManager - Window sequence complete. Fullscreen enforced.", flush=True)
            else:
                if self.local_state_fullscreen:
                    print("DEBUG: AlertManager - ACCESS GRANTED/RESET. Hiding window.", flush=True)
                    
                    window.on_top = False
                    window.fullscreen = False
                    await asyncio.sleep(0.1)
                    
                    print("DEBUG: AlertManager - Calling hide().", flush=True)
                    window.hide()
                    self.local_state_fullscreen = False
                    print("DEBUG: AlertManager - Window hidden.", flush=True)

        except Exception as e:
            print(f"DEBUG: AlertManager - Error in manage_window: {e}", flush=True)
