import numpy as np
import matplotlib.pyplot as plt
import math


ksi = (math.pi)/4



def k(x):
    if (x<0) or (x>1):
        return 0
    if (x>=0) and (x<ksi):
        return (math.sqrt(2)*math.sin(x))
    if (x>ksi)and(x<=1):
        return (math.cos(x)*math.cos(x))

def q(x):
    if (x<0) or (x>1):
        return 0
    if (x>=0) and (x<ksi):
        return 1
    if (x>ksi)and(x<=1):
        return x*x

def f(x):
    if (x<0) or (x>1):
        return 0
    if (x>=0) and (x<ksi):
        return math.sin(2*x)
    if (x>ksi)and(x<=1):
        return math.cos(x)


def k_t(x):
    if (x<0) or (x>1):
        return 0
    if (x>=0) and (x<ksi):
        return (math.sqrt(2)*math.sin(ksi))
    if (x>ksi)and(x<=1):
        return (math.cos(ksi)*math.cos(ksi))

def q_t(x):
    if (x<0) or (x>1):
        return 0
    if (x>=0) and (x<ksi):
        return 1
    if (x>ksi)and(x<=1):
        return ksi*ksi

def f_t(x):
    if (x<0) or (x>1):
        return 0
    if (x>=0) and (x<ksi):
        return math.sin(2*ksi)
    if (x>ksi)and(x<=1):
        return math.cos(ksi)

def test_task(x):
    if (x<0)or x>1:
        return 0

    # c1 = -0.575591935460424
    # c2 = 0.575591935460424
    c1 = -0.3393176035227834
    c2 = 0.3393176035227834

    # c3 = -0.211143654983572
    # c4 = -1.53397470253939
    c3 = -0.4920418012319509
    c4 = 1.0560782612867800

    if (x>=0)and(x<=ksi):
       #return c1*np.exp(np.sqrt(ksi/(ksi*ksi+2))*x)+c2*np.exp(-np.sqrt(ksi/(ksi*ksi+2))*x)+np.sin(2*ksi)
        return 1.0 + c1*np.exp(x) + c2*np.exp(-x)
    else:
        return c3*np.exp(np.sqrt((ksi*ksi)/(np.cos(ksi)*np.cos(ksi)))*x)+c4*np.exp((-1)*np.sqrt((ksi*ksi)/(np.cos(ksi)*np.cos(ksi)))*x)+(np.cos(ksi)/(ksi*ksi))

def test_task_solution(n):
    h = 1.0/n
    res = []

    for i in range(0,n+1):
        x = i*h
        res.append(test_task(x))
    return res


def numerical_test_task(n):
    result = []
    a_i = []
    d_i = []
    fi_i = []
    x = 0.0
    h = 1.0/n

    for i in range(1,n+1):
        if (x+0.5*h<=ksi):
            a_i.append(k_t(x+0.5*h))

        else:
            if (x>= ksi):
                a_i.append(k_t(x+0.5*h))
            else:
                tmp = n*((ksi-x)/k_t(0.5*(x+ksi))+(x+h-ksi)/k_t(0.5*(x+h+ksi)))
                a_i.append(1.0/tmp)
        x+=h

    x = 0.0
    for i in range(1,n):
        if (x+0.5*h<=ksi):
            d_i.append(q_t(x))
            fi_i.append(f_t(x))
        else:
            if (x-0.5*h>=ksi):
                d_i.append(q_t(x))
                fi_i.append(f_t(x))
            else:
                d_i.append(n*((ksi-x+0.5*h)*q_t(0.5*(x-0.5*h+ksi))+(x+0.5*h-ksi)*q_t(0.5*(x+0.5*h+ksi))))
                fi_i.append(n*((ksi-x+0.5*h)*f_t(0.5*(x-0.5*h+ksi))+(x+0.5*h-ksi)*f_t(0.5*(x+0.5*h+ksi))))
        x+=h
    xi1 = 0.0
    xi2 = 0.0

    v_tmp = [None]*(n+1)
    v_tmp[0] = 1.0
    v_tmp[n] = 0.0

    A = []
    B = []
    C = []

    for i in range(0,n-1):
        A.append(a_i[i]/(h*h))
        B.append(a_i[i+1]/(h*h))
        C.append(A[-1]+B[-1]+d_i[i])

    alpha = []
    beta = []

    alpha.append(xi1)
    beta.append(1.0)

    for i in range(0,n-1):
        alpha.append(B[i]/(C[i]-alpha[i]*A[i]))
        beta.append((fi_i[i]+beta[i]*A[i])/(C[i]-alpha[i]*A[i]))

    for i in range(n-1,0,-1):
        v_tmp[i] = alpha[i]*v_tmp[i+1]+beta[i]

    x = []
    x_tmp = 0
    e = []
    u = test_task_solution(n)
    u[n] = 0.0
    for i in range(0,n+1):
        x.append(x_tmp)
        e.append(np.abs(u[i]-v_tmp[i]))
        x_tmp += h

    return x, u, v_tmp, e


