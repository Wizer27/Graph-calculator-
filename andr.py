from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.togglebutton import ToggleButton
Window.size = (600, 600)
Window.clearcolor = (0.05, 0.05, 0.2, 1)
TextInput.background_color = (0.1, 0.1, 0.3, 1);
TextInput.foreground_color = (1, 1, 1, 1);
Button.background_color = (0.2, 0.3, 0.6, 1);
Button.color = (1, 1, 1, 1)
Window.title = "Построитель графиков"
class Main(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.btn1 = Button(text = 'Test')
    def build(self):
        main = BoxLayout(orientation='vertical', size_hint_x=1)  
        main.add_widget(self.btn1)  
        return main
Main().run()
