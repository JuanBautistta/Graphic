from cmath import exp
import tkinter as tk
import matplotlib
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import ttk
matplotlib.use('TkAgg')
#from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
import serial
import numpy as np

__author__ = "Juan Bautista"
__version__ = "1.0.0"

#main window GUI
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Monitoreo de sensores")
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        #self.iconbitmap('./../Images/linux96.ico')

#OK
class MainFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)
        self.add_widgets()
        self.pack(fill='both', expand=1)
    
    def add_widgets(self):
        #s2 = ttk.Style()
        #s2.configure('My2.TFrame', background='blue')
        #side_bar.configure(style = 'My2.TFrame')
        side_bar = SideBar(self)
        side_bar.grid(column=0, row = 0)
        graphics = Graphics(self)
        graphics.grid(column=1, row = 0)

class SideBar(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        #s3 = ttk.Style()
        #s3.configure('My3.TFrame', background='blue')
        #title.configure(style = 'My3.TFrame')
        self.columnconfigure(0, weight=1)
        title = TitleFrame(self, "Sensors")
        title.grid(column=0, row=0)
        checks = ListChecksFrame(container=self)
        checks.grid(column=0, row=1)
        #self.pack(fill='both', expand=1)

class Graphics(ttk.Frame):

    def __init__(self, container):
        super().__init__(container)
        title = TitleFrame(self, "Plots in real time")
        title.grid(column=0, row=0)
        plots = ListPlotsFrame(self)
        plots.grid(column=0, row=1)

class TitleFrame(ttk.Frame):
    def __init__(self, container, title_frame="Title"):
        super().__init__(container)
        title = ttk.Label(self, text = title_frame)
        title.pack(fill='both', expand=1)


class ListChecksFrame(ttk.Frame):
    def __init__(self, container, list=["name plot 1", "name plot 2", "name plot 3"]):
        super().__init__(container)
        for name in list:
            button = ttk.Checkbutton(self, text=name)
            button.pack(fill='both', expand=1)

#OK
class ListPlotsFrame(ttk.Frame):

    def __init__(self, container, max_data_x=100, max_data_y=100, serial_port = 'COM3', speed = 9600, names=["plot1", "plot2", "plot3"]):
        super().__init__(container)

        self.max_data_x = max_data_x
        self.max_data_y = max_data_y
        self.serial_port = serial_port
        self.speed = speed
        self.x_array = np.array(range(max_data_x))
        self.y_array = [0.0]

        #correr un hilo para obtener los datos de manera concurrente(tiempo real)
        self.thread_input_data = threading.Thread(target=self.get_data, args=())
        self.thread_input_data.start() #correrlo como si fuera un demonio -> investigar

        #plt.style.use('fivethirtyeight')
        #s = ttk.Style()
        #s.configure('My.TFrame', background='red')
        #self.configure(style='My.TFrame')
        
        #create a figure
        #figure = plt.Figure(figsize=(8,4), dpi=100)
        
        #create FigureCanvas TkAgg object
        figure_canvas = FigureCanvasTkAgg(figure, self)
        #create toolbar
        NavigationToolbar2Tk(figure_canvas, self)
        #create axes
        axes = figure.add_subplot(len(names), 1)
        #axes = plt.gcf().get_axes()
        #axes.set_title("Plot #1")
        #axes.set_xlabel("Time")
        #axes.set_ylabel("Value")
        #axes.set_xlim(0, 100)
        #axes.set_ylim(900, 1000)

        #canvas = FigureCanvasTkAgg(figure, master=self) # A tk drawing area
        #canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        #canvas.draw()

        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        figure.subplots(1,1)
        ani = animation.FuncAnimation(figure, self.animate, interval=100, blit=False)
        ani
        plt.show()
        self.thread_input_data.join()

    def animate(self, i, figure):
        axes = figure.add_subplot()
        axes.set_title("Plot 1")
        axes.set_xlabel("Time")
        axes.set_ylabel("Value")
        axes.set_xlim(0, 100)
        axes.set_ylim(900, 1000)
        axes.cla()
        axes.plot(self.x_array, self.y_array)

    def get_data(self):
        conexion = serial.Serial(self.serial_port, self.speed)
        while True:
            line = conexion.readline().decode("utf-8")
            try:
                self.y_array.append(float(line))
                if len(self.y_array) > self.max_data_y:
                    self.y_array.pop(0)
            except:
                pass

if __name__ == "__main__":

    app = App()                                  #create the main window
    main_frame = MainFrame(app)                  #creating the main_frame over the main window
    s = ttk.Style()                              #create new style
    s.configure('My.TFrame', background='light blue') #configure new style
    main_frame.configure(style = 'My.TFrame')    #apply style
    main_frame.config()                        #lock
    app.mainloop()                               # execute
    
    #app = App()
    #title_frame = TitleFrame(container=app, title_frame="Hola")
    #title_frame.pack()
    #app.mainloop()