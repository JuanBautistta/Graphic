from random import randint
from time import sleep
import tkinter as tk
from tkinter import NSEW, ttk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import serial
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading

# ### GLOBAL VARIABLES ### #

plot_names = ['plot1', 'plot2', 'plot3']

#values for graphs

x_vals  = np.arange(100).tolist()
y_vals  = np.arange(100).tolist()
y_vals2 = np.arange(100).tolist()

# figure

fig = Figure()

gs = fig.add_gridspec(2, 1, hspace=0.5, wspace=2)
ax, ax2 = gs.subplots()

#ax = fig.add_subplot(211)
ax.set_title('Plots')
ax.set_xlabel('Time')
ax.set_ylabel('Data')
ax.set_xlim(0, 100)
ax.set_ylim(900, 1000)

#ax2 = fig.add_subplot(212)
ax2.set_title('Plots')
ax2.set_xlabel('Time')
ax2.set_ylabel('Data')
ax2.set_xlim(0, 100)
ax2.set_ylim(0, 100)

# ### FUNCTIONS ### #

#get data all the time
def get_data():
    global y_vals
    connection = serial.Serial('COM3',9600)
    while True:
        try:
            line = connection.readline().decode('utf-8')
            y_vals.append(float(line))
            if len(y_vals) > 100:
                y_vals.pop(0)
            y_vals2.append(randint(0,100))
            y_vals2.pop(0)
        except:
            pass

def animate(i):
    global y_vals, ax, x_vals, y_vals2, ax2
    #y_vals = y_vals[0:100]
    #y_vals = y_vals[-100:]
    #ax = plt.gcf().get_axes()
    #ax = fig.get_axes()
    
    #y_vals.append(randint(0,100))
    #print(y_vals)
    #y_vals = y_vals[-100:]
    #print(y_vals)

    ax.cla()
    ax.set_title('Plots')
    ax.set_xlabel('Time')
    ax.set_ylabel('Data')
    ax.set_ylim(900, 1000)
    ax.set_xlim(0, 100)
    ax.plot(x_vals, y_vals, color='orange')

    ax2.cla()
    ax2.set_title('Plots')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Data')
    ax2.set_ylim(0, 100)
    ax2.set_xlim(0, 100)
    ax2.plot(x_vals, y_vals2, color='purple')

    '''
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
    '''

# ### GUI ### #

# main window
root = tk.Tk()
root.title('Real Time Plots')
root.configure(background='blue')
root.geometry('{0}x{1}+0+0'.format(root.winfo_screenwidth(), root.winfo_screenheight()))

# main frame
style_main_frame = ttk.Style()
style_main_frame.configure('MainFrame.TFrame', background='light blue')
main_frame = ttk.Frame(root)
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=4)
main_frame.configure(style='MainFrame.TFrame')
main_frame.pack(fill='both', expand=1, padx=10, pady=10)

# side bar frame
style_side_bar_frame = ttk.Style()
style_side_bar_frame.configure('SideBar.TFrame', background='red')
side_bar_frame = ttk.Frame(main_frame)
side_bar_frame.configure(style='SideBar.TFrame')
side_bar_frame.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)

# title side bar frame
title_side_bar = ttk.Label(side_bar_frame, text='Sensors')
title_side_bar.pack(padx=10, pady=10)

for i in range(len(plot_names)):
    current_plot = ttk.Checkbutton(side_bar_frame, text=plot_names[i])
    current_plot.pack(fill=tk.X, padx=10)

# graphics frame
style_graphics_frame = ttk.Style()
style_graphics_frame.configure('Graphics.TFrame', background='orange')
graphics_frame = ttk.Frame(main_frame)
graphics_frame.configure(style='Graphics.TFrame')
graphics_frame.grid(column=1, row=0, sticky=tk.NSEW, padx=10, pady=10)

#title graphic frame
title_graphics = ttk.Label(graphics_frame, text='Graphics')
title_graphics.pack(padx=10, pady=10)

#plots frame
plots_frame = ttk.Frame(graphics_frame)
plots_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

################## ANIMATION ###################

thread_input_data = threading.Thread(target=get_data, args=())
thread_input_data.start()

canvas = FigureCanvasTkAgg(fig, master=plots_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
#fig.subplots(2,1)

ani = FuncAnimation(fig, animate, interval=100, blit=False)

root.mainloop()
thread_input_data.join()