from nicegui import ui
from .. import functions as f

class PinDialog:
    def __init__(self, on_success):
        self.on_success = on_success
        self.dialog = ui.dialog()
        with self.dialog, ui.card().classes('w11-card w-[320px] items-center p-6'):
            ui.label('Digite o PIN').classes('text-xl font-semibold mb-6')
            self.pin_input = ui.input(password=True).classes('w-full mb-6 text-center text-2xl tracking-widest')
            
            with ui.grid(columns=3).classes('gap-3 w-full'):
                for i in range(1, 10):
                    ui.button(str(i), on_click=lambda x=i: self.pin_input.set_value(self.pin_input.value + str(x))).classes('w11-btn bg-white text-lg h-12')
                ui.button('C', on_click=lambda: self.pin_input.set_value('')).classes('w11-btn bg-white text-lg h-12 text-red-500')
                ui.button('0', on_click=lambda: self.pin_input.set_value(self.pin_input.value + '0')).classes('w11-btn bg-white text-lg h-12')
                ui.button('OK', on_click=self.verify_pin).classes('w11-btn bg-primary text-lg h-12 col-span-3')

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
    with ui.row().classes('w-full h-[80px] items-center justify-center px-6 shrink-0').style('background-color: var(--surface); border-top: 1px solid var(--border);'):
         ui.button('Entrar com PIN', on_click=on_click).classes('w11-btn bg-white w-full max-w-sm')
