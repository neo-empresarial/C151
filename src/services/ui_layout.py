from nicegui import ui

class UILayout:
    def __init__(self, access_controller, db_manager):
        self.access_controller = access_controller
        self.db_manager = db_manager
        self.container = None

    def build(self):
        self.container = ui.element('div').classes('fixed top-0 left-0 w-screen h-screen bg-red-600 flex flex-col justify-center items-center z-[9999]')
        self.container.visible = False
        
        with self.container:
            ui.icon('warning', size='12rem').classes('text-white mb-8 animate-pulse')
            ui.label('ACESSO NEGADO').classes('text-8xl font-black text-white text-center')
            ui.label('ÁREA RESTRITA A ADMINISTRADORES').classes('text-3xl text-white mt-4 font-bold')
            
            with ui.row().classes('mt-10 items-center gap-2'):
                pin_input = ui.input(placeholder='PIN de Admin', password=True).classes('bg-white rounded px-2 text-black text-xl w-40')
                
                def try_unlock():
                    if self.access_controller.unlock_with_pin(pin_input.value, self.db_manager):
                        pin_input.value = ""
                        ui.notify("Acesso Liberado", type='positive')
                    else:
                        ui.notify("PIN Invalido", type='negative')
                        pin_input.value = ""
                
                ui.button('DESBLOQUEAR', on_click=try_unlock).classes('bg-white text-red-600 font-bold text-xl')
    
    def update_visibility(self):
        if self.container:
            self.container.visible = self.access_controller.denied
