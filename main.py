import tkinter as tk
from tkinter import ttk
from random import choice


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
        self.geometry("1300x600")
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
        tabs = ttk.Notebook(tabFrame, width=202 * 5, height=tabFrame.winfo_height())
        tabFrame.rowconfigure(0, weight=1)
        tabFrame.columnconfigure(0, weight=1)

        """Creating Tab 1"""
        tab1 = tk.Frame(tabs)
        text_list = [('label', 'button'), ('thing', 'click'), ('third', 'something'), ('label1', 'button'),
                     ('label2', 'button'), ('label3', 'button'), ('label4', 'button'),
                     ('label2', 'button'), ('label3', 'button'), ('label4', 'button'),
                     ('label2', 'button'), ('label3', 'button'), ('label4', 'button'),
                     ('label2', 'button'), ('label3', 'button'), ('label4', 'button')]
        scroll = ScrollFrame(tab1, 100, 1)

        """Creating Tab 2"""
        tab2 = tk.Frame(tabs)

        """Adding tabs to Tab Notebook Frame"""
        tabs.add(tab1, text='First Tab')
        tabs.add(tab2, text='Second Tab')

        tabs.grid(sticky='nsew')

        """Side Bar Configuration"""
        sideBarFrame.rowconfigure((0, 1, 2), weight=1, uniform='a')
        sideBarFrame.columnconfigure((0, 1), weight=1, uniform='a')

        midSideBarFrame = tk.Frame(sideBarFrame)
        midSideBarFrame.grid(row=1, columnspan=2, padx=10, pady=10, sticky="nsew")
        # ClientListTree(midSideBarFrame, "Machine").pack(fill='both', expand=True)
        clients = ClientListTree(midSideBarFrame, "Clients")
        clients.insert(parent='', index=0, values=["VB1"])
        clients.insert(parent='', index=1, values=["VB2"])
        clients.insert(parent='', index=2, values=["VB3"])
        clients.pack(fill='both', expand=True)

        botSideBarFrame = tk.Frame(sideBarFrame)
        botSideBarFrame.grid(row=2, columnspan=2, padx=10, pady=10, sticky="nsew")
        commands = CommandListTree(botSideBarFrame, "Command")
        commands.insert(parent='', index=0, values=["test"])
        commands.insert(parent='', index=1, values=["sdfa"])
        commands.insert(parent='', index=2, values=["vxcvc"])
        commands.pack(fill='both', expand=True)

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

        self.tree_row = 0
        self.tree_column = 0

        def mouse_release(_):
            global client_store
            try:
                start_x = tabs.winfo_pointerx() - tabs.winfo_rootx()
                start_y = tabs.winfo_pointery() - tabs.winfo_rooty()
                if 0 <= start_x <= tabs.winfo_width() and 0 <= start_y <= tabs.winfo_height():
                    if client_store != None:
                        for item in client_store:
                            new_item = scroll.create_item(item)
                            new_item.grid(row=self.tree_row, column=self.tree_column)
                            self.tree_row, self.tree_column = update_row_column(scroll.tree_index,
                                                                                self.tree_row,
                                                                                self.tree_column)
                        self.update_idletasks()
                        if (scroll.tree_index - 1) == 1:
                            height = 340
                        else:
                            height = 226 * (scroll.tree_index - 1)
                        scroll.update_size_new_item(height)
                else:
                    pass
                client_store = None
            except NameError:
                print(None)

        def update_row_column(tree_index, row, column):
            if tree_index < 6:
                row = 0
                column += 1
            else:
                row += 1
                column = 0
            return row, column

        self.bind('<ButtonRelease-1>', mouse_release)

