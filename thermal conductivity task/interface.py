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
window.title("Численное решение уравнения теплопроводности")
window.geometry("1920x1080")

window.option_add("*tearOff", FALSE)


main_menu = Menu()
Label(window, text='Введите значение n: ').place(x=0, y=0)
Label(window, text='Введите значение m: ').place(x=0, y=20)
#Label(window, text='Введите левое значение х: ').place(x=0, y=40)
Label(window, text='Введите правое значение X: ').place(x=0, y=40)
#Label(window, text='Введите левое значение t: ').place(x=0, y=80)
Label(window, text='Введите правое значение T: ').place(x=0, y=60)


value_n = Entry(window)
value_m = Entry(window)
#value_x0 = Entry(window)
value_x = Entry(window)
#value_t0 = Entry(window)
value_t = Entry(window)

value_n.insert(END, 10)
value_m.insert(END, 10000)
#value_x0.insert(END, 0)
value_x.insert(END, 1)
#value_t0.insert(END, 0)
value_t.insert(END, 10)



value_n.place(x=180, y=0)
value_m.place(x=180, y=20)
#value_x0.place(x=180, y=40)
value_x.place(x=180, y=40)
#value_t0.place(x=180, y=80)
value_t.place(x=180, y=60)

# добавление справки

canvas = tk.Canvas(window, height=700, width=700)
image = Image.open("nm_text_2.png")
photo = ImageTk.PhotoImage(image)
image = canvas.create_image(0, 0, anchor='nw',image=photo)
canvas.place(x = 0, y = 100)


def makeData(w):
    # Строим сетку в интервале от -10 до 10, имеющую 100 отсчетов по обоим координатам
    x = get_x_i(value_n.get(),value_x.get())
    y = get_t_j(value_m.get(),value_t.get())

    # Создаем двумерную матрицу-сетку
    xgrid, ygrid = np.meshgrid(x, y)


    # В узлах рассчитываем значение функции
    zgrid= np.zeros([len(w), len(w[0])])
    for i in range(len(w)):
        for j in range(len(w[i])):
            zgrid[i][j] = main.get_node(w,i,j)

    return xgrid, ygrid, zgrid

def get_x_i(n,x):
    n = int(n)
    x = int(x)
    h = float(x/n)
    x_i = np.arange(0, x + h, h)
    return x_i

def get_t_j(m,T):
    m = int(m)
    T = int(T)
    t = T/m
    t_j = np.arange(0, T + t, t)
    return t_j

def solution():
    # создаем холст для таблицы
    c = Canvas(window, height=1000, width = 1900)
    c.place(x =0, y = 600)
    c.create_rectangle(0, 0, 1900, 600,
                       fill='white',
                       outline='white',
                       width=3,
                       activedash=(5, 4))
    # графики

    x,y,z = makeData(main.teploprovodnost(value_n.get(), value_m.get(), value_x.get(), value_t.get()))
    fig = plt.figure(figsize=(16, 16))
    ax = fig.add_subplot(1, 2, 1, projection='3d')
    ax.grid(True)
    ax.plot_surface(x, y, z, color='skyblue')
    #ax.set_title("Численные решения")
    chart = FigureCanvasTkAgg(fig, window)
    chart.get_tk_widget().place(x=500, y=-500)


    # таблица
    w = main.teploprovodnost(value_n.get(),value_m.get(),value_x.get(),value_t.get())
    table_w = np.zeros((len(w)+1, len(w[0])+3), dtype=float).tolist()

    print(table_w)
    for j in range(2,len(w[0])+2):
        table_w[0][j] = get_x_i(value_n.get(),value_x.get())[j-2]
    for i in range(1,len(w)+1):
        table_w[i][1] = get_t_j(value_m.get(), value_t.get())[i-1]
        table_w[i][0] = i-1
        for j in range(2,len(w[0])+2):
           table_w[i][j] = w[i-1,j-2]
    table_w[0][0] = 'Номер слоя '
    table_w[0][1] = 'Узел t  \  Узел x'
    tuple_w = []
    #print(table_w)
    for i in table_w:
        tuple_w.append(tuple(i))

    heads = []
    heads.append('')
    heads.append('Номер узла x')
    for i in range(2,len(get_x_i(value_n.get(),value_x.get()))+2):
        heads.append(i-2)

    table = ttk.Treeview(window, show='headings', columns=heads, height=7)

    for header in heads:
        table.heading(header, text=header, anchor='center')
        table.column(header, anchor='center', width=100)
    table.column(heads[0],anchor='center',width=100)
    for row in tuple_w:
        table.insert( '', END, values=row)

    table.place(x=15, y=600)

    # Прокрутка

    scrollbary = Scrollbar(window, orient=VERTICAL)
    scrollbarx = Scrollbar(window, orient=HORIZONTAL)
    table.configure(yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbarx.configure(command=table.xview)
    scrollbary.configure(command=table.yview)
    scrollbary.place(x=0, y=600, width=15, height=165)
    #scrollbarx.place(x=15, y=650, width=165, height=15)


# кнопка

button = Button(window, text='Построить решение', command =solution)
button.place(x=350, y=50)






window.config(menu=main_menu)
window.mainloop()

