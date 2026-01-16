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
                # print("DEBUG: AlertManager - No window available yet.")
                return

            window = app.native.main_window

            if is_denied:
                if not self.local_state_fullscreen:
                    print("DEBUG: AlertManager - ACCESS DENIED detected. Initiating window show sequence.", flush=True)
                    try:
                        print("DEBUG: AlertManager - Restoring window...", flush=True)
                        window.restore() 
                    except Exception as e:
                        print(f"DEBUG: AlertManager - Restore failed (might not be needed): {e}", flush=True)
                    
                    try:
                        # Aggressive Fullscreen Strategy: Resize to Screen Dimensions
                        screens = webview.screens
                        if screens:
                            screen = screens[0]
                            print(f"DEBUG: AlertManager - Resizing to Screen: {screen.width}x{screen.height}", flush=True)
                            window.resize(screen.width, screen.height)
                            window.move(0, 0)
                    except Exception as e:
                        print(f"DEBUG: AlertManager - Manual resize failed: {e}", flush=True)

                    print("DEBUG: AlertManager - Setting ON TOP.", flush=True)
                    window.on_top = True
                    
                    print("DEBUG: AlertManager - Showing window.", flush=True)
                    window.show()
                    
                    print("DEBUG: AlertManager - Maximizing window.", flush=True)
                    try:
                         window.maximize()
                    except:
                         pass

                    await asyncio.sleep(0.5)
                    
                    print("DEBUG: AlertManager - Setting FULLSCREEN.", flush=True)
                    window.fullscreen = True
                    
                    self.local_state_fullscreen = True
                    print("DEBUG: AlertManager - Window sequence complete. Should be visible and fullscreen.", flush=True)
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