def numerical_task_n(n):

    a_i = []
    d_i = []
    fi_i = []
    x = 0.0
    h = 1.0/n

    for i in range(1,n+1):
        x += h
        if (x<=ksi):
            a_i.append(k(x-0.5*h))
        elif (x-h>=ksi):
            a_i.append(k(x-0.5*h))
        else:
            tmp = n*((ksi-x+h)/k(0.5*(x-h+ksi))+(x-ksi)/k(0.5*(x+ksi)))
            a_i.append(1.0/tmp)

    x = 0.0
    for i in range(1,n):
        x+=h
        if(x+0.5*h<=ksi):
            d_i.append(q(x))
            fi_i.append(f(x))
        elif (x-0.5*h>=ksi):
            d_i.append(q(x))
            fi_i.append(f(x))
        else:
            d_i.append(n*((ksi-x+0.5*h)*q(0.5*(x-0.5*h+ksi))+(x+0.5*h-ksi)*q(0.5*(x+0.5*h+ksi))))
            fi_i.append(n*((ksi-x+0.5*h)*f(0.5*(x-0.5*h+ksi))+(x+0.5*h-ksi)*f(0.5*(x+0.5*h+ksi))))

    xi1 = 0.0
    xi2 = 0.0
    v_tmp = [None] * (n + 1)
    v_tmp[0] = 1.0
    v_tmp[n] = 0.0
    A = []
    B = []
    C = []

    for i in range(0,n-1):
        A.append(a_i[i]/(h*h))
        B.append(a_i[i+1]/(h*h))
        C.append(A[-1]+B[-1]+d_i[i])

    alpha = []
    beta = []

    alpha.append(xi1)
    beta.append(1)

    for i in range(0,n-1):
        alpha.append(B[i]/(C[i]-alpha[i]*A[i]))
        beta.append((fi_i[i]+beta[i]*A[i])/(C[i]-alpha[i]*A[i]))

    for i in range(n-1,0,-1):
        v_tmp[i] = alpha[i]*v_tmp[i+1]+beta[i]

    return v_tmp

def numerical_main_task(n):
    result = []
    v = numerical_task_n(n)
    v2 = numerical_task_n(2*n)


    e = []
    x_tmp = 0.0
    x = []
    h = 1.0/n
    for i in range(0,n+1):
        x.append(x_tmp)
        e.append(np.abs(v[i] - v2[i]))
        x_tmp += h

    v2 = [v2[2 * i] for i in range(n + 1)]
    return x, v, v2, e


#

#n = 100
#numerical_test_task(n)
# h = 1.0/n
# x, res1, res2, e = numerical_test_task(n)
# x1, v, v2, e1 = numerical_main_task(n)


# fig, ax = plt.subplots()
# ax.plot(x,res1,label='u(x)')
# ax.plot(x,res2,label='v(x)')
# ax.legend()

# fig, ax = plt.subplots()
# ax.plot(x1,v,label='v(x)')
# ax.plot(x1,v2,label='2v(x)')
# ax.legend()
# plt.show()
