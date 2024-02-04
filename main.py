import tkinter as tk
from tkinter import ttk
from configuration import Configuration


class App(tk.Tk):
    def __init__(self, title, dimensions):
        # main setup
        super().__init__()
        self.title(title)
        self.geometry(f"{dimensions[0]}x{dimensions[1]}")
        self.minsize(200, 200)
        self.maxsize(300, 300)

        # Widgets
        self.menu = Menu(self)

        # Run
        self.mainloop()


class Menu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(x=0, y=0, relwidth=1, relheight=1)

        self.menu_button_1 = ttk.Button(self, text='Button 1')
        self.menu_button_2 = ttk.Button(self, text='Button 2')
        self.menu_button_3 = ttk.Button(self, text='Button 3')
        self.menu_button_4 = ttk.Button(self, text='Button 4')
        self.menu_button_5 = ttk.Button(self, text='Button 5')
        self.menu_button_6 = ttk.Button(self, text='Button 6')
        self.config_button = ttk.Button(self, text='Configuration', command=Configuration)

        # create the grid
        self.columnconfigure(0, weight=1, uniform='a')
        self.columnconfigure(1, weight=1, uniform='a')

        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=1, uniform='a')
        self.rowconfigure(2, weight=1, uniform='a')
        self.rowconfigure(3, weight=1, uniform='a')

        # place the widgets
        self.menu_button_1.grid(row=0, column=0, sticky='nsew', columnspan=1, padx=(10, 5), pady=(10, 10))
        self.menu_button_2.grid(row=0, column=1, sticky='nsew', columnspan=1, padx=(5, 10), pady=(10, 10))
        self.menu_button_3.grid(row=1, column=0, sticky='nsew', columnspan=1, padx=(10, 5), pady=(10, 10))
        self.menu_button_4.grid(row=1, column=1, sticky='nsew', columnspan=1, padx=(5, 10), pady=(10, 10))
        self.menu_button_5.grid(row=2, column=0, sticky='nsew', columnspan=1, padx=(10, 5), pady=(10, 10))
        self.menu_button_6.grid(row=2, column=1, sticky='nsew', columnspan=1, padx=(5, 10), pady=(10, 10))
        self.config_button.grid(row=3, column=0, sticky='nsew', columnspan=2, padx=(5, 10), pady=(10, 10))




App('Glass Panel Control', (200, 200))
