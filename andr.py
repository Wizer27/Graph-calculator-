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
import numpy as np
import matplotlib.pyplot as plt
from numpy import *
import numexpr as ne





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
        self.xmin = TextInput(hint_text="Минимум",text = "20",multiline=False, size_hint_x = 1,size_hint_y = 0.1)
        self.xmax = TextInput(hint_text="Максимум",text = '-20',multiline=False, size_hint_x=1,size_hint_y = 0.1)
        self.grin = CheckBox(active=False, color=[100, 100, 100, 5], size_hint_x=0.1,size_hint_y = 0.1)
        self.formula = TextInput(hint_text="Формула",multiline=False, size_hint_x = 1,size_hint_y = 0.1)
        self.fun2 = TextInput(hint_text="Формула",multiline=False, size_hint_x=1,size_hint_y = 0.1)
        self.btn1 = Button(text = "Enter",on_press = self.main)
    def replace_abs_notation(expression):
        """Заменяет |x| на abs(x) в выражении (оригинальная функция без изменений)"""
        stack = []
        result = []
        i = 0
        n = len(expression)

        while i < n:
            if expression[i] == '|':
                if stack:
                    stack.pop()
                    result.append(')')
                else:
                    stack.append('|')
                    result.append('abs(')
                i += 1
            else:
                result.append(expression[i])
                i += 1
                
        result = ''.join(result).replace('^', '**')
        for i in range(len(result)):
            if result[i] == 'x' and (result[i - 1].isdigit() or result[i-1] == ')'):
                result = result[:i] + '*' + result[i:]
                result = ''.join(result)
            if result[i] == 'x' and (result[i + 1] == '(' or result[i + 1].isdigit()):
                result = result[:i+1] + '*' + result[i:]
                result = ''.join(result)
        return result
    def safe_evaluate(expr, variables=None):
        """Безопасная замена ne.evaluate() с ограниченным набором функций"""
        allowed_functions = {
            'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
            'exp': np.exp, 'log': np.log, 'sqrt': np.sqrt,
            'abs': abs

        }
        local_dict = {**(variables or {}), **allowed_functions}
        return ne.evaluate(expr, local_dict=local_dict, global_dict={})
    def main(self,instance):
        x = linspace(-20,20,50)
        try:
            y = self.safe_evaluate(self.replace_abs_notation(self.formula))
        except Exception as e:
            print("Error")
            y = np.zeros_like(x)
        plt.plot(x,y)
        y0 = np.asarray([0] * len(x))
        plt.plot(x, y0, color='black')
        plt.plot(y0, x, color='black')
        plt.show()        
    def build(self):
        main = BoxLayout(orientation='vertical', size_hint_x=1)  
        x = BoxLayout(orientation = 'vertical', size_hint_x=0.5,size_hint_y = 0.5,padding=10, spacing=10)
        bottom = MyCanvas(size_hint=(1, 0.5))
        gr = BoxLayout(orientation='vertical',size_hint_x=0.5,size_hint_y = 0.5)
        fr_box = BoxLayout(orientation='vertical',size_hint_x=0.5,size_hint_y = 0.5)
        x.add_widget(self.xmin)
        x.add_widget(self.xmax)
        gr.add_widget(self.grin)
        fr_box.add_widget(self.formula)
        fr_box.add_widget(self.fun2)
        main.add_widget(x)
        main.add_widget(gr)
        main.add_widget(fr_box)
        main.add_widget(self.btn1)
        #main.add_widget(bottom)
        return main
Main().run()
