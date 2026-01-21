from nicegui import ui
from .. import functions as f

class PinDialog:
    def __init__(self, on_success):
        self.on_success = on_success
        self.dialog = ui.dialog()
        with self.dialog, ui.card().classes('w11-card w-[420px] items-center p-10 bg-opacity-90'):
            ui.label('Acesso via PIN').classes('text-3xl font-light mb-10 tracking-tight text-center w-full')
            
            self.pin_input = ui.input(password=True).classes('w-full mb-10 text-center text-5xl font-mono tracking-[0.5em] text-primary')
            self.pin_input.props('borderless input-class="text-center placeholder-gray-400 text-primary"')
            self.pin_input.style('background: transparent; border-bottom: 2px solid var(--border); border-radius: 0;')
            
            with ui.grid(columns=3).classes('gap-6 w-full px-4'):
                for i in range(1, 10):
                    ui.button(str(i), on_click=lambda x=i: self.pin_input.set_value(self.pin_input.value + str(x))) \
                        .classes('w11-btn text-2xl h-16 shadow-lg font-light text-primary bg-surface hover:bg-primary/10 backdrop-blur-sm')
                
                ui.button('C', on_click=lambda: self.pin_input.set_value('')) \
                    .classes('w11-btn text-red-400 text-2xl h-16 shadow-lg font-light bg-surface hover:bg-red-50 backdrop-blur-sm')
                
                ui.button('0', on_click=lambda: self.pin_input.set_value(self.pin_input.value + '0')) \
                    .classes('w11-btn text-2xl h-16 shadow-lg font-light text-primary bg-surface hover:bg-primary/10 backdrop-blur-sm')
                
                ui.button('ENTRAR', on_click=self.verify_pin) \
                    .classes('w11-btn bg-primary text-white text-xl h-16 col-span-3 mt-4 tracking-widest shadow-xl hover:scale-105')

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
    with ui.row().classes('w-full justify-center absolute bottom-10 z-20'):
         ui.button('Entrar com PIN', on_click=on_click).classes('w11-btn bg-white px-12 py-4 text-lg backdrop-blur-md shadow-2xl')
