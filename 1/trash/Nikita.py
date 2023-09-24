
import numpy as np
from matplotlib import pyplot as plt
import sympy as sp
import math as ms
from scipy.spatial import distance
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

def start():

    # Условие
    x = sp.Symbol('x')
    y = sp.Symbol('y')
    a = sp.Symbol('a')
    
    a = eval(param_entry.get())
    h = eval(accuracy_entry.get())

    #X = x + y + a*x*(1-x)
    #Y = y + a*x*(1-x)

    X=eval(Firstpoint_equation_1.get())
    Y=eval(Firstpoint_equation_2.get())

    # Ручной ввод
    V1 = [eval(First_vector_entry_X.get()), eval(First_vector_entry_Y.get())]
    V2 = [eval(Second_vector_entry_X.get()),  eval(Second_vector_entry_Y.get())]

    # Длинна отрезка

    def length(a, b):
        [x1, y1], [x2, y2] = a, b
        return (((x1-x2)**2)+((y1-y2)**2))**0.5

    # Функция для итерирования

    def gen(a, b):

        # Отобразили полученные не отображённые границы отрезков
        # Нужно для определения длинны отрезка

        x1 = X.subs({x: a[0], y: a[1]})
        y1 = Y.subs({x: a[0], y: a[1]})
        x2 = X.subs({x: b[0], y: b[1]})
        y2 = Y.subs({x: b[0], y: b[1]})

        # Проверка на точность

        if length([x1, y1], [x2, y2]) > h:
            return gen(a, [(a[0]+b[0])/2, (a[1]+b[1])/2])+gen([(a[0]+b[0])/2, (a[1]+b[1])/2], b)
        else:
            return [X.subs({x: a[0], y: a[1]}), Y.subs({x: a[0], y: a[1]})]

    # Взято тут    
    # https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/

    def ccw(A,B,C):
        [ax, ay] = A
        [bx, by] = B
        [cx, cy] = C
        return (cy-ay)*(bx-ax) > (by-ay)*(cx-ax)
    

    def intersect(A,B,C,D):
            return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)


    def coef(a, b):
        (x1, y1) = a[0]
        (x2, y2) = a[1]
        (X1, Y1) = b[0]
        (X2, Y2) = b[1]
        if intersect(a[0], a[1], b[0], b[1]) == True:
            a1, b1, c1 = 1/(x2-x1), -1/(y2-y1), x1/(x2-x1) - y1/(y2-y1)
            a2, b2, c2 = 1/(X2-X1), -1/(Y2-Y1), X1/(X2-X1) - Y1/(Y2-Y1)
            if (a1*b2-a2*b1) != 0:
                ha = [(c1*b2-c2*b1)/(a1*b2-a2*b1), (a1*c2-a2*c1)/(a1*b2-a2*b1)]
                if (ha[0] == 0) and (ha[1] == 0):
                    return 0
                else:
                    if (min(x1, x2) <= ha[0]) and (max(x1, x2) >= ha[0]):
                        if (min(X1, X2) <= ha[0]) and (max(X1, X2) >= ha[0]):
                            if (min(y1, y2) <= ha[1]) and (max(y1, y2) >= ha[1]):
                                if (min(Y1, Y2) <= ha[1]) and (max(Y1, Y2) >= ha[1]):
                                    return ha
            else:
                return 0
        else: 
            return 0

    # Для V1

    V1_x_folder = [0.0, V1[0], X.subs({x: V1[0], y: V1[1]})]
    V1_y_folder = [0.0, V1[1], Y.subs({x: V1[0], y: V1[1]})]

    # Отобразили новые точки
    
    for i in range(0):
        X_current =X.subs({x: V1_x_folder[-1], y: V1_y_folder[-1]})
        Y_current = Y.subs({x: V1_x_folder[-1], y: V1_y_folder[-1]})
        V1_x_folder.append(X_current)
        V1_y_folder.append(Y_current)
    
    # Проверили содержание массивов

    print(V1_x_folder)
    print(V1_y_folder)

    # Объединяем результаты работы рекурсивной функции и полученные ранее границы отрезков

    u = []
    for i in range(len(V1_x_folder)-1):
        u = u + gen([V1_x_folder[i], V1_y_folder[i]], [V1_x_folder[i+1], V1_y_folder[i+1]])
    #print(u)
    V1_x_folder, V1_y_folder = u[0::2], u[1::2]
    

    
    # Для V2

    # Другие формулы для Х и У

    X=eval(Secondpoint_equation_1.get())
    Y=eval(Secondpoint_equation_2.get())

    #X = x - y
    #Y = y - a*(x-y)*(1-x+y)

    V2_x_folder = [0.0, V2[0], X.subs({x: V2[0], y: V2[1]})]
    V2_y_folder = [0.0, V2[1], Y.subs({x: V2[0], y: V2[1]})]

    for i in range(0):
        X_current =X.subs({x: V2_x_folder[-1], y: V2_y_folder[-1]})
        Y_current = Y.subs({x: V2_x_folder[-1], y: V2_y_folder[-1]})
        V2_x_folder.append(X_current)
        V2_y_folder.append(Y_current)
        
    print(V2_x_folder)
    print(V2_y_folder)
    
    u = []
    for i in range(len(V2_x_folder)-1):
        u = u + gen([V2_x_folder[i], V2_y_folder[i]], [V2_x_folder[i+1], V2_y_folder[i+1]])
    print(u)
    V2_x_folder, V2_y_folder = u[0::2], u[1::2]
    
    def intersection(V1_x_folder, V1_y_folder, V2_x_folder, V2_y_folder):
        first_list = list(zip(V1_x_folder,V1_y_folder))
        second_list = list(zip(V2_x_folder, V2_y_folder))
        for i in range(len(first_list)-1):
            for j in range(len(second_list)-1):
                saver = coef([first_list[i], first_list[i+1]], [second_list[j], second_list[j+1]])
                if saver != 0 and saver != None:                
                    V1_x_folder = V1_x_folder[:i+1] 
                    V1_x_folder.append(saver[0])
                    V2_x_folder = V2_x_folder[:j+1] 
                    V2_x_folder.append(saver[0])
                    V1_y_folder = V1_y_folder[:i+1] 
                    V1_y_folder.append(saver[1])
                    V2_y_folder = V2_y_folder[:j+1] 
                    V2_y_folder.append(saver[1])
                    return [[V1_x_folder, V1_y_folder], [V2_x_folder, V2_y_folder]]
    
    u = intersection(V1_x_folder, V1_y_folder, V2_x_folder, V2_y_folder)

    plt.plot(*u[0], color = first_plot.get(), label='Прямое отображение')
    plt.plot(*u[1], color = second_plot.get(), label='Обратное отображение')
    plt.grid()
    plt.legend()
    plt.show()

