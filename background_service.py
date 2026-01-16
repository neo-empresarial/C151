import threading
import time
import asyncio
from nicegui import ui, app
from src.services.services import camera_manager, engine, db_manager
from src.services.access_control import AccessController
from src.services.alert_manager import AlertManager
from src.services.ui_layout import UILayout

access_controller = AccessController()
alert_manager = AlertManager()
layout = UILayout(access_controller, db_manager)

def face_processing_loop():
    print("DEBUG: Loop de processamento iniciado.", flush=True)
    try:
        engine.start()
        print("DEBUG: Engine iniciada.", flush=True)
        camera_manager.start()
        if camera_manager.cap is None or not camera_manager.cap.isOpened():
             print("DEBUG: AVISO - Falha ao abrir a câmera no reset inicial.", flush=True)
        else:
             print("DEBUG: Câmera iniciada com sucesso.", flush=True)

    except Exception as e:
        print(f"DEBUG: Erro na inicialização: {e}", flush=True)
        pass
    
    first_pass = True
    while True:
        try:
            ret, frame = camera_manager.read()
            if first_pass:
                 if ret:
                      print("DEBUG: PRIMEIRO FRAME LIDO COM SUCESSO!", flush=True)
                 else:
                      print("DEBUG: FALHA AO LER PRIMEIRO FRAME - Verifique a camera", flush=True)
                 first_pass = False

            if ret:
                engine.update_frame(frame)
            else:
                # Opcional: imprimir periodicamente se continuar falhando?
                pass
            
            results = engine.get_results()
            access_controller.process_result(results)

        except Exception as e:
            print(f"DEBUG: Erro no loop: {e}", flush=True)
            pass
        
        time.sleep(0.5)

@ui.page('/')
def main_page():
    layout.build()
    ui.timer(0.5, layout.update_visibility)

def main():
    proc_thread = threading.Thread(target=face_processing_loop, daemon=True)
    proc_thread.start()
    
    async def window_loop():
        await alert_manager.ensure_hidden_startup()
        while True:
            await asyncio.sleep(0.5)
            await alert_manager.manage_window(access_controller.denied)

    app.on_startup(window_loop)

    try:
        ui.run(
            title="Serviço de Biometria",
            port=8080,
            show=False,
            reload=False,
            native=True,
            window_size=(800, 600)
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"FATAL ERROR in main: {e}")

if __name__ in {"__main__", "__mp_main__"}:
    main()
