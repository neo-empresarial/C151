from nicegui import ui
import base64

def render(container, photos, on_delete):
    container.clear()
    with container:
        for photo in photos:
            with ui.card().classes('p-2 flex flex-col gap-2 items-center bg-white shadow-sm hover:shadow-md transition-all'):
                b64_img = base64.b64encode(photo['image_blob']).decode('utf-8')
                ui.image(f'data:image/jpeg;base64,{b64_img}').style('height: 150px; width: auto; min-width: 100px; object-fit: contain;').classes('rounded border border-gray-200')
                ui.button('Remover', icon='delete', color='negative', on_click=lambda _, pid=photo['id']: on_delete(pid)).props('flat dense size=sm w-full')
