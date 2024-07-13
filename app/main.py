from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from file_operations import *
from storage_analysis import get_storage_usage, get_file_details
from security import Security
import os

class FileManager(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.current_path = 'C:\\Users\\ander\\OneDrive\\Documents\\simple-file-explorer\\index-file'  # Ruta inicial alternativa
        self.add_widget(Label(text='Simple File Manager'))
        self.add_widget(Button(text='Browse Files', on_press=self.browse_files))
        self.add_widget(Button(text='Storage Analysis', on_press=self.storage_analysis))
        self.add_widget(Button(text='Security Settings', on_press=self.security_settings))
        self.add_widget(Button(text='Change Path', on_press=self.change_path))
        self.security = Security()
        
        # Add a ScrollView to display files and folders
        self.scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height * 0.6))
        self.file_list = GridLayout(cols=1, size_hint_y=None)
        self.scroll_view.add_widget(self.file_list)
        self.add_widget(self.scroll_view)
        
        self.update_file_list(self.current_path)

    def update_file_list(self, path):
        self.file_list.clear_widgets()
        if not os.path.exists(path):
            self.show_error_popup(f'La ruta especificada no existe: {path}')
            return

        try:
            items = os.listdir(path)
            self.file_list.height = len(items) * 40  # Adjust height based on number of items
            for item in items:
                item_path = os.path.join(path, item)
                btn = Button(text=item, size_hint_y=None, height=40, on_press=lambda x, ip=item_path: self.on_item_click(ip))
                self.file_list.add_widget(btn)
        except Exception as e:
            print(f'Error updating file list: {e}')
            self.show_error_popup(f'Error updating file list: {e}')

    def on_item_click(self, path):
        if os.path.isdir(path):
            self.current_path = path
            self.update_file_list(path)
        else:
            self.show_file_options(path)

    def show_file_options(self, path):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Button(text='Copy', on_press=lambda x: self.copy_file(path)))
        content.add_widget(Button(text='Move', on_press=lambda x: self.move_file(path)))
        content.add_widget(Button(text='Delete', on_press=lambda x: self.delete_file(path)))
        content.add_widget(Button(text='Rename', on_press=lambda x: self.rename_file(path)))
        content.add_widget(Button(text='Compress', on_press=lambda x: self.compress_file(path)))
        content.add_widget(Button(text='Decompress', on_press=lambda x: self.decompress_file(path)))
        popup = Popup(title='File Options', content=content, size_hint=(0.8, 0.8))
        popup.open()

    def copy_file(self, path):
        # Implement copy file functionality
        pass

    def move_file(self, path):
        # Implement move file functionality
        pass

    def delete_file(self, path):
        # Implement delete file functionality
        pass

    def rename_file(self, path):
        # Implement rename file functionality
        pass

    def compress_file(self, path):
        # Implement compress file functionality
        pass

    def decompress_file(self, path):
        # Implement decompress file functionality
        pass

    def browse_files(self, instance):
        self.update_file_list(self.current_path)

    def storage_analysis(self, instance):
        path = self.current_path
        total_size = get_storage_usage(path)
        details = get_file_details(path)
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=f'Total Size: {total_size} bytes'))
        if details:
            content.add_widget(Label(text=f'Last Modified: {details["last_modified"]}'))
        popup = Popup(title='Storage Analysis', content=content, size_hint=(0.8, 0.8))
        popup.open()

    def security_settings(self, instance):
        self.security.show_security_popup()

    def change_path(self, instance):
        content = BoxLayout(orientation='vertical')
        input_path = TextInput(text=self.current_path, multiline=False)
        content.add_widget(input_path)
        content.add_widget(Button(text='OK', on_press=lambda x: self.set_new_path(input_path.text)))
        popup = Popup(title='Change Path', content=content, size_hint=(0.8, 0.8))
        popup.open()

    def set_new_path(self, path):
        if os.path.exists(path):
            self.current_path = path
            self.update_file_list(path)
        else:
            self.show_error_popup(f'La nueva ruta especificada no existe: {path}')

    def show_error_popup(self, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        popup = Popup(title='Error', content=content, size_hint=(0.8, 0.8))
        popup.open()

class FileManagerApp(App):
    def build(self):
        return FileManager()

if __name__ == '__main__':
    FileManagerApp().run()
