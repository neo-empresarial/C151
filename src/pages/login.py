
import base64
import cv2
import time
from nicegui import ui

from src.services.services import camera_manager, db_manager, engine
from src.common.state import state

def login_page():
    # Check if any user exists. If not, force registration of Admin.
    users = db_manager.get_users()
    if not users:
        ui.navigate.to('/setup')
        return

    # Reset State on Entry
    state.current_user = None
    state.is_admin = False

    # Main Container
    with ui.column().classes('w-full h-screen items-center justify-center bg-gray-100 p-4'):
        
        # Card
        with ui.card().classes('w11-card w-full max-w-[1000px] h-[700px] p-0 flex flex-col overflow-hidden shadow-lg'):
            
            # Header
            with ui.row().classes('w-full h-[60px] bg-white border-b border-gray-200 items-center px-6 justify-between shrink-0'):
                ui.label('Reconhecimento Facial').classes('text-xl font-semibold text-gray-800')
                
                # Navigation Actions
                with ui.row().classes('gap-2'):
                    ui.button(icon='home', on_click=lambda: ui.navigate.to('/')).props('flat round dense')
            
            # Camera View Area (Fill remaining space)
            # Using a fixed aspect ratio container or just filling
            # Camera View Area
            # Using ui.image instead of interactive_image for better native compatibility
            with ui.column().classes('w-full h-[500px] bg-black items-center justify-center relative overflow-hidden'):
                
                # Using interactive image for better performance
                video_image = ui.interactive_image().classes('w-full h-full object-cover')
                
                # Face Mask Overlay
                ui.element('div').classes('absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[220px] h-[320px] border-2 border-white/50 rounded-[50%] pointer-events-none shadow-[0_0_0_9999px_rgba(0,0,0,0.5)]')
                
                # Feedback Overlay
                feedback_label = ui.label('Inicializando...').classes('absolute bottom-4 left-1/2 transform -translate-x-1/2 bg-black/60 text-white px-6 py-2 rounded-full text-lg font-medium backdrop-blur-sm z-10')

            
            # Footer / PIN Action
            with ui.row().classes('w-full h-[80px] bg-white border-t border-gray-200 items-center justify-center px-6 shrink-0'):
                 ui.button('Entrar com PIN', on_click=lambda: pin_dialog.open()).classes('w11-btn bg-gray-100 text-gray-800 border border-gray-300 hover:bg-gray-200')


    # --- Logic ---

    def go_dashboard():
        ui.navigate.to('/dashboard')

    def on_access_granted(user):
        state.current_user = user
        feedback_label.text = f"Bem-vindo, {user['name']}!"
        feedback_label.classes(remove='bg-black/60', add='bg-green-600')
        
        if user.get('access_level') == 'Admin':
            state.is_admin = True
            ui.notify('Admin Identificado', type='positive')
            # ui.timer(1.0, lambda: ui.navigate.to('/dashboard'), once=True) # User requested to stay on page
        else:
            ui.notify('Acesso Liberado', type='positive')
            ui.timer(3.0, lambda: reset_state(), once=True)

    def reset_state():
        state.current_user = None
        state.is_admin = False
        feedback_label.text = "Aguardando rosto..."
        feedback_label.classes(remove='bg-green-600', add='bg-black/60')

    # PIN Logic
    pin_dialog = ui.dialog()
    with pin_dialog, ui.card().classes('w11-card w-[320px] items-center p-6'):
        ui.label('Digite o PIN').classes('text-xl font-semibold mb-6')
        pin_input = ui.input(password=True).classes('w-full mb-6 text-center text-2xl tracking-widest')
        
        def verify_pin():
            user = db_manager.get_user_by_pin(pin_input.value)
            if user:
                pin_dialog.close()
                on_access_granted(user)
            else:
                ui.notify('PIN Inválido', type='negative')
                pin_input.value = ''

        with ui.grid(columns=3).classes('gap-3 w-full'):
            for i in range(1, 10):
                ui.button(str(i), on_click=lambda x=i: pin_input.set_value(pin_input.value + str(x))).classes('w11-btn text-lg h-12 bg-gray-50')
            ui.button('C', on_click=lambda: pin_input.set_value('')).classes('w11-btn text-lg h-12 bg-red-50 text-red-600')
            ui.button('0', on_click=lambda: pin_input.set_value(pin_input.value + '0')).classes('w11-btn text-lg h-12 bg-gray-50')
            ui.button('OK', on_click=verify_pin).classes('w11-btn text-lg h-12 bg-blue-600 text-white col-span-3')

    # Loop
    async def loop():
        if state.current_user:
            # Verify if user is still logged in or if we should show something else
            pass
            
        # 1. Capture
        ret, frame = camera_manager.read()
        
        if not ret:
            feedback_label.text = "Câmera desconectada"
            feedback_label.classes(remove='bg-green-600', add='bg-red-600')
            # Clear image or show placeholder if needed
            return

        # 2. Inference
        engine.update_frame(frame)
        results = engine.get_results()
        
        # 3. Draw
        display_frame = frame.copy()
        
        detected_known = False
        user_found = None
        
        for res in results:
            x, y, w, h = res["box"]
            known = res["known"]
            name = res.get("name", "Desconhecido")
            
            color = (0, 255, 0) if known else (100, 100, 100)
            
            cv2.rectangle(display_frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(display_frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
            if known:
                detected_known = True
                user_found = res

        # 4. Update UI Feedback
        if not state.current_user:
            if detected_known:
                feedback_label.text = f"Identificando..."
                feedback_label.classes(remove='bg-black/60', add='bg-blue-600')
            else:
                feedback_label.text = "Aguardando rosto..."
                feedback_label.classes(remove='bg-blue-600', add='bg-black/60')

        # 5. Handle Login
        if detected_known and not state.current_user and user_found:
             on_access_granted(user_found)

        # 6. Update Video Feed
        _, buffer = cv2.imencode('.jpg', display_frame)
        video_image.set_source(f'data:image/jpeg;base64,{base64.b64encode(buffer).decode("utf-8")}')

    # Attach timer
    ui.timer(0.05, loop)
