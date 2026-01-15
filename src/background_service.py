import threading
import time
import sys
import os
from nicegui import ui, app
from fastapi import Request
import PIL.Image
from collections import deque
from collections import Counter

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from src.services.services import camera_manager, db_manager, engine

access_state = {
    "denied": False,
    "user": None,
    "lock": threading.Lock(),
    "history": deque(maxlen=5)
}

def create_tray_icon(shutdown_event):
    import pystray
    
    def on_exit(icon, item):
        icon.stop()
        shutdown_event.set()
        app.shutdown()

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

def face_processing_loop():
    print("Iniciando loop de processamento facial em background...", flush=True)
    engine.start()
    camera_manager.start()
    
    while True:
        try:
            ret, frame = camera_manager.read()
            if ret:
                engine.update_frame(frame)
            else:
                print("DEBUG: Camera read returned False!", flush=True)
            
            results = engine.get_results()
            if results:
                print(f"DEBUG RESULTS: {results}", flush=True)
            
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
                    if not access_state["denied"]:
                         print("ALERTA: Acesso Negado Detectado!", flush=True)
                         access_state["denied"] = True
                         access_state["user"] = results[0]["name"]
                         
                         try:
                             import webbrowser
                             webbrowser.open('http://localhost:8080')
                         except:
                             pass
                elif found_admin:
                    if access_state["denied"]:
                        print("Admin detectado. Acesso liberado.", flush=True)
                        access_state["denied"] = False
                        access_state["user"] = None
                else:
                    if access_state["denied"]:
                         pass

        except Exception as e:
            print(f"Erro no loop de processamento: {e}", flush=True)
        
        time.sleep(0.5)

@app.get('/verificar_operador')
def api_verificar():
    results = engine.get_results()
    
    # --- TEMPORAL CONSISTENCY ---
    with access_state["lock"]:
        if results:
            best = results[0]
            current_user_name = best["name"]
        else:
            current_user_name = None
        
        access_state["history"].append(current_user_name)
        
        # Voting Logic: User must appear in majority of recent frames
        counts = Counter(access_state["history"])
        most_common, count = counts.most_common(1)[0] if counts else (None, 0)
        
        confirmed_user = None
        # Require 3 out of 5 frames to confirm identity
        if most_common is not None and count >= 3:
            confirmed_user = most_common

    print(f"DEBUG: API Verification. History: {list(access_state['history'])} -> Confirmed: {confirmed_user}", flush=True)

    if confirmed_user and confirmed_user != "Desconhecido":
        # Find user details from engine knowledge base
        user_info = next((u for u in engine.known_embeddings if u["name"] == confirmed_user), None)
        
        # Or fall back to current result if it matches
        if not user_info and results and results[0]["name"] == confirmed_user:
             user_info = results[0]
             
        if user_info:
             return {
                "status": "sucesso",
                "usuario": user_info["name"],
                "id": user_info["id"],
                "funcao": user_info.get("access_level", "Visitante"),
                "confianca": 0.99 
            }
            
    return {
        "status": "nenhum_usuario",
        "usuario": None
    }

@ui.page('/')
def main_page():
    
    with ui.column().classes('w-full h-screen justify-center items-center bg-red-600 p-0 m-0 text-white') as container:
        container.style('display: none;') # Hidden initially via CSS or JS class toggle
        container.props('id="access-denied-container"')
        
        ui.icon('gpp_bad', size='150px').classes('animate-bounce')
        ui.label('ACESSO NEGADO').classes('text-9xl font-black blink')
        ui.label('Apenas Administradores Permitidos').classes('text-4xl mt-4')
        
    ui.add_head_html('''
        <style>
            .blink { animation: blinker 1s linear infinite; }
            @keyframes blinker { 50% { opacity: 0; } }
        </style>
        <script>
            window.show_access_denied = function() {
                document.getElementById('c2').style.display = 'flex'; 
            }
            window.hide_access_denied = function() {
                 document.getElementById('c2').style.display = 'none';
            }
        </script>
    ''')

    is_denied = ui.element('div').classes('w-full h-screen absolute top-0 left-0 bg-red-600 flex flex-col justify-center items-center z-50')
    is_denied.bind_visibility_from(access_state, 'denied')
    
    with is_denied:
         ui.icon('warning', size='12rem').classes('text-white mb-8 animate-pulse')
         ui.label('ACESSO NEGADO').classes('text-8xl font-black text-white text-center')
         ui.label('ÁREA RESTRITA A ADMINISTRADORES').classes('text-3xl text-white mt-4 font-bold')

    ui.timer(0.5, lambda: is_denied.update())

def main():
    shutdown_event = threading.Event()
    tray_icon = create_tray_icon(shutdown_event)
    
    tray_thread = threading.Thread(target=tray_icon.run, daemon=True)
    tray_thread.start()
    
    proc_thread = threading.Thread(target=face_processing_loop, daemon=True)
    proc_thread.start()
    
    import webbrowser
    
    def browser_control_loop():
        while True:
            if access_state["denied"]:
                pass 
            time.sleep(1)
    
    print("Iniciando Serviço de Biometria (Modo Server)...", flush=True)
    
    ui.run(
        title="Serviço de Biometria",
        port=8080,
        show=False, 
        reload=False,
        native=False
    )


if __name__ in {"__main__", "__mp_main__"}:
    main()
