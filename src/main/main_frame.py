import tkinter as tk
import matplotlib
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import ttk
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

__author__ = "Juan Bautista"
__version__ = "1.0.0"

class Graphic:
    """
    Class used to graphic data in real time from a sensor.

    Attributes
    ----------
    max_data_x : int
        Range in which the graph will be represented on the x axis, that is, the fragment 0 to x will be shown.
    max_data_y : int
        The number of data that will be taken from the sensor.
    serial_port : str
        The serial port through which it communicates with the arduino uno (default 'COM1')
    speed : int
        The spped through which it comunicates with the  arduino uno (default 9600)

    Methods
    -------
    update_line ()
        Update the data with which the line will be drawn on the graph.
    get_data ()
        Method that updates the data from the sensor.
    """

    def __init__(self, max_data_x = 5, max_data_y = 200, serial_port = 'COM3', speed = 9600):
        """
        Parameters
        ----------
        max_data_x : int
            Range in which the graph will be represented on the x axis, that is, the fragment 0 to x will be shown (default 5).
        max_data_y : int
            The number of data that will be taken from the sensor (default 200).
        serial_port : str
            The serial port through which it communicates with the arduino uno (default 'COM1')
        speed : int
            The speed through which it comunicates with the  arduino uno (default 9600)
        """
        self.max_data_x = max_data_x
        self.max_data_y = max_data_y
        self.serial_port = serial_port
        self.speed = speed

        self.x_array = [0.0]
        self.y_array = [0.0]

        self.thread_input_data = threading.Thread(target=self.get_data, args=())
        self.thread_input_data.start()

    def update_line(self, num, hl):
        """
        Update the data with wich the line will be drawn on the graphic.

        Parameters
        ----------
        num : int
            Variable to test.
        hl : iterable
            Iterable with the new data for the line
        """
        dx = np.array(range(len(self.y_array)))
        dy = np.array(self.y_array)
        hl.set_data(dx, dy)
        return hl,

    def get_data(self):
        """
        Method that gets the new data from the sensor.
        """
        conexion = serial.Serial(self.serial_port, self.speed)
        while True:
            line = conexion.readline().decode("utf-8")
            try:
                self.y_array.append(float(line))
                if len(self.y_array) > 200:
                    self.y_array.pop(0)
            except:
                pass


#ok
class Graphics(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        s = ttk.Style()
        s.configure('My.TFrame', background='red')
        self.configure(style='My.TFrame')
        title = TitleFrame(self, "Plots")
        title.grid(column=0, row=0)
        plots = ListPlotsFrame(self)
        plots.grid(column=0, row=1)

#OK
class ListChecksFrame(ttk.Frame):
    def __init__(self, container, list=["name1", "name2", "name3"]):
        super().__init__(container)
        #s = ttk.Style()
        #s.configure('My.TFrame', background='red')
        #self.configure(style='My.TFrame')
        for name in list:
            button = ttk.Checkbutton(self, text=name)
            button.pack()

#OK
class ListPlotsFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        #s = ttk.Style()
        #s.configure('My.TFrame', background='red')
        #self.configure(style='My.TFrame')
        
        #create a figure
        figure = Figure(figsize=(6,4), dpi=100)
        #create FigureCanvas TkAgg object
        figure_canvas = FigureCanvasTkAgg(figure, self)
        #create toolbar
        NavigationToolbar2Tk(figure_canvas, self)
        #create axes
        g = Graphic()
        fig = plt.figure(figsize=(10,8))
        plt.ylim(800, 1000)
        plt.xlim(0, 200)
        hl = plt.plot(g.x_array, g.y_array)
        lineanimation = animation.FuncAnimation(fig, g.update_line, fargs = (hl), interval=50, blit=True)
        lineanimation.show()
        g.dataCollector.join()
        axes = figure.add_subplot(g)
        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)



#OK
class TitleFrame(ttk.Frame):
    def __init__(self, container, title_frame="Title"):
        super().__init__(container)
        title = ttk.Label(self, text = title_frame)
        title.pack()
#OK
class SideBar(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.columnconfigure(0, weight=1)
        title = TitleFrame(self, "Sensors")
        #s3 = ttk.Style()
        #s3.configure('My3.TFrame', background='blue')
        #title.configure(style = 'My3.TFrame')
        title.grid(column=0, row=0)
        checks = ListChecksFrame(container=self)
        checks.grid(column=0, row=1)
        #self.pack(fill='both', expand=1)
#OK
class MainFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.add_widgets()
        self.pack(fill='both', expand=1)
    
    def add_widgets(self):
        side_bar = SideBar(self)
        #s2 = ttk.Style()
        #s2.configure('My2.TFrame', background='blue')
        #side_bar.configure(style = 'My2.TFrame')
        side_bar.grid(column=0, row = 0)
        graphics = Graphics(self)
        graphics.grid(column=1, row = 0)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Monitoreo de sensores")
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.iconbitmap('./../Images/linux96.ico')

if __name__ == "__main__":
    #create the main window
    app = App()
    #creating the main_frame over the main window
    main_frame = MainFrame(app)
    s = ttk.Style()
    s.configure('My.TFrame', background='white')
    main_frame.configure(style = 'My.TFrame')
    # main_frame.config()
    
    # execute
    app.mainloop()
    
    #app = App()
    #title_frame = TitleFrame(container=app, title_frame="Hola")
    #title_frame.pack()
    #app.mainloop()