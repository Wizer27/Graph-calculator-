import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from numpy import *
import numexpr as ne
# Заголовок приложения
def f(s):
    return ne.evaluate(replace_abs_notation(s), global_dict=None)
def replace_abs_notation(expression):
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
        if expression[i] == 'x' and (expression[i - 1].isdigit() or expression[i-1] == ')'):
            result = expression[:i-1] + '*' + expression[i:]
            result = ''.join(result)
        if expression[i] == 'x' and (expression[i + 1] == '(' or expression[i + 1].isdigit()):
            result = expression[:i+1] + '*' + expression[i:]
            result = ''.join(result)
    return result
# Сайдбар для ввода параметров
with st.sidebar:
    x_min = st.number_input("Минимум", value=0)
    x_max = st.number_input("Максимум", value=10)
    steps = st.slider("Количество точек", 50, 500)
    grid = st.checkbox("Сетка")
    function = st.text_input("Формула", value='x')
    fun2 = st.text_input("Формула",value = '')    
    # Описание функций
    description = st.empty()  # Пустой контейнер для описания

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
    else:
        description.text("")  # Очищаем описание, если функция не распознана
# Генерация данных для графика
x = linspace(x_min, x_max, steps)
try:
    y = eval(function)  # Вычисление значения функции
    if fun2 != '':
        try:
            y2 = eval(fun2)  # Вычисление значения функции
        except Exception as e:
            st.error(f"Ошибка в формуле: {e}")
            y2 = np.zeros_like(x)    
except Exception as e:
    st.error(f"Ошибка в формуле: {e}")
    y = np.zeros_like(x)  # Если ошибка, строим нулевой график
figure = plt.figure()
plt.plot(x, y)
if grid:
    plt.grid()
# Отображение графика в Streamlit
if fun2 != '':
    #fig2 = plt.figure()
        plt.plot(x,y2)    
st.pyplot(figure)   
if fun2 != '':
    try:
        y2 = eval(fun2)  # Вычисление значения функции
    except Exception as e:
        st.error(f"Ошибка в формуле: {e}")
        y2 = np.zeros_like(x)
if fun2 != '':
    #fig2 = plt.figure()
    plt.plot(x,y2)
    #st.pyplot(figure)       
# Построение графика

        
    