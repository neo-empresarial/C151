import threading
import time
import sys
import os
import signal
from nicegui import ui, app
from fastapi import Request
import PIL.Image

# Add src to path if needed (though running from root usually works)
# Add Root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from src.services.services import camera_manager, db_manager, engine

# Global state for the access denied loop
access_state = {
    "denied": False,
    "user": None,
    "lock": threading.Lock()
}

# --- System Tray Logic ---
def create_tray_icon(shutdown_event):
    import pystray
    
    def on_exit(icon, item):
        icon.stop()
        shutdown_event.set()
        app.shutdown()

    # Create a simple icon (you might want to load a real .png/.ico)
    # For now, a simple colored square
    image = PIL.Image.new('RGB', (64, 64), color=(0, 103, 192))
    
    icon = pystray.Icon(
        "FaceAuthService",
        image,
        "Serviço de Biometria",
        menu=pystray.Menu(
            pystray.MenuItem("Sair", on_exit)
        )
    )
    return icon

# --- Background Face Processing ---
def face_processing_loop():
    print("Iniciando loop de processamento facial em background...", flush=True)
    engine.start() # Ensure engine is running
    camera_manager.start()
    
    while True:
        try:
            # 1. Capture Frame (CameraManager handles reading)
            # The engine automatically picks up the latest frame if we are feeding it
            # But here we need to actively manage the engine update or check results
            
            # Wait for result from engine (which runs on its own thread if started)
            # OR force a single representation if we want strict control.
            # The Engine class in src/features/inferencia/engine.py has a _process_loop
            # that runs continually if update_frame is called.
            
            # Let's check engine integration:
            # engine._process_loop calls update_frame? No.
            # We need to feed the engine.
            
            ret, frame = camera_manager.read()
            if ret:
                engine.update_frame(frame)
            
            # Get latest results
            results = engine.get_results()
            
            # Logic for Access Denied
            found_admin = False
            found_someone = False
            
            if results:
                for res in results:
                    found_someone = True
                    if res.get("access_level") == "Admin":
                        found_admin = True
                        break
            
            with access_state["lock"]:
                if found_someone and not found_admin:
                    # User detected but NOT Admin -> TRIGGER ALARM
                    if not access_state["denied"]:
                         print("ALERTA: Acesso Negado Detectado!", flush=True)
                         access_state["denied"] = True
                         access_state["user"] = results[0]["name"]
                         # Trigger UI Show
                         ui.run_javascript('window.show_access_denied();')
                         # Force Open Browser to SPAM screen
                         try:
                             import webbrowser
                             webbrowser.open('http://localhost:8080')
                         except:
                             pass
                elif found_admin:
                    # Admin present -> All good
                    if access_state["denied"]:
                        print("Admin detectado. Acesso liberado.", flush=True)
                        access_state["denied"] = False
                        access_state["user"] = None
                        # Hide UI
                        ui.run_javascript('window.hide_access_denied();')
                else:
                    # No one detected -> calm down? 
                    # Or keep alarm valid until admin clears it?
                    # Let's say: if no one, we keep state as is?
                    # Or auto-reset? Let's auto-reset for now to avoid stuck screens if user leaves.
                    if access_state["denied"]:
                         pass # Keep denying until admin saves or time out?
                         # For now let's keep it simple: Realtime check.
                         # If face leaves, alarm stops? Or stays?
                         # User requested "spam in the screen", implies persistent annoyance.
                         pass

        except Exception as e:
            print(f"Erro no loop de processamento: {e}", flush=True)
        
        time.sleep(0.5) # Check every 500ms

# --- API Endpoints ---
@app.get('/verificar_operador')
def api_verificar():
    results = engine.get_results()
    if results:
        # Return best match
        # If multiple, logic might need adjustment. Returning first for now.
        best = results[0]
        return {
            "status": "sucesso",
            "usuario": best["name"],
            "id": best["id"],
            "funcao": best["access_level"],
            "confianca": best["confidence"]
        }
    else:
        return {
            "status": "nenhum_usuario",
            "usuario": None
        }

