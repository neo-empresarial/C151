from nicegui import ui
from .. import functions as f

class PinDialog:
    def __init__(self, on_success):
        self.on_success = on_success
        self.dialog = ui.dialog()
        # Use glass card with extra padding
        with self.dialog, ui.card().classes('w11-card w-[360px] items-center p-8'):
            ui.label('Digite o PIN').classes('text-2xl font-normal mb-8')
            
            # Input needs high contrast against glass
            self.pin_input = ui.input(password=True).classes('w-full mb-8 text-center text-3xl tracking-[1em] font-mono')
            self.pin_input.props('outlined rounded input-class="text-center"')
            
            with ui.grid(columns=3).classes('gap-4 w-full'):
                for i in range(1, 10):
                    ui.button(str(i), on_click=lambda x=i: self.pin_input.set_value(self.pin_input.value + str(x))) \
                        .classes('w11-btn bg-white text-lg h-14 shadow-sm hover:shadow-md font-normal')
                
                ui.button('C', on_click=lambda: self.pin_input.set_value('')) \
                    .classes('w11-btn bg-white text-red-500 text-lg h-14 shadow-sm hover:shadow-md font-normal')
                
                ui.button('0', on_click=lambda: self.pin_input.set_value(self.pin_input.value + '0')) \
                    .classes('w11-btn bg-white text-lg h-14 shadow-sm hover:shadow-md font-normal')
                
                ui.button('CONFIRMAR', on_click=self.verify_pin) \
                    .classes('w11-btn bg-primary text-white text-base h-14 col-span-3 font-medium tracking-wide shadow-lg')

    def open(self):
        self.pin_input.value = ''
        self.dialog.open()

    def verify_pin(self):
        user = f.verify_pin(self.pin_input.value)
        if user:
            self.dialog.close()
            self.on_success(user)
        else:
            ui.notify('PIN Inválido', type='negative')
            self.pin_input.value = ''

def render_trigger_button(on_click):
    # Ensure this bar sits at the bottom nicely
    with ui.row().classes('w-full h-auto py-6 items-center justify-center px-6 shrink-0').style('background: var(--surface); border-top: 1px solid var(--border);'):
         ui.button('Entrar com PIN', on_click=on_click).classes('w11-btn bg-white w-full max-w-sm')
