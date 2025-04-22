from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import Rectangle
from kivy.uix.widget import Widget






Window.size = (600, 600)
Window.clearcolor = (0.05, 0.05, 0.2, 1)
TextInput.background_color = (0.1, 0.1, 0.3, 1);
TextInput.foreground_color = (1, 1, 1, 1);
Button.background_color = (0.2, 0.3, 0.6, 1);
Button.color = (1, 1, 1, 1)
Window.title = "Построитель графиков"







class MyCanvas(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            # Добавляем изображение
            self.rect = Rectangle(
                source='/Applications/Math_App/dragon.jpg',  # Путь к изображению
                pos=(100, 100),     # Позиция (x, y)
                size=(200, 200)     # Размер (ширина, высота)
            )
        self.bind(size=self.update_rect)   
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size     



            
class Main(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.xmin = TextInput(hint_text="Минимум", multiline=False, size_hint_x=1)
        self.xmax = TextInput(hint_text="Максимум", multiline=False, size_hint_x=1)
    def build(self):
        x = BoxLayout(orientation = 'vertical', size_hint_x=1, padding=10, spacing=10)
        main = BoxLayout(orientation='vertical', size_hint_x=1)  
        bottom = MyCanvas(size_hint=(1, 0.5))
        x.add_widget(self.xmin)
        x.add_widget(self.xmax)
        main.add_widget(x)
        main.add_widget(bottom)
        return main
Main().run()