class ScrollFrame(ttk.Frame):
    def __init__(self, parent, item_height, tree_index):
        super().__init__(master=parent)
        self.pack(expand=True, fill='both')

        # widget data
        self.tree_index = tree_index
        self.item_height = item_height
        self.list_height = (self.tree_index * item_height)  # Five items per row

        # canvas
        self.canvas = tk.Canvas(self, background='red', scrollregion=(0, 0, self.winfo_width(), self.list_height))
        self.canvas.pack(expand=True, fill='both')

        # display frame
        self.frame = ttk.Frame(self)

        # scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')

        # events
        self.canvas.bind_all('<MouseWheel>', lambda event: self.canvas.yview_scroll(-int(event.delta / 60), "units"))
        self.bind('<Configure>', self.update_size_event)

    def update_size_event(self, event):
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

    def update_size_new_item(self, new_height):
        if new_height >= self.list_height:
            height = new_height
            self.canvas.bind_all('<MouseWheel>',
                                 lambda event: self.canvas.yview_scroll(-int(event.delta / 60), "units"))
            self.scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
        else:
            height = self.list_height
            self.canvas.unbind_all('<MouseWheel>')
            self.scrollbar.place_forget()

        self.canvas.create_window(
            (0, 0),
            window=self.frame,
            anchor='nw',
            width=self.winfo_width(),
            height=height)

        self.canvas.configure(scrollregion=(0, 0, self.winfo_width(), height))
        self.list_height = height

    def create_item(self, store):
        frame = ttk.Frame(self.frame)
        TabBarTree(frame, f'{store}').pack(expand=True, fill='both')
        self.tree_index += 1
        return frame

class CommandListTree(ttk.Treeview):
    def __init__(self, parent, *args):
        super().__init__(master=parent, columns=args, show='headings')

        def item_select(_):
            self.tree_selection = list()
            for i in self.selection():
                self.tree_selection.append(self.item(i)['values'][0])
            global command_store
            command_store = self.tree_selection

        for arg in args:
            self.heading(arg, text=str(arg))

        self.bind('<<TreeviewSelect>>', item_select)


class ClientListTree(ttk.Treeview):
    def __init__(self, parent, *args):
        super().__init__(master=parent, columns=args, show='headings')

        def item_select(_):
            self.tree_selection = list()
            for i in self.selection():
                self.tree_selection.append(self.item(i)['values'][0])
            global client_store
            client_store = self.tree_selection

        for arg in args:
            self.heading(arg, text=str(arg))

        self.bind('<<TreeviewSelect>>', item_select)

class TabBarTree(ttk.Treeview):
    def __init__(self, parent, *args):
        super().__init__(master=parent, columns=args, show='headings')

        for arg in args:
            self.heading(arg, text=str(arg))

        def mouse_release(_):
            global command_store
            # start_x = self.winfo_pointerx() - self.winfo_rootx()
            # start_y = self.winfo_pointery() - self.winfo_rooty()
            # print(f'start x{start_x}, start y {start_y}')
            try:
                start_x = self.winfo_pointerx() - self.winfo_rootx()
                start_y = self.winfo_pointery() - self.winfo_rooty()

                # print(f'start x{start_x}, start y {start_y}')
                if 0 <= start_x <= self.winfo_width() and 0 <= start_y <= self.winfo_height():
                    if command_store != None:
                        print(command_store)
                        # print(command_store)
                    #     for item in command_store:
                    #         new_item = self.create_item(item)
                    #         new_item.grid(row=self.tree_row, column=self.tree_column)
                    #         self.tree_row, self.tree_column = update_row_column(self.tree_index,
                    #                                                             self.tree_row,
                    #                                                             self.tree_column)
                    #     self.update_idletasks()
                    #     if (scroll.tree_index - 1) == 1:
                    #         height = 340
                    #     else:
                    #         height = 226 * (scroll.tree_index - 1)
                    #     scroll.update_size_new_item(height)
                else:
                    pass
                command_store = None
            except NameError:
                print(None)

        def update_row_column(tree_index, row, column):
            if tree_index < 6:
                row = 0
                column += 1
            else:
                row += 1
                column = 0
            return row, column

        self.bind('<ButtonRelease-1>', mouse_release)

App('Glass Panel Control', (200, 200))