#   Интерфейс

window = Tk() 
window.resizable(True, True)

window.title('Нахождение гомоклинических точек')

tool_bar_1 = Frame(window, highlightbackground="gray", highlightthickness=1)
tool_bar_1.grid(column=0, row=0, columnspan=1)

tool_bar_2 = Frame(window, highlightbackground="gray", highlightthickness=1)
tool_bar_2.grid(column=1, row=0, columnspan=1)

tool_bar = Frame(window, highlightbackground="gray", highlightthickness=1)
tool_bar.grid(column=0, row=1, columnspan=2)

start_btn = Button(
    master = tool_bar, 
    text = 'Решить', 
    command = start, 

)
start_btn.grid(column=0, row=7)

iter_btn = Button(
    master = tool_bar, 
    text = 'Итерация', 
    command = start, 

)
iter_btn.grid(column=1, row=7)

accuracy_label=Label(tool_bar, text="Введите точность:")
accuracy_label.grid(column=0, row=0, sticky=E)

accuracy_entry = Entry(tool_bar, width=17)
accuracy_entry.grid(column=1, row=0)
accuracy_entry.insert(END, '0.1')

param_label=Label(tool_bar, text="Введите параметр:")
param_label.grid(column=0, row=1, sticky=E)

First_vector_label=Label(tool_bar_1, text="Первая точка")
First_vector_label.grid(column=0, row=0, columnspan=2)

Firstpoint_equation_1 = Entry(tool_bar_1, width=20)
Firstpoint_equation_1.grid(column=1, row=1)
Firstpoint_equation_1.insert(END, "x + y + a*x*(1-x)")

Firstpoint_equation_2 = Entry(tool_bar_1, width=20)
Firstpoint_equation_2.grid(column=1, row=2)
Firstpoint_equation_2.insert(END, "y + a*x*(1-x)")

First_point_x_label = Label(tool_bar_1, text="X:")
First_point_x_label.grid(column=0, row=4, sticky=E)

First_vector_entry_X = Entry(tool_bar_1, width=17)
First_vector_entry_X.grid(column=1, row=4, sticky=W)
First_vector_entry_X.insert(END, '((11**0.5)+1)/2')

First_point_y_label = Label(tool_bar_1, text="Y:")
First_point_y_label.grid(column=0, row=5, sticky=E)

First_vector_entry_Y = Entry(tool_bar_1, width=17)
First_vector_entry_Y.grid(column=1, row=5, sticky=W)
First_vector_entry_Y.insert(END, '1')



Second_vector_label=Label(tool_bar_2, text="Вторая точка")
Second_vector_label.grid(column=0, row=0, columnspan=2)

Secondpoint_equation_1 = Entry(tool_bar_2, width=20)
Secondpoint_equation_1.grid(column=1, row=1)
Secondpoint_equation_1.insert(END, "x - y")

Secondpoint_equation_2 = Entry(tool_bar_2, width=20)
Secondpoint_equation_2.grid(column=1, row=2)
Secondpoint_equation_2.insert(END, "y - a*(x-y)*(1-x+y)")

Second_point_x_label = Label(tool_bar_2, text="X:")
Second_point_x_label.grid(column=0, row=4, sticky=E)

Second_vector_entry_X = Entry(tool_bar_2, width=17)
Second_vector_entry_X.grid(column=1, row=4, sticky=W)
Second_vector_entry_X.insert(END, '((11**0.5)-1)/2')

Second_point_y_label = Label(tool_bar_2, text="Y:")
Second_point_y_label.grid(column=0, row=5, sticky=E)

Second_vector_entry_Y = Entry(tool_bar_2, width=17)
Second_vector_entry_Y.grid(column=1, row=5, sticky=W)
Second_vector_entry_Y.insert(END, '-1')

param_entry = Entry(tool_bar, width=17)
param_entry.grid(column=1, row=1)
param_entry.insert(END, '1.35')

first_plot = ttk.Combobox(
    tool_bar_1,
    width = 5,
    state="readonly",
    values=['red', 'blue', 'green', 'black', 'yellow', 'cyan', 'magenta']
)
first_plot.grid(column=0, row=6, columnspan=2)
first_plot.current(0)

second_plot = ttk.Combobox(
    tool_bar_2,
    width = 5,
    state="readonly",
    values=['red', 'blue', 'green', 'black', 'yellow', 'cyan', 'magenta']
)
second_plot.grid(column=0, row=6, columnspan=2)
second_plot.current(3)
'''
window.columnconfigure(0, minsize=500)
window.rowconfigure(0, minsize=200)
'''
window.mainloop()
