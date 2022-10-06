import tkinter as tk
from tkinter import ttk
from matplotlib import container

from matplotlib.pyplot import title

class SideBar(ttk.Frame):
    def _init__(self, container):
        super().__init__(container)
        title = TitleFrame(self, "Sensors")
        title.grid(column=0, row=0)
        #checks = ListChecksFrame(container=self)
        #checks.grid(column=0, row=1)
        #self.pack(fill='both', expand=1)

class Graphics(ttk.Frame):
    def _init__(self, container):
        super().__init__(container)
        s = ttk.Style()
        s.configure('My.TFrame', background='red')
        self.configure(style='My.TFrame')
        title = TitleFrame(self, "Plots")
        title.grid(column=0, row=0)
        plots = ListPlotsFrame(self)
        plots.grid(column=0, row=1)

class ListChecksFrame(ttk.Frame):
    def __init__(self, container, list=["name1", "name2", "name3"]):
        super().__init__(container)
        s = ttk.Style()
        s.configure('My.TFrame', background='red')
        self.configure(style='My.TFrame')
        for name in list:
            button = ttk.Checkbutton(self, text=name)
            button.pack(fill=tk.X)
            pass

class ListPlotsFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        s = ttk.Style()
        s.configure('My.TFrame', background='red')
        self.configure(style='My.TFrame')

class TitleFrame(ttk.Frame):
    def __init__(self, container, title_frame="Title"):
        super().__init__(container)
        title = ttk.Label(self, text = title_frame)
        title.pack()


class MainFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.add_widgets()
        self.pack(fill='both', expand=1)
    
    def add_widgets(self):
        side_bar = SideBar(self)
        s2 = ttk.Style()
        s2.configure('My2.TFrame', background='blue')
        side_bar.configure(style = 'My2.TFrame')
        side_bar.grid(column=0, row = 0, sticky='NS', padx=5, pady=5)
        # graphics = Graphics(self)
        # graphics.grid(column=1, row = 0)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Monitoreo de sensores")
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.iconbitmap('./../Images/linux96.ico')

if __name__ == "__main__":

    
    #create main frame of the app
    app = App()
    
    main_frame = MainFrame(app)
    s = ttk.Style()
    s.configure('My.TFrame', background='red')
    main_frame.configure(style = 'My.TFrame')
    # main_frame.config()
    
    # execute
    app.mainloop()
    
    #app = App()
    #title_frame = TitleFrame(container=app, title_frame="Hola")
    #title_frame.pack()
    #app.mainloop()