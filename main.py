import tkinter as tk
from tkinter import ttk
from random import choice

class App(tk.Tk):
    def __init__(self, title, dimensions):
        # main setup
        super().__init__()
        self.title(title)
        self.geometry(f"{dimensions[0]}x{dimensions[1]}")
        self.minsize(600, 600)
        self.maxsize(900, 800)

        # Widgets
        self.menu = Menu(self)

        # Run
        self.mainloop()


class Menu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(x=0, y=0, relwidth=1, relheight=1)

        global open_config

        def open_config():
            Configuration()

        self.create_widgets()

    def create_widgets(self):
        menu_button1 = ttk.Button(self, text='Button 1')
        menu_button2 = ttk.Button(self, text='Button 2')
        menu_button3 = ttk.Button(self, text='Button 3')
        menu_button4 = ttk.Button(self, text='Button 4')
        menu_button5 = ttk.Button(self, text='Button 5')
        menu_button6 = ttk.Button(self, text='Button 6')
        config_button = ttk.Button(self, text='Configuration', command=open_config)

        # create the grid
        self.columnconfigure((0, 1), weight=1, uniform='a')
        self.rowconfigure((0, 1, 2, 3), weight=1, uniform='a')

        # place the widgets
        menu_button1.grid(row=0, column=0, sticky='nsew', columnspan=1, padx=(10, 5), pady=(10, 10))
        menu_button2.grid(row=0, column=1, sticky='nsew', columnspan=1, padx=(5, 10), pady=(10, 10))
        menu_button3.grid(row=1, column=0, sticky='nsew', columnspan=1, padx=(10, 5), pady=(10, 10))
        menu_button4.grid(row=1, column=1, sticky='nsew', columnspan=1, padx=(5, 10), pady=(10, 10))
        menu_button5.grid(row=2, column=0, sticky='nsew', columnspan=1, padx=(10, 5), pady=(10, 10))
        menu_button6.grid(row=2, column=1, sticky='nsew', columnspan=1, padx=(5, 10), pady=(10, 10))
        config_button.grid(row=3, column=0, sticky='nsew', columnspan=2, padx=(5, 10), pady=(10, 10))


class Configuration(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Configuration')
        self.geometry("800x600")
        self.minsize(400, 300)

        self.create_widgets()

    def create_widgets(self):
        """All Frames that make up Configuration Window"""
        tabFrame = ttk.Frame(self, relief=tk.GROOVE)
        sideBarFrame = ttk.Frame(self, relief=tk.GROOVE)
        topBarFrame = ttk.Frame(self, relief=tk.GROOVE)
        botBarFrame = ttk.Frame(self, relief=tk.GROOVE)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=5)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)

        """Tab Frame configuration"""
        tabs = ttk.Notebook(tabFrame, width=tabFrame.winfo_width(), height=tabFrame.winfo_height())
        tabFrame.rowconfigure(0, weight=1)
        tabFrame.columnconfigure(0, weight=1)

        """Creating Tab 1"""
        tab1 = tk.Frame(tabs)
        text_list = [('label', 'button'), ('thing', 'click'), ('third', 'something'), ('label1', 'button'),
                     ('label2', 'button'), ('label3', 'button'), ('label4', 'button'),
                     ('label2', 'button'), ('label3', 'button'), ('label4', 'button'),
                     ('label2', 'button'), ('label3', 'button'), ('label4', 'button'),
                     ('label2', 'button'), ('label3', 'button'), ('label4', 'button')]
        ScrollFrame(tab1, text_list, 100)

        """Creating Tab 2"""
        tab2 = tk.Frame(tabs)
        # ScrollFrame(tab2, text_list, 100)

        """Adding tabs to Tab Notebook Frame"""
        tabs.add(tab1, text='First Tab')
        tabs.add(tab2, text='Second Tab')

        tabs.grid(sticky='nsew')

        """Side Bar Configuration"""
        sideBarFrame.rowconfigure((0, 1, 2), weight=1, uniform='a')
        sideBarFrame.columnconfigure(0, weight=1, uniform='a')

        midSideBarFrame = tk.Frame(sideBarFrame)
        midSideBarFrame.grid(row=1)
        computerList = tk.Listbox(midSideBarFrame, bg='red')
        computerList.pack()

        SideBarTree(sideBarFrame, "Command").grid(row=2)

        """top Bar Configuration"""
        topLabel = ttk.Label(topBarFrame, text="Top Bar")
        topLabel.pack(expand=True)
        """bot Bar Configuration"""
        botLabel = ttk.Label(botBarFrame, text="Bottom Bar")
        botLabel.pack(expand=True)

        tabFrame.grid(row=1, column=1, sticky='nsew', padx=(10, 5), pady=(10, 10))
        sideBarFrame.grid(row=0, column=0, sticky='nsew', rowspan=3, padx=(10, 5), pady=(10, 10))
        topBarFrame.grid(row=0, column=1, sticky='nsew', padx=(10, 5), pady=(10, 10))
        botBarFrame.grid(row=2, column=1, sticky='nsew', padx=(10, 5), pady=(10, 10))


class ScrollFrame(ttk.Frame):
    def __init__(self, parent, text_data, item_height):
        super().__init__(master=parent)
        self.pack(expand=True, fill='both')

        # widget data
        self.text_data = text_data
        self.item_number = len(text_data)
        self.list_height = (self.item_number * item_height)  # Five items per row
        # self.list_height = (20 * item_height) / 5  # Test of 20 items

        # canvas
        self.canvas = tk.Canvas(self, background='red', scrollregion=(0, 0, self.winfo_width(), self.list_height))
        self.canvas.pack(expand=True, fill='both')

        # display frame
        self.frame = ttk.Frame(self)

        row = 0
        column = 0
        for item in range(self.item_number):
            if column > 4:
                row += 1  # Increment the row
                column = 0  # Set column back to 0
            self.create_item(column, item).grid(row=row, column=column, sticky='nsew', padx=5, pady=10)
            column += 1

        # scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')

        # events
        self.canvas.bind_all('<MouseWheel>', lambda event: self.canvas.yview_scroll(-int(event.delta / 60), "units"))
        self.bind('<Configure>', self.update_size)

    def update_size(self, event):
        if self.list_height >= self.winfo_height():
            height = self.list_height
            self.canvas.bind_all('<MouseWheel>',
                                 lambda event: self.canvas.yview_scroll(-int(event.delta / 60), "units"))
            self.scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
        else:
            height = self.winfo_height()
            self.canvas.unbind_all('<MouseWheel>')
            self.scrollbar.place_forget()

        self.canvas.create_window(
            (0, 0),
            window=self.frame,
            anchor='nw',
            width=self.winfo_width(),
            height=height)

    def create_item(self, index, item):
        frame = ttk.Frame(self.frame)
        tk.Listbox(frame, bg='red').pack(expand=True, fill='both')
        return frame


class SideBarTree(ttk.Treeview):
    def __init__(self, parent, *args):
        super().__init__(master=parent, columns=args, show='headings')

        for arg in args:
            self.heading(arg, text=str(arg))






App('Glass Panel Control', (600, 600))
