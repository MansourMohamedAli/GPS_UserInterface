import tkinter as tk
from tkinter import ttk

global command_store
command_store = None


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
        self.tree_column = None
        self.tree_row = None
        self.tree_index = None
        self.scroll = None
        self.title('Configuration')
        self.geometry("1300x600")
        self.minsize(400, 300)
        self.create_widgets()
        # self.bind('<ButtonPress-1>', self.mouse_down)

    def mouse_down(self, event):
        caller = event.widget
        print(type(caller))
        # print('clicked')
    def create_widgets(self):
        """All Frames that make up Configuration Window"""
        tab_frame = ttk.Frame(self, relief=tk.GROOVE)
        side_bar_frame = ttk.Frame(self, relief=tk.GROOVE)
        top_bar_frame = ttk.Frame(self, relief=tk.GROOVE)
        bot_bar_frame = ttk.Frame(self, relief=tk.GROOVE)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=5)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)

        """Tab Frame configuration"""
        tabs = ttk.Notebook(tab_frame, width=202 * 5, height=tab_frame.winfo_height())
        tab_frame.rowconfigure(0, weight=1)
        tab_frame.columnconfigure(0, weight=1)

        """Creating Tab 1"""
        tab1 = tk.Frame(tabs)
        text_list = [('label', 'button'), ('thing', 'click'), ('third', 'something'), ('label1', 'button'),
                     ('label2', 'button'), ('label3', 'button'), ('label4', 'button'),
                     ('label2', 'button'), ('label3', 'button'), ('label4', 'button'),
                     ('label2', 'button'), ('label3', 'button'), ('label4', 'button'),
                     ('label2', 'button'), ('label3', 'button'), ('label4', 'button')]
        self.scroll = ScrollFrame(tab1, 100, 1)

        """Creating Tab 2"""
        tab2 = tk.Frame(tabs)

        """Adding tabs to Tab Notebook Frame"""
        tabs.add(tab1, text='First Tab')
        tabs.add(tab2, text='Second Tab')

        tabs.grid(sticky='nsew')

        """Side Bar Configuration"""
        side_bar_frame.rowconfigure((0, 1, 2), weight=1, uniform='a')
        side_bar_frame.columnconfigure((0, 1), weight=1, uniform='a')

        mid_side_bar_frame = tk.Frame(side_bar_frame)
        mid_side_bar_frame.grid(row=1, columnspan=2, padx=10, pady=10, sticky="nsew")
        # ClientListTree(mid_side_bar_frame, "Machine").pack(fill='both', expand=True)
        clients = ClientListTree(mid_side_bar_frame, "Clients")
        clients.insert(parent='', index=0, values=["VB1"])
        clients.insert(parent='', index=1, values=["VB2"])
        clients.insert(parent='', index=2, values=["VB3"])
        clients.pack(fill='both', expand=True)

        bot_side_bar_frame = tk.Frame(side_bar_frame)
        bot_side_bar_frame.grid(row=2, columnspan=2, padx=10, pady=10, sticky="nsew")
        commands = CommandListTree(bot_side_bar_frame, "Command")
        commands.insert(parent='', index=0, values=["test"])
        commands.insert(parent='', index=1, values=["sdfa"])
        commands.insert(parent='', index=2, values=["vxcvc"])
        commands.pack(fill='both', expand=True)

        """top Bar Configuration"""
        top_label = ttk.Label(top_bar_frame, text="Top Bar")
        top_label.pack(expand=True)
        """bot Bar Configuration"""
        bot_label = ttk.Label(bot_bar_frame, text="Bottom Bar")
        bot_label.pack(expand=True)

        tab_frame.grid(row=1, column=1, sticky='nsew', padx=(10, 5), pady=(10, 10))
        side_bar_frame.grid(row=0, column=0, sticky='nsew', rowspan=3, padx=(10, 5), pady=(10, 10))
        top_bar_frame.grid(row=0, column=1, sticky='nsew', padx=(10, 5), pady=(10, 10))
        bot_bar_frame.grid(row=2, column=1, sticky='nsew', padx=(10, 5), pady=(10, 10))


