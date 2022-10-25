import tkinter as tk
from tkinter import ttk
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import serial
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading

# Global variables

plot_names = ['plot1', 'plot2', 'plot3']
data_list = []
data = np.array([])
connection = serial.Serial('COM3', 9600)

# PLOTS

fig = Figure()
ax = fig.add_subplot(111)
ax.set_title('Plots')
ax.set_xlabel('Time')
ax.set_ylabel('Data')
ax.set_xlim(0, 100)
ax.set_ylim(900, 1000)
lines = ax.plot([], [])[0]

# Functions

def animate(i, connection):
    global data
    connection.write(b'g')
    input_data = connection.readline().decode('ascii')
    try:
        data.append(float(input_data))
    except:
        pass

    data = data[-100:]
    lines.set_xdata(np.arrange(0, len(data)))
    lines.set_ydata(data)
    canvas.draw()

    #ax.clear()
    #ax.plot(data_list)
    #ax.set_title('Plots')
    #ax.set_xlabel('Time')
    #ax.set_ylabel('Data')
    #ax.set_ylim(0, 100)
    #ax.set_xlim(900, 1000)

# GUI


root = tk.Tk()
root.title('Real Time Plots')
root.configure(background='blue')
root.geometry('{0}x{1}+0+0'.format(root.winfo_screenwidth(), root.winfo_screenheight()))

style_main_frame = ttk.Style()
style_main_frame.configure('MainFrame.TFrame', background='light blue')
main_frame = ttk.Frame(root)
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=4)
main_frame.configure(style='MainFrame.TFrame')
main_frame.pack(fill='both', expand=1, padx=10, pady=10)

style_side_bar_frame = ttk.Style()
style_side_bar_frame.configure('SideBar.TFrame', background='orange')
side_bar_frame = ttk.Frame(main_frame)
side_bar_frame.configure(style='SideBar.TFrame')
side_bar_frame.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)

title_side_bar = ttk.Label(side_bar_frame, text='Sensors')
title_side_bar.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)

for i in range(len(plot_names)):
    current_plot = ttk.Checkbutton(side_bar_frame, text=plot_names[i])
    current_plot.grid(row=i + 1, column=0, sticky=tk.NSEW, padx=10)

style_graphics_frame = ttk.Style()
style_graphics_frame.configure('Graphics.TFrame', background='orange')
graphics_frame = ttk.Frame(main_frame)
graphics_frame.configure(style='Graphics.TFrame')
graphics_frame.grid(column=1, row=0, sticky=tk.NSEW, padx=10, pady=10)

title_graphics = ttk.Label(graphics_frame, text='Graphics')
title_graphics.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)

plots_frame = ttk.Frame(graphics_frame)
plots_frame.grid(column=0, row=1, sticky=tk.NSEW, padx=10, pady=10)

ani = animation.FuncAnimation(fig, animate, frames=100, fargs=(connection), interval=100)

canvas = FigureCanvasTkAgg(fig, master=plots_frame)
canvas.get_tk_widget().pack(fill='both', expand=1)
canvas.draw()

root.mainloop()
