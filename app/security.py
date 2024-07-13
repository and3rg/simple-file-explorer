from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

class Security:
    def __init__(self):
        self.password = None

    def set_password(self, new_password):
        self.password = new_password

    def check_password(self, password):
        return self.password == password

    def show_security_popup(self):
        layout = BoxLayout(orientation='vertical')
        password_input = TextInput(hint_text='Enter Password', password=True)
        layout.add_widget(password_input)
        submit_button = Button(text='Submit', on_press=lambda x: self.submit_password(password_input.text))
        layout.add_widget(submit_button)
        self.popup = Popup(title='Security', content=layout, size_hint=(0.5, 0.5))
        self.popup.open()

    def submit_password(self, password):
        if self.check_password(password):
            print('Access Granted')
            self.popup.dismiss()
        else:
            print('Access Denied')
