import main
import numpy as np
from tkinter import *
from tkinter import ttk
import tkinter as tk
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

# создание формы и заполнение полей
window = Tk()
window.title("Решение краевой задачи для ОДУ")
window.geometry("1920x1080")

window.option_add("*tearOff", FALSE)


main_menu = Menu()
Label(window, text='Введите значение n: ').place(x=0, y=0)


value_n = Entry(window)

value_n.insert(END, 100)

value_n.place(x=180, y=0)






def solution_th():
    n = int(value_n.get())
    x,res1,res2,e = main.numerical_test_task(n)
    max_e = max(e)

    fig, ax = plt.subplots(1, 2)
    fig.set_size_inches(11, 5)
    y = []

    for i, j in zip(res1, res2):
        y.append(abs(i - j))

    ax[0].plot(x, res1, label='u(x)')
    ax[0].plot(x, res2, label='v(x)')
    ax[0].set_title('Графики аналитического и численного решений')
    ax[1].plot(x, y, label='u(x)-v(x)')
    ax[1].set_xlabel('x')
    ax[1].set_ylabel('u(x)-v(x)')
    ax[1].set_title('Разность графиков \nаналитического и численного решений')
    ax[1].legend()
    ax[0].set_xlabel('x')
    ax[0].set_ylabel('y')
    ax[0].legend()
    ax[0].grid(True)
    ax[1].grid(True)
    chart = FigureCanvasTkAgg(fig, window)
    chart.get_tk_widget().place(x=500, y=0)

    # создаем холст для таблицы
    c = Canvas(window, height=1000, width = 1900)
    c.place(x =0, y = 600)
    c.create_rectangle(0, 0, 1900, 600,
                       fill='white',
                       outline='white',
                       width=3,
                       activedash=(5, 4))

    #таблица

    heads = ['i','x_i','u_i','v_i','|u_i-v_i|']

    table = ttk.Treeview(window, show='headings', columns=heads, height=7)

    for header in heads:
        table.heading(header, text=header, anchor='center')
        table.column(header, anchor='center', width=150)

    w = np.zeros((n+1,5), dtype=float).tolist()


    for i in range(n+1):
        for j in range(5):
            if j == 0:
                w[i][j] = i
            elif j == 1:
                w[i][j] = x[i]
            elif j == 2:
                w[i][j] = res1[i]
            elif j == 3:
                w[i][j] = res2[i]
            elif j == 4:
                w[i][j] = e[i]
    for row in w:
        table.insert( '', END, values=row)

    table.place(x=15, y=600)

    #Прокрутка

    scrollbary = Scrollbar(window, orient=VERTICAL)
    table.configure(yscrollcommand=scrollbary.set)
    scrollbary.configure(command=table.yview)
    scrollbary.place(x=0, y=600, width=15, height=165)

    # добавление справки
    editor = Text(width=50, height=10)
    editor.place(x=0, y=200)
    editor.insert(END, "Для решения задачи использована равномерная сетка с числом разбиений ")  # вставка в конец
    editor.insert(END, n)
    editor.insert(END, '\nЗадача должна быть решена с погрешностью не более e=0.5*10^-6')
    editor.insert(END, '\nЗадача решена с погрешностью ')
    editor.insert(END, max_e)


def solution():
    n = int(value_n.get())
    x,res1,res2,e = main.numerical_main_task(n)
    max_e = max(e)
    fig, ax = plt.subplots(1, 2)
    fig.set_size_inches(11, 5)
    y = []

    for i, j in zip(res1, res2):
        y.append(abs(i - j))

    ax[0].plot(x, res1, label='v(x)')
    ax[0].plot(x, res2, '.', label='v2(x)')
    ax[0].set_title('Графики численного решения \nс обычным и половинным шагом')
    ax[1].plot(x, y, label='v(x)-v2(x)')
    ax[1].set_title('Разность графиков численного решения')
    ax[1].set_xlabel('x')
    ax[1].set_ylabel('v(x)-v2(x)')
    ax[0].set_xlabel('X')
    ax[0].set_ylabel('Y')
    ax[0].legend()
    ax[0].grid(True)
    ax[1].grid(True)
    chart = FigureCanvasTkAgg(fig, window)
    chart.get_tk_widget().place(x=500, y=0)

    # создаем холст для таблицы
    c = Canvas(window, height=1000, width = 1900)
    c.place(x =0, y = 600)
    c.create_rectangle(0, 0, 1900, 600,
                       fill='white',
                       outline='white',
                       width=3,
                       activedash=(5, 4))

    # таблица

    heads = ['i', 'x_i', 'v_i', '2v_i', '|v_i-2v_i|']

    table = ttk.Treeview(window, show='headings', columns=heads, height=7)

    for header in heads:
        table.heading(header, text=header, anchor='center')
        table.column(header, anchor='center', width=150)

    w = np.zeros((n + 1, 5), dtype=float).tolist()

    for i in range(n + 1):
        for j in range(5):
            if j == 0:
                w[i][j] = i
            elif j == 1:
                w[i][j] = x[i]
            elif j == 2:
                w[i][j] = res1[i]
            elif j == 3:
                w[i][j] = res2[i]
            elif j == 4:
                w[i][j] = e[i]
    for row in w:
        table.insert('', END, values=row)

    table.place(x=15, y=600)

    # Прокрутка

    scrollbary = Scrollbar(window, orient=VERTICAL)
    table.configure(yscrollcommand=scrollbary.set)
    scrollbary.configure(command=table.yview)
    scrollbary.place(x=0, y=600, width=15, height=165)

    # добавление справки
    editor = Text(width=50, height=10)
    editor.place(x=0, y=200)
    editor.insert(END, "Для решения задачи использована равномерная сетка с числом разбиений ")  # вставка в конец
    editor.insert(END, n)
    editor.insert(END, '\nЗадача должна быть решена с погрешностью не более e=0.5*10^-6')
    editor.insert(END, '\nЗадача решена с погрешностью ')
    editor.insert(END, max_e)



# кнопки

button = Button(window, text='Решение тестовой задачи', command =solution_th)
button.place(x=50, y=50)
button1 = Button(window, text='Решение основной задачи', command =solution)
button1.place(x=50, y=100)





window.config(menu=main_menu)
window.mainloop()

