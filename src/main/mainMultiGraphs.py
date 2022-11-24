from random import randint
from time import sleep
import tkinter as tk
from tkinter import IntVar, ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import serial
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
import os

class App:
    """
    Class used to graphic data in real time from a multiple sensor.

    Attributes
    ----------
    plots_dict : dict
        A dictionary with the name of the sensors as a key and whose value is its first 100 values obtained, 
        these values can in principle be pure zeros.
    port : str
        The serial port through which it communicates with the arduino uno (default 'COM1')
    speed : int
        The spped through which it comunicates with the  arduino uno (default 9600)
    
    Methods
    -------
    get_data ()
        Method that updates the data from the sensor.
    animate ()
        Method that performs the update of the information of the graph.
    update_plots()
        Method that removes or adds graphs to the graphical interface depending on the graphs 
        selected in the graphical interface.
    create_gui()
        Method responsible for creating the graphical interface, as well as initializing all the necessary 
        programs in the background so that the user can interact with it.
    on_closing()
        Method responsible for properly ending the application, 
        closing all background applications that are running.
    """

    def __init__(self, plots_dict: dict, port: str = "COM3", speed: int = 9600) -> None:
        """
        constructor method

        Parameters
        ----------
        plots_dict : int
            A dictionary with the name of the sensors as a key and whose value is its first 100 values obtained, 
            these values can in principle be pure zeros.
        port : str
            The serial port through which it communicates with the arduino uno (default 'COM1')
        speed : int
            The spped through which it comunicates with the  arduino uno (default 9600)
        """
        self.plots_dict = plots_dict
        self.fig = Figure()
        self.gs = self.fig.add_gridspec(len(self.plots_dict), hspace=1, wspace=2)
        self.axes = self.gs.subplots()
        self.port = port
        self.speed = speed
        self.stop = False
        self.root = tk.Tk()

    def get_data(self):
        """
        Method that gets the new data from the sensors.
        """
        connection = serial.Serial(self.port, self.speed)
        while True:
            try:
                if(self.stop):
                    break
                line = connection.readline().decode('utf-8')
                line_list = line.split()
                name = line_list[0]
                value = line_list[1]
                for n in list(self.plots_dict.keys()):
                    n = str(n)
                    if n == name:
                        lista = self.plots_dict[name]
                        lista.append(float(value))
                        if len(lista) > 100:
                            lista.pop(0)
            except:
                pass
    
    def animate(self, i):
        """
        function that updates the graphs so that they are seen in real time
        """
        if len(self.plots_dict) == 1:
            current_axe = self.axes
            current_axe.cla()
            current_axe.set_title('Plot1')
            current_axe.set_xlabel('Time')
            current_axe.set_ylabel('Value')
            current_axe.plot(np.arange(100).tolist(), list(self.plots_dict.values())[0])
        else:
            for i in range(len(self.plots_dict)):
                current_axe = self.axes[i]
                current_axe.cla()
                current_axe.set_title('Plot' + str(i))
                current_axe.set_xlabel('Time')
                current_axe.set_ylabel('Value')
                current_axe.plot(np.arange(100).tolist(), list(self.plots_dict.values())[i])

    def update_plots(self):
        """
        function that adds or removes graphics from the graphical interface.
        """
        for p in self.plots_checked:
            if self.plots_checked[p].get() == 0 and p in self.plots_dict:
                self.fig.clf()
                self.plots_dict.pop(p)
                if len(self.plots_dict) > 0:
                    self.gs   = self.fig.add_gridspec(len(self.plots_dict), hspace=1, wspace=2)
                    self.axes = self.gs.subplots()

            if self.plots_checked[p].get() == 1 and not(p in self.plots_dict):
                self.fig.clf()
                self.plots_dict.update({p : np.arange(100).tolist()})
                self.gs   = self.fig.add_gridspec(len(self.plots_dict), hspace=1, wspace=2)
                self.axes = self.gs.subplots()

    def create_gui(self):
        """
        function to create the graphical interface
        """
        self.root.title("Monitoreo de sensores")
        self.root.geometry(("{0}x{1}+0+0".format(self.root.winfo_screenwidth(), self.root.winfo_screenheight())))
        self.root.iconbitmap(os.path.abspath('../../icos/linux96.ico'))

        main_frame = ttk.Frame(self.root)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=4)
        main_frame.pack(fill='both', expand=1, padx=10, pady=10)

        side_bar_frame = ttk.Frame(main_frame)
        side_bar_frame.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)
        title_side_bar = ttk.Label(side_bar_frame, text='Sensors')
        title_side_bar.pack(padx=10, pady=10)

        self.plots_checked = {
            'plot0' : IntVar(value=1),
            'plot1' : IntVar(value=1),
            'plot2' : IntVar(value=1)
        }

        for p in self.plots_checked:
            self.plots_checked[p] = IntVar(value=1)
            l = ttk.Checkbutton(side_bar_frame, text=p, variable=self.plots_checked[p], command=self.update_plots)
            l.pack(fill=tk.X, padx=10)

        # graphics frame
        graphics_frame = ttk.Frame(main_frame)
        graphics_frame.grid(column=1, row=0, sticky=tk.NSEW, padx=10, pady=10)

        title_graphics = ttk.Label(graphics_frame, text='Graphics')
        title_graphics.pack(padx=10, pady=10)

        # plots frame
        plots_frame = ttk.Frame(graphics_frame)
        plots_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # ANIMATION

        thread_input_data = threading.Thread(target=self.get_data, args=())
        thread_input_data.start()

        canvas = FigureCanvasTkAgg(self.fig, master=plots_frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        ani = FuncAnimation(self.fig, self.animate, interval=100, blit=False)
        ani

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        thread_input_data.join()

    def on_closing(self):
        if messagebox.askokcancel("Quit","Do you want to quit?"):
            self.stop = True
            self.root.destroy()

if __name__ == "__main__":
    """
    Main method from which the application is executed
    """
    p_d = {
        'plot0' : np.arange(100).tolist(),
        'plot1' : np.arange(100).tolist(),
        'plot2' : np.arange(100).tolist()
    }
    app = App(p_d, 'COM3', 9600)
    app.create_gui()
