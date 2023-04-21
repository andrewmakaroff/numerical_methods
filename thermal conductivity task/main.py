import numpy as np
from tkinter import *
from tkinter import ttk
import math
import matplotlib.pyplot as plt


def get_node(w, i, j):
    i = int(i)
    j = int(j)
    return w[i][j]


def makeData(w):
    # Строим сетку в интервале от -10 до 10, имеющую 100 отсчетов по обоим координатам
    x = x_i
    y = t_j

    # Создаем двумерную матрицу-сетку
    xgrid, ygrid = np.meshgrid(x, y)


    # В узлах рассчитываем значение функции
    zgrid= np.zeros([len(t_j), len(x_i)])
    for i in range(len(w)):
        for j in range(len(w[i])):
            zgrid[i][j] = get_node(w,i,j)

    return xgrid, ygrid, zgrid


def teploprovodnost(n, m, l, T):
    gamma = 3.0
    n = int(n)
    m = int(m)
    l = int(l)
    T = int(T)
    h = l / n  # шаг сетки по х
    t = T / m  # шаг сетки по времени

    if t<(h*h)/(2*gamma):
        # зададим сетку
        global x_i
        global t_j
        x_i = np.arange(0, l+h, h)  # значения в узлах по х
        t_j = np.arange(0, T+t, t)  # значение в узлах по t
        r_j = len(t_j)  # количество узлов по t
        r_i = len(x_i)  # количество узлов по x
        w_h_t = np.zeros([r_j, r_i])  # итоговая сетка размером x_i*t_j
        # зададим значение функции входящей в начальное уравнение
        #print(w_h_t)


        x = 0

        def g(x,t):

            return (t/(t+1))*np.cos(np.pi*x)

        def fi(x):

            return 1-(x*x)

        def m1(t):
            return np.cos(t)

        def m2(t):
            return np.sin(4*t)



        # граничные условия
        ux_0 = m1(t_j)  # граничное условие на левом конце при x=0
        ut_0 = fi(x_i)  # граничное условие при t=0

        # найдем значения на нулевом слое при t=0 ut_0 = fi(x_i)
        w_h_t[0] = fi(x_i)

        # найдем значения w_h_t на первом и последующих слоях
        const = t / (h ** 2)


        for j in range(1,m+1):
            w_h_t[j, 0] = m1(t_j[j])
            w_h_t[j, n] = m2(t_j[j])


        for j in range(0, len(w_h_t) -1 ):
            for i in range(1,len(w_h_t[j]) - 1 ):
                w_h_t[j + 1, i] = w_h_t[j, i] + const * gamma* (w_h_t[j, i + 1] - 2 * w_h_t[j, i] + w_h_t[j, i - 1]) + t * g(x_i[i],t_j[j])




        # В
        for line in w_h_t:
            print(*line)
        return(w_h_t)

    else:
        return 0

n = 3  # максимальное число шагов по х
m = 1000 # максимальное число шагов по t
l = 1  # значение х на правой границе

T = 10  # максимальное значение времени t на правой границе

print(np.sin(0.04))
#teploprovodnost(n,m,l,T)



