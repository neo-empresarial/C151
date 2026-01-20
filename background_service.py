import threading
import time
import asyncio
from nicegui import ui, app
from src.common.utils import find_free_port
from src.services.services import camera_manager, engine, db_manager
from src.services.access_control import AccessController
from src.services.alert_manager import AlertManager
from src.services.ui_layout import UILayout
from src.common.logger import AppLogger
import logging

access_controller = AccessController()
alert_manager = AlertManager()
layout = UILayout(access_controller, db_manager)

def face_processing_loop():
    AppLogger.log("Loop de processamento iniciado.", "info")
    try:
        engine.start()
        AppLogger.log("Engine iniciada.", "info")
        camera_manager.start()
        if camera_manager.cap is None or not camera_manager.cap.isOpened():
             AppLogger.log("AVISO - Falha ao abrir a câmera no reset inicial.", "warning")
        else:
             AppLogger.log("Câmera iniciada com sucesso.", "info")

    except Exception as e:
        AppLogger.log(f"Erro na inicialização: {e}", "error")
        pass
    
    first_pass = True
    while True:
        try:
            ret, frame = camera_manager.read()
            if first_pass:
                 if ret:
                      AppLogger.log("PRIMEIRO FRAME LIDO COM SUCESSO!", "info")
                 else:
                      AppLogger.log("FALHA AO LER PRIMEIRO FRAME - Verifique a camera", "error")
                 first_pass = False

            if ret:
                engine.update_frame(frame)
            else:
                pass
            
            results = engine.get_results()
            access_controller.process_result(results)
            
            if int(time.time()) % 10 == 0:
                 print(f"DEBUG: Background Loop - Denied={access_controller.denied}, Results={len(results)}", flush=True)

        except Exception as e:
            AppLogger.log(f"Erro no loop: {e}", "error")
            pass
        
        time.sleep(0.5)

@ui.page('/')
def main_page():
    layout.build()
    ui.timer(0.5, layout.update_visibility)

def main():
    AppLogger.setup()
    proc_thread = threading.Thread(target=face_processing_loop, daemon=True)
    proc_thread.start()
    
    async def window_loop():
        await alert_manager.ensure_hidden_startup()
        while True:
            await asyncio.sleep(0.5)
            await alert_manager.manage_window(access_controller.denied)

    app.on_startup(window_loop)

    try:
        port = find_free_port()
        AppLogger.log(f"Starting Background Service UI on port {port}", "info")
        ui.run(
            title="Serviço de Biometria",
            port=port,
            show=False,
            reload=False,
            native=True,
            fullscreen=True,
            window_size=(800, 600)
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        AppLogger.log(f"FATAL ERROR in main: {e}", "error")

if __name__ in {"__main__", "__mp_main__"}:
    main()