class ScrollFrame(ttk.Frame):
    def __init__(self, parent, item_height, tree_index):
        super().__init__(master=parent)
        self.pack(expand=True, fill='both')

        # widget data
        self.tree_index = tree_index
        self.tree_row = 0
        self.tree_col = 0
        self.item_height = item_height
        self.list_height = (self.tree_index * item_height)  # Five items per row

        # canvas
        self.canvas = tk.Canvas(self, background='red', scrollregion=(0, 0, self.winfo_width(), self.list_height))
        self.canvas.pack(expand=True, fill='both')

        # display frame
        self.frame = ttk.Frame(self)

        #Adding new tag for frame to allow scroll only when not on treeview
        new_tags = self.frame.bindtags() + ("scroll_frame_bg",)
        self.frame.bindtags(new_tags)
        print(self.frame.bindtags())

        # scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')


        # events
        self.canvas.bind_class('scroll_frame_bg', '<MouseWheel>', lambda event: self.canvas.yview_scroll(-int(event.delta / 60), "units"))
        self.bind('<Configure>', self.update_size_event)
        self.bind_all('<ButtonRelease-1>', self.client_release)

    def update_size_event(self, event):
        if self.list_height >= self.winfo_height():
            height = self.list_height
            self.canvas.bind_class('scroll_frame_bg', '<MouseWheel>',
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
            self.canvas.bind_class('scroll_frame_bg', '<MouseWheel>',
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
        item = TabBarTree(frame, f'{store}')
        item.pack(expand=True, fill='both')
        self.tree_index += 1
        return frame

    def client_release(self, event):
        global client_store
        try:
            start_x = self.winfo_pointerx() - self.winfo_rootx()
            start_y = self.winfo_pointery() - self.winfo_rooty()
            if 0 <= start_x <= self.winfo_width() and 0 <= start_y <= self.winfo_height():
                if client_store:
                    for item in client_store:
                        new_item = self.create_item(item)
                        new_item.grid(row=self.tree_row, column=self.tree_col)

                        if self.tree_row == 0:
                            height = 340
                        else:
                            height = 226 * self.tree_row
                        print(f'tree row= {self.tree_row}')
                        self.update_size_new_item(height)

                        self.tree_row, self.tree_col = self.update_row_column(self.tree_row,
                                                                              self.tree_col)
                    self.update_idletasks()

            else:
                pass
            client_store = None
        except NameError:
            print(None)

    def update_row_column(self, row, column):
        if column >= 4:
            row += 1
            column = 0
        else:
            column += 1
        return row, column


class ClientListTree(ttk.Treeview):
    def __init__(self, parent, *args):
        super().__init__(master=parent, columns=args, show='headings')
        self.args = args
        self.parent = parent
        self.get_tree_headings()
        self.bind('<<TreeviewSelect>>', self.item_select)

    def item_select(self, event):
        tree_selection = list()
        for i in self.selection():
            tree_selection.append(self.item(i)['values'][0])
        global client_store
        client_store = tree_selection

    def get_tree_headings(self):
        for arg in self.args:
            self.heading(arg, text=str(arg))


class CommandListTree(ttk.Treeview):
    def __init__(self, parent, *args):
        super().__init__(master=parent, columns=args, show='headings')
        self.args = args
        self.parent = parent
        self.get_tree_headings()
        tags = self.bindtags() + ("commands",)
        self.bindtags(tags)
        self.bind('<<TreeviewSelect>>', self.item_select)

    def item_select(self, event):
        tree_selection = list()
        for i in self.selection():
            tree_selection.append(self.item(i)['values'][0])
        # print(f'item selected{tree_selection}')
        global command_store
        command_store = tree_selection

    def get_tree_headings(self):
        for arg in self.args:
            self.heading(arg, text=str(arg))


class TabBarTree(ttk.Treeview):
    def __init__(self, parent, *args):
        super().__init__(master=parent, columns=args, show='headings')
        self.args = args
        self.parent = parent
        self.get_tree_headings()
        self.bind('<ButtonRelease-1>', self.command_release)

    def get_tree_headings(self):
        for arg in self.args:
            self.heading(arg, text=str(arg))

    def command_release(self, event):
        global command_store
        # caller = event.widget
        # print(caller)
        start_x = self.winfo_pointerx() - self.winfo_rootx()
        start_y = self.winfo_pointery() - self.winfo_rooty()
        width = self.winfo_width()
        height = self.winfo_height()
        # print(f'{self.args[0]}')
        # print(f'start_x {start_x}')
        # print(f'start_y {start_y}')
        # print(f'tree width {width}')
        # print(f'tree height {height}')
        if command_store:
            if 0 <= start_x <= self.winfo_width() and 0 <= start_y <= self.winfo_height():
                for index, _ in enumerate(command_store):
                    self.insert(parent='', index=tk.END, values=(command_store[index]))
                print(type(command_store))
                command_store = None
            else:
                command_store = None


App('Glass Panel Control', (200, 200))