# --- NiceGUI Interface (The "Hidden" Window) ---
@ui.page('/')
def main_page():
    # This page is usually hidden.
    # We will build recent Access Denied UI here, but hidden by default.
    
    with ui.column().classes('w-full h-screen justify-center items-center bg-red-600 p-0 m-0 text-white') as container:
        container.style('display: none;') # Hidden initially via CSS or JS class toggle
        container.props('id="access-denied-container"')
        
        ui.icon('gpp_bad', size='150px').classes('animate-bounce')
        ui.label('ACESSO NEGADO').classes('text-9xl font-black blink')
        ui.label('Apenas Administradores Permitidos').classes('text-4xl mt-4')
        
        # We can add a button for Admin to dismiss via PIN if we wanted, 
        # but facial recognition is the key here.

    # Javascript to control visibility from Python
    ui.add_head_html('''
        <style>
            .blink { animation: blinker 1s linear infinite; }
            @keyframes blinker { 50% { opacity: 0; } }
        </style>
        <script>
            window.show_access_denied = function() {
                document.getElementById('c2').style.display = 'flex'; // c2 is usually the ID of the first container if not set? 
                // Better to bind visibility data.
                // But let's assume we can maximize window here too.
            }
            window.hide_access_denied = function() {
                 document.getElementById('c2').style.display = 'none';
            }
        </script>
    ''')

    # Better NiceGUI way: Data binding
    # But thread interaction needs care.

    # Let's use a visibility binding
    is_denied = ui.element('div').classes('w-full h-screen absolute top-0 left-0 bg-red-600 flex flex-col justify-center items-center z-50')
    is_denied.bind_visibility_from(access_state, 'denied')
    
    with is_denied:
         ui.icon('warning', size='12rem').classes('text-white mb-8 animate-pulse')
         ui.label('ACESSO NEGADO').classes('text-8xl font-black text-white text-center')
         ui.label('ÁREA RESTRITA A ADMINISTRADORES').classes('text-3xl text-white mt-4 font-bold')

    # Timer to sync state check for UI updates (NiceGUI needs this to react to thread changes)
    ui.timer(0.5, lambda: is_denied.update())

# --- Startup ---
def main():
    # Setup System Tray
    shutdown_event = threading.Event()
    tray_icon = create_tray_icon(shutdown_event)
    
    # Start Tray in separate thread (Linux AppIndicator usually fine with this)
    # If this crashes due to Main Thread requirement, we might need to swap.
    tray_thread = threading.Thread(target=tray_icon.run, daemon=True)
    tray_thread.start()
    
    # Start Processing Loop
    proc_thread = threading.Thread(target=face_processing_loop, daemon=True)
    proc_thread.start()
    
    # Modify Access Denied Logic to use Browser
    import webbrowser
    
    def browser_control_loop():
        # Simple poller to open browser if denied
        while True:
            if access_state["denied"]:
                # Check if we should open the window
                # We can't easily know if it's already open, but we can try to call "spam"
                # Using run_javascript relies on a connected client.
                # If no client is connected, we MUST open the browser.
                
                # We can check clients connected to NiceGUI?
                # For now, blindly open if not recently opened? 
                # Let's rely on the JS "show_access_denied" if client exists, 
                # but if no client, we open.
                pass 
            time.sleep(1)
            
    # We'll just rely on the user having the page open? 
    # No, user said "spam the screen".
    # So we should force open it.
    
    # Inject logic into the processing loop (via globals or callback) to open browser
    # We will do it in the processing loop above? No, let's keep it clean.
    
    print("Iniciando Serviço de Biometria (Modo Server)...", flush=True)
    
    # Run NiceGUI in Server Mode (Non-Native) to avoid GTK Conflict
    ui.run(
        title="Serviço de Biometria",
        port=8080,
        show=False, 
        reload=False,
        native=False # Disable Native Window to fix GTK conflict
    )


if __name__ in {"__main__", "__mp_main__"}:
    main()
