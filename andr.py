from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.animation import Animation
from kivy.metrics import dp
import numpy as np
import matplotlib.pyplot as plt
from numpy import *
import numexpr as ne





Builder.load_string('''
#:set accent_color 0.2, 0.5, 0.8, 1
#:set dark_bg 0.09, 0.09, 0.12, 1
#:set input_bg 0.12, 0.12, 0.16, 1

<LargeTextInput>:
    background_normal: ''
    background_color: input_bg
    foreground_color: 0.9, 0.9, 0.95, 1
    hint_text_color: 0.5, 0.5, 0.6, 1
    padding: [dp(25), dp(15)]
    font_size: '20sp'
    multiline: False
    size_hint: (None, None)
    size: (dp(450), dp(60))
    canvas.after:
        Color:
            rgba: accent_color if self.focus else (0.3, 0.3, 0.4, 1)
        Line:
            width: dp(2) if self.focus else dp(1.5)
            rounded_rectangle: (self.x, self.y, self.width, self.height, dp(12))

<LargeButton>:
    background_normal: ''
    background_color: accent_color
    color: 0.95, 0.95, 1, 1
    bold: True
    font_size: '22sp'
    size_hint: (None, None)
    size: (dp(450), dp(70))
    canvas.before:
        Color:
            rgba: accent_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(12),]

<MainInterface>:
    orientation: 'vertical'
    spacing: dp(30)
    padding: [dp(40), dp(40), dp(40), dp(30)]
    canvas.before:
        Color:
            rgba: dark_bg
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        spacing: dp(20)
        size_hint_y: None
        height: dp(120)
        
        Label:
            text: "НАСТРОЙКИ ГРАФИКА"
            color: accent_color
            font_size: '24sp'
            bold: True
            size_hint_y: None
            height: dp(40)
            
        BoxLayout:
            orientation: 'horizontal'
            spacing: dp(30)
            size_hint_y: None
            height: dp(70)
            
            LargeTextInput:
                id: x_min
                hint_text: "Минимум X"
                text: "-20"
                
            LargeTextInput:
                id: x_max
                hint_text: "Максимум X"
                text: "20"

    BoxLayout:
        orientation: 'vertical'
        spacing: dp(20)
        size_hint_y: None
        height: dp(200)
        
        Label:
            text: "ФОРМУЛЫ"
            color: accent_color
            font_size: '24sp'
            bold: True
            size_hint_y: None
            height: dp(40)
            
        LargeTextInput:
            id: formula1
            hint_text: "Введите первую формулу"
            
        LargeTextInput:
            id: formula2
            hint_text: "Введите вторую формулу"

    BoxLayout:
        orientation: 'horizontal'
        spacing: dp(20)
        size_hint_y: None
        height: dp(60)
        
        Label:
            text: "Отображать сетку:"
            color: 0.8, 0.8, 0.9, 1
            font_size: '20sp'
            size_hint_x: None
            width: dp(180)
            
        CheckBox:
            id: grid_cb
            active: False
            color: accent_color
            size_hint: (None, None)
            size: (dp(40), dp(40))

    LargeButton:
        id: plot_btn
        text: "ПОСТРОИТЬ ГРАФИК"
        on_press: root.start_plot()
''')
#локальные функции для графиков (не вставляй в класс)
def safe_evaluate(expr, variables=None):
    """Безопасная замена ne.evaluate() с ограниченным набором функций"""
    allowed_functions = {
        'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
        'exp': np.exp, 'log': np.log, 'sqrt': np.sqrt,
        'abs': abs

    }
    local_dict = {**(variables or {}), **allowed_functions}
    return ne.evaluate(expr, local_dict=local_dict, global_dict={})


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

################# Классы #################
##########################################
##########################################

class LargeTextInput(TextInput):
    pass

class LargeButton(Button):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            anim = Animation(background_color=(0.25, 0.6, 1, 1), duration=0.1)
            anim.start(self)
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            anim = Animation(background_color=(0.2, 0.5, 0.8, 1), duration=0.3)
            anim.start(self)
        return super().on_touch_up(touch)

class MainInterface(BoxLayout):
    def start_plot(self):
        print("### WORKING ###")
        x = linspace(int(self.ids.x_min.text),int(self.ids.x_max.text),500)
        print(x)
        try:
            y = safe_evaluate(replace_abs_notation(self.ids.formula1.text), {'x': x})
        except Exception as e:
            print("### ERROR ###")
            y = np.zeros_like(x)
        with open('test.txt','a+') as file:
            file.write(self.ids.formula1.text + '\n')
        y0 = np.asarray([0] * len(x))
        plt.plot(x, y0, color='black')
        plt.plot(y0, x, color='black')    
        plt.plot(x,y)
        plt.show()             
        
       

class GraphApp(App):
    def build(self):
        Window.clearcolor = (0.07, 0.07, 0.1, 1)
        Window.size = (1000, 800)  # Увеличил размер окна
        return MainInterface()

if __name__ == '__main__':
    GraphApp().run()
