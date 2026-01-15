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
    try:
        engine.start()
        camera_manager.start()
    except Exception:
        pass
    
    while True:
        try:
            ret, frame = camera_manager.read()
            if ret:
                engine.update_frame(frame)
            
            results = engine.get_results()
            access_controller.process_result(results)

        except Exception:
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

    ui.run(
        title="Serviço de Biometria",
        port=8080,
        show=False,
        reload=False,
        native=True,
        window_size=(800, 600)
    )

if __name__ in {"__main__", "__mp_main__"}:
    main()
