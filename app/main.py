from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Rectangle
import os
import time

# Importar funciones de operaciones de archivo
from file_operations import copy_file, move_file, delete_file, rename_file, compress_file, decompress_file

# Ajustar el tamaño de la ventana para simular un teléfono
Window.size = (360, 640)

class FileManager(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.current_path = 'C:\\Users\\ander\\OneDrive\\Documentos\\CarpetaPrueba'  # Ruta inicial alternativa

        # Encabezado de la aplicación con altura reducida y diseño mejorado
        self.header = BoxLayout(size_hint_y=None, height='40dp', padding=[10, 10, 10, 10], spacing=10)
        with self.header.canvas.before:
            Color(1, 0.5, 0, 1)  # Naranja
            self.header_rect = Rectangle(size=self.header.size, pos=self.header.pos)
        self.header.bind(size=self._update_rect, pos=self._update_rect)
        self.header.add_widget(Label(text='File Manager', font_size='20sp', bold=True, color=get_color_from_hex('#FFFFFF')))
        self.add_widget(self.header)

        # Sección de scroll para la lista de archivos
        self.scroll_view = ScrollView(size_hint=(1, 1), bar_width=10, bar_color=get_color_from_hex('#AAAAAA'))
        self.file_list = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=[10, 10, 10, 10])
        self.scroll_view.add_widget(self.file_list)
        self.add_widget(self.scroll_view)

        # Barra de navegación inferior mejorada
        self.nav_bar = BoxLayout(size_hint_y=None, height='60dp', spacing=10)
        self.nav_bar.add_widget(Button(text='Files', on_press=self.browse_files, font_size='14sp'))
        self.nav_bar.add_widget(Button(text='Recents', font_size='14sp'))
        self.nav_bar.add_widget(Button(text='Storage', on_press=self.storage_analysis, font_size='14sp'))
        self.add_widget(self.nav_bar)

        self.update_file_list(self.current_path)

    def _update_rect(self, instance, value):
        self.header_rect.pos = instance.pos
        self.header_rect.size = instance.size

    def update_file_list(self, path):
        self.file_list.clear_widgets()
        if not os.path.exists(path):
            self.show_error_popup(f'La ruta especificada no existe: {path}')
            return

        try:
            items = os.listdir(path)
            item_height = 80  # Altura de cada elemento
            max_scroll_height = Window.height * 0.8  # Altura máxima del ScrollView
            total_height = len(items) * item_height  # Altura total necesaria

            # Ajustar la altura del ScrollView según el número de archivos
            self.scroll_view.height = min(total_height, max_scroll_height)
            self.file_list.height = total_height  # Ajustar la altura del GridLayout

            for item in items:
                item_path = os.path.join(path, item)
                file_info = BoxLayout(orientation='horizontal', size_hint_y=None, height=f'{item_height}dp', spacing=10)

                # Información del archivo
                info_layout = BoxLayout(orientation='vertical')
                info_layout.add_widget(Label(text=item, font_size='16sp', color=get_color_from_hex('#FFFFFF')))

                # Tamaño y fecha del archivo
                size = os.path.getsize(item_path)
                mtime = time.strftime('%d.%m.%Y, %H:%M %p', time.gmtime(os.path.getmtime(item_path)))
                info_layout.add_widget(Label(text=f'{size // 1024} kB   {mtime}', font_size='12sp', color=get_color_from_hex('#AAAAAA')))

                file_info.add_widget(info_layout)

                # Añadir la disposición del archivo a la lista
                self.file_list.add_widget(file_info)
        except Exception as e:
            print(f'Error updating file list: {e}')
            self.show_error_popup(f'Error updating file list: {e}')

    def browse_files(self, instance):
        self.update_file_list(self.current_path)

    def storage_analysis(self, instance):
        path = self.current_path
        total_size = self.get_storage_usage(path)
        details = self.get_file_details(path)
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=f'Total Size: {total_size} bytes', font_size='14sp'))
        if details:
            content.add_widget(Label(text=f'Last Modified: {details["last_modified"]}', font_size='14sp'))
        popup = Popup(title='Storage Analysis', content=content, size_hint=(0.8, 0.8))
        popup.open()

    def show_error_popup(self, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message, font_size='14sp'))
        popup = Popup(title='Error', content=content, size_hint=(0.8, 0.8))
        content.add_widget(Button(text='OK', on_press=popup.dismiss))
        popup.open()

    def show_success_popup(self, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message, font_size='14sp'))
        popup = Popup(title='Success', content=content, size_hint=(0.8, 0.8))
        content.add_widget(Button(text='OK', on_press=popup.dismiss))
        popup.open()

    def copy_file(self, src, dst):
        if copy_file(src, dst):
            self.show_success_popup(f'File copied successfully: {os.path.basename(src)}')
            self.update_file_list(self.current_path)
        else:
            self.show_error_popup(f'Failed to copy file: {os.path.basename(src)}')

    def move_file(self, src, dst):
        if move_file(src, dst):
            self.show_success_popup(f'File moved successfully: {os.path.basename(src)}')
            self.update_file_list(self.current_path)
        else:
            self.show_error_popup(f'Failed to move file: {os.path.basename(src)}')

    def delete_file(self, path):
        if delete_file(path):
            self.show_success_popup(f'File deleted successfully')
            self.update_file_list(self.current_path)
        else:
            self.show_error_popup(f'Failed to delete file')

    def rename_file(self, src, dst):
        if rename_file(src, dst):
            self.show_success_popup(f'File renamed successfully')
            self.update_file_list(self.current_path)
        else:
            self.show_error_popup(f'Failed to rename file')

    def compress_file(self, src, dst):
        if compress_file(src, dst):
            self.show_success_popup(f'File compressed successfully: {os.path.basename(dst)}')
            self.update_file_list(self.current_path)
        else:
            self.show_error_popup(f'Failed to compress file: {os.path.basename(src)}')

    def decompress_file(self, src, dst):
        if decompress_file(src, dst):
            self.show_success_popup(f'File decompressed successfully: {os.path.basename(src)}')
            self.update_file_list(self.current_path)
        else:
            self.show_error_popup(f'Failed to decompress file: {os.path.basename(src)}')

    def on_copy_button_press(self, instance):
        src = 'ruta_del_archivo_origen'
        dst = 'ruta_del_archivo_destino'
        self.copy_file(src, dst)

    def on_move_button_press(self, instance):
        src = 'ruta_del_archivo_origen'
        dst = 'ruta_del_archivo_destino'
        self.move_file(src, dst)

    def on_delete_button_press(self, instance):
        path = 'ruta_del_archivo_a_eliminar'
        self.delete_file(path)

    def on_rename_button_press(self, instance):
        src = 'ruta_del_archivo_actual'
        dst = 'nuevo_nombre_del_archivo'
        self.rename_file(src, dst)

    def on_compress_button_press(self, instance):
        src = 'ruta_del_archivo_a_comprimir'
        dst = 'ruta_del_archivo_comprimido.zip'
        self.compress_file(src, dst)

    def on_decompress_button_press(self, instance):
        src = 'ruta_del_archivo_comprimido.zip'
        dst = 'carpeta_de_destino'
        self.decompress_file(src, dst)

class FileManagerApp(App):
    def build(self):
        return FileManager()

if __name__ == '__main__':
    FileManagerApp().run()
