from random import randint
from time import sleep
import tkinter as tk
from tkinter import IntVar, ttk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import serial
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading

# GLOBAL VARIABLES

lock = threading.Lock()

plots_dict = {
    'plot0' : np.arange(100).tolist(),
    'plot1' : np.arange(100).tolist(),
    'plot2' : np.arange(100).tolist()
}

fig  = Figure()
gs   = fig.add_gridspec(len(plots_dict), hspace=1, wspace=2)
axes = gs.subplots()

# FUNCTIONS

def get_data():
    global plots_dict
    connection = serial.Serial('COM3', 9600)
    while True:
        try:
            line = connection.readline().decode('utf-8')
            line_list = line.split()
            name = line_list[0] 
            value = line_list[1]
            for n in list(plots_dict.keys()):
                n = str(n)
                if n == name:
                    lista = plots_dict[name]
                    lista.append(float(value))
                    if len(lista) > 100:
                        lista.pop(0)
        except:
            pass

def animate(i):
    lock.acquire()
    global plots_dict, axes
    if len == 0:
        current_axe = axes
        current_axe.cla()
    elif len(plots_dict) == 1:
        current_axe = axes
        current_axe.cla()
        current_axe.set_title('Plot1')
        current_axe.set_xlabel('Time')
        current_axe.set_ylabel('Value')
        current_axe.plot(np.arange(100).tolist(), list(plots_dict.values())[0])
    else:
        for i in range(len(plots_dict)):
            current_axe = axes[i]
            current_axe.cla()
            current_axe.set_title('Plot' + str(i))
            current_axe.set_xlabel('Time')
            current_axe.set_ylabel('Value')
            current_axe.plot(np.arange(100).tolist(), list(plots_dict.values())[i])
    lock.release()

def uptade_plots():
    lock.acquire()
    global plots_dict, gs, axes, plots_checked,fig
    for p in plots_checked:
        print(plots_dict)
        print(p, plots_checked[p].get())
        if plots_checked[p].get() == 0 and p in plots_dict:
            fig.clf()
            plots_dict.pop(p)
            if len(plots_dict) > 0:
                gs   = fig.add_gridspec(len(plots_dict), hspace=1, wspace=2)
                axes = gs.subplots()

        if plots_checked[p].get() == 1 and not(p in plots_dict):
            fig.clf()
            plots_dict.update({p : np.arange(100).tolist()})
            gs   = fig.add_gridspec(len(plots_dict), hspace=1, wspace=2)
            axes = gs.subplots()
    lock.release()
    '''
    if flag:
        fig.clf()
        plots_dict.update({key : np.arange(100).tolist()})
        gs   = fig.add_gridspec(len(plots_dict), 1, hspace=1, wspace=2)
        axes = gs.subplots()
    else:
        fig.clf()
        plots_dict.pop(key)
        gs   = fig.add_gridspec(len(plots_dict), 1, hspace=1, wspace=2)
        axes = gs.subplots()
    '''

# GUI

root = tk.Tk()
root.title('Real Time Plots')
root.geometry('{0}x{1}+0+0'.format(root.winfo_screenwidth(), root.winfo_screenheight()))

main_frame = ttk.Frame(root)
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=4)
main_frame.pack(fill='both', expand=1, padx=10, pady=10)

side_bar_frame = ttk.Frame(main_frame)
side_bar_frame.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)

title_side_bar = ttk.Label(side_bar_frame, text='Sensors')
title_side_bar.pack(padx=10, pady=10)

plots_checked = {
    'plot0' : IntVar(value=1),
    'plot1' : IntVar(value=1),
    'plot2' : IntVar(value=1)
}

for p in plots_checked:
    plots_checked[p] = IntVar(value=1)
    l = ttk.Checkbutton(side_bar_frame, text=p, variable=plots_checked[p], command=uptade_plots)
    l.pack(fill=tk.X, padx=10)

#for i in range(len(plots_checked)):
#    current_plot = ttk.Checkbutton(side_bar_frame, text=list(plots_checked.keys())[i], command=lambda:uptade_plots(False,list(plots_checked.keys())[i]), variable=plots_checked[list(plots_checked.keys())[i]])
#    current_plot.pack(fill=tk.X, padx=10)

graphics_frame = ttk.Frame(main_frame)
graphics_frame.grid(column=1, row=0, sticky=tk.NSEW, padx=10, pady=10)

title_graphics = ttk.Label(graphics_frame, text='Graphics')
title_graphics.pack(padx=10, pady=10)

plots_frame = ttk.Frame(graphics_frame)
plots_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# ANIMATION

thread_input_data = threading.Thread(target=get_data, args=())
thread_input_data.start()

canvas = FigureCanvasTkAgg(fig, master=plots_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

ani = FuncAnimation(fig, animate, interval=100, blit=False)

root.mainloop()
thread_input_data.join()