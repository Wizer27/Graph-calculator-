import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from numpy import *
import numexpr as ne

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
    for i in range(len(expression)):
        if expression[i] == 'x' and expression[i - 1].isdigit():
            result = expression[:i] + '*' + expression[i:]
            result = ''.join(result)
       # if expression[i] == 'x' and (expression[i + 1] == '(' or expression[i + 1].isdigit()):
           # result = expression[:i+1] + '*' + expression[i:]
            #result = ''.join(result)
    return result

# Streamlit интерфейс (без изменений)
tit = st.title("Построитель графиков")
with st.sidebar:
    x_min = st.number_input("Минимум", value=-10)
    x_max = st.number_input("Максимум", value=10)
    steps = st.slider("Количество точек", 50, 500)
    grid = st.checkbox("Сетка")
    function = st.text_input("Формула", value='x') + ' '
    fun2 = st.text_input("Формула", value='')   
    
    description = st.empty()

    if 'sin' in function:
        description.text("Синус - это тригонометрическая функция, которая описывает колебания.")
    elif 'cos' in function:
        description.text("Косинус - это тригонометрическая функция, которая также описывает колебания, но со сдвигом фазы.")
    elif 'tan' in function:
        description.text("Тангенс - это тригонометрическая функция, которая описывает отношение синуса к косинусу.")
    elif 'exp' in function:
        description.text("Экспонента - это функция, которая описывает экспоненциальный рост или затухание.")
    elif 'log' in function:
        description.text("Логарифм - это функция, обратная экспоненте, которая описывает рост или затухание в логарифмической шкале.")
    elif 'sqrt' in function:
        description.text("Квадратный корень - это функция, которая возвращает квадратный корень из числа.")
    elif 'sin' not in function and 'cos' not in function and 'tan' not in function and 'exp' not in function and 'log' not in function and 'sqrt' not in function:
        description.text("Линейная функция - вида kx + b, некоторые переменные могут отсутствовать.")   
    else:
        description.text("")  
print(replace_abs_notation(function))
# Вычисления (с заменой ne.evaluate на safe_evaluate)
x = linspace(x_min, x_max, steps)
try:
    y = safe_evaluate(replace_abs_notation(function), {'x': x})
except Exception as e:
    st.error(f"Ошибка в формуле: {e}")
    y = np.zeros_like(x) 

if fun2 != '':
    fun2 = fun2 + ' '
    try:
        y2 = safe_evaluate(replace_abs_notation(fun2), {'x': x})
    except Exception as e:
        st.error(f"Ошибка в формуле: {e}")
        y2 = np.zeros_like(x)        

# Построение графика (без изменений)
figure = plt.figure()
plt.plot(x, y)
if fun2 != '':
    plt.plot(x, y2)    

y0 = np.asarray([0] * len(x))
plt.plot(x, y0, color='black')
plt.plot(y0, x, color='black')

if grid:
    plt.grid()

st.pyplot(figure)
def test():
    pass
