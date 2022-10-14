import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import serial

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


if __name__ == "__main__":
    """
    Main method from which the application is executed
    """
    g = Graphic()
    fig = plt.figure(figsize=(10,8))
    plt.ylim(800, 1000)
    plt.xlim(0, 200)
    hl = plt.plot(g.x_array, g.y_array)
    lineanimation = animation.FuncAnimation(fig, g.update_line, fargs = (hl), interval=50, blit=True)
    plt.show()
    g.dataCollector.join()
