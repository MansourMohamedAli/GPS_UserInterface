import tkinter as tk
from tkinter import ttk

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


class Configuration(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.tree_column = None
        self.tree_row = None
        self.tree_index = None
        self.scroll = None
        self.title('Configuration')
        self.geometry("1000x600")
        # self.resizable(False, False)
        # self.minsize(400, 300)

        self.tab_frame = ttk.Frame(self, relief=tk.GROOVE)
        self.side_bar_frame = ttk.Frame(self, relief=tk.GROOVE)
        self.top_bar_frame = ttk.Frame(self, relief=tk.GROOVE)
        self.bot_bar_frame = ttk.Frame(self, relief=tk.GROOVE)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=5)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)

        # Tab Frame configuration
        self.tabs = ttk.Notebook(self.tab_frame, width=700, height=self.tab_frame.winfo_height())
        self.tab_frame.rowconfigure(0, weight=1)
        self.tab_frame.columnconfigure(0, weight=1)

        # Creating Tab 1
        self.tab1 = tk.Frame(self.tabs)
        self.scroll = ScrollFrame(self.tab1, 100, 1)

        # Creating Tab 2
        self.tab2 = tk.Frame(self.tabs)

        # Adding tabs to Tab Notebook Frame
        self.tabs.add(self.tab1, text='First Tab')
        self.tabs.add(self.tab2, text='Second Tab')

        self.tabs.grid(sticky='nsew')

        # Side Bar Configuration
        self.side_bar_frame.rowconfigure(0, weight=1, uniform='a')
        self.side_bar_frame.rowconfigure(1, weight=1, uniform='a')
        # self.side_bar_frame.rowconfigure(2, weight=10, uniform='a')
        self.side_bar_frame.columnconfigure(0, weight=1, uniform='a')
        self.side_bar_frame.columnconfigure(1, weight=1, uniform='a')

        self.mid_side_bar_frame = ttk.Frame(self.side_bar_frame)
        self.mid_side_bar_frame.grid(row=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.client_frame = ttk.Frame(self.mid_side_bar_frame)
        self.client_frame.columnconfigure(0, weight=1, uniform='a')
        self.client_frame.columnconfigure(1, weight=1, uniform='a')
        self.client_frame.pack(fill='both', expand=True)

        self.clients = ClientListTree(self.client_frame, "Clients")
        self.clients.insert(parent='', index=0, values=["VB1"])
        self.clients.insert(parent='', index=1, values=["VB2"])
        self.clients.insert(parent='', index=2, values=["VB3"])

        # New Command Button
        self.new_client_button = ttk.Button(self.client_frame,
                                            text="New",
                                            command=lambda: self.insert_row(self.clients))

        # Delete Command Button
        self.delete_client_button = ttk.Button(self.client_frame,
                                               text="Delete",
                                               command=lambda: self.delete_row(self.clients))

        # Adding command section to sidebar.
        self.clients.grid(row=0, columnspan=2)
        self.new_client_button.grid(row=1, column=0, padx=5, pady=5)
        self.delete_client_button.grid(row=1, column=1, padx=5, pady=5)

        self.bot_side_bar_frame = ttk.Frame(self.side_bar_frame)
        self.bot_side_bar_frame.grid(row=1, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.command_frame = ttk.Frame(self.bot_side_bar_frame)
        self.command_frame.columnconfigure(0, weight=1, uniform='a')
        self.command_frame.columnconfigure(1, weight=1, uniform='a')
        self.command_frame.pack(fill='both', expand=True)

        # Command List Tree
        self.commands_tree = CommandListTree(self.command_frame, "Commands")
        self.commands_tree.insert(parent='', index=0, values=["Load VB1"])
        self.commands_tree.insert(parent='', index=1, values=["Load VB2"])
        self.commands_tree.insert(parent='', index=2, values=["Load VB3"])

        self.new_command_button = ttk.Button(self.command_frame,
                                             text="New",
                                             command=CommandWindow)

        # Delete Command Button
        self.delete_command_button = ttk.Button(self.command_frame,
                                                text="Delete",
                                                command=lambda: self.delete_row(self.commands_tree))

        # Adding command section to sidebar.
        self.commands_tree.grid(row=0, columnspan=2)
        self.new_command_button.grid(row=1, column=0, padx=5, pady=5)
        self.delete_command_button.grid(row=1, column=1, padx=5, pady=5)

        # self.commands_tree.pack(fill='both', expand=True)
        # self.new_command_button.pack(side="bottom")

        # Top Bar Configuration
        self.top_label = ttk.Label(self.top_bar_frame, text="Top Bar")
        self.top_label.pack(expand=True)
        # Bottom Bar Configuration
        self.bot_label = ttk.Label(self.bot_bar_frame, text="Bottom Bar")
        self.bot_label.pack(expand=True)

        self.tab_frame.grid(row=1, column=1, sticky='nsew', padx=(10, 5), pady=(10, 10))
        self.side_bar_frame.grid(row=0, column=0, sticky='nsw', rowspan=3, padx=(10, 5), pady=(10, 10))
        self.top_bar_frame.grid(row=0, column=1, sticky='nsew', padx=(10, 5), pady=(10, 10))
        self.bot_bar_frame.grid(row=2, column=1, sticky='nsew', padx=(10, 5), pady=(10, 10))

        # self.update()
        # print(self.side_bar_frame.winfo_width())

    @staticmethod
    def insert_row(tree_list):
        tree_list.insert(parent='', index=tk.END, values='TEST')

    @staticmethod
    def delete_row(tree_list):
        selected_items = tree_list.selection()
        for item in selected_items:
            tree_list.delete(item)

    # @staticmethod
    # def mouse_down(event):
    #     caller = event.widget
    #     print(type(caller))
    #     # print('clicked')


class CommandWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Configuration')
        self.geometry("500x200")
        self.resizable(False, False)


        # Frame for left text
        self.labels_frame = ttk.Frame(self)
        # Command Name Label
        self.command_name_label = ttk.Label(self.labels_frame, text="Command Name:")
        # Command Name Label
        self.command_text_label = ttk.Label(self.labels_frame, text="Command:")
        # Placing Labels
        self.command_name_label.place(relx=0.1, rely=0.1)
        self.command_text_label.place(relx=0.1, rely=0.30)
        # Frame for text entries
        self.text_frame = ttk.Frame(self)
        # Text box for commands
        self.command_name_entry = tk.Entry(self.text_frame, width=53)
        # Text box for commands
        self.command_text_box = tk.Text(self.text_frame, width=40, height=5)
        # Placing Text Boxes
        self.command_name_entry.place(relx=0, rely=0.1)
        self.command_text_box.place(relx=0, rely=0.30)

        # Button Frame
        self.buttons_frame = ttk.Frame(self)
        # Done button



        self.done_button = ttk.Button(self.buttons_frame,
                                      text="Done",
                                      command=lambda: done_press())
        # Add Another Button
        self.add_another_button = ttk.Button(self.buttons_frame,
                                             text="Add Another",
                                             command=lambda: add_another_press())
        # Placing Buttons
        self.done_button.place(relx=0.125, rely=0)
        self.add_another_button.place(relx=0.45, rely=0)

        # Configuring Grid
        self.rowconfigure(0, weight=5)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # Placing frames in grid
        self.labels_frame.grid(row=0, column=0, rowspan=2, sticky='nsew')
        self.text_frame.grid(row=0, column=1, rowspan=2, sticky='nsew')
        self.buttons_frame.grid(row=1, column=1, sticky='nsew')

        def done_press():
            stored_entry = self.command_name_entry.get()
            stored_text = self.command_text_box.get('1.0', 'end')
            # Configuration.commands.insert(parent='', index=tk.END, values='TEST')
            print(f'Command Name = {stored_entry}, Command Text = {stored_text}')

        # @staticmethod
        # def insert_row(tree_list):
        #     tree_list.insert(parent='', index=tk.END, values='TEST')
        def add_another_press():
            pass




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

        # Adding new tag for frame to allow scroll only when not on treeview
        self.new_tags = self.frame.bindtags() + ("scroll_frame_bg",)
        self.frame.bindtags(self.new_tags)

        # scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')

        # events
        self.canvas.bind_class('scroll_frame_bg', '<MouseWheel>',
                               lambda event: self.canvas.yview_scroll(-int(event.delta / 60), "units"))
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
        if new_height >= self.winfo_height():
            height = new_height
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
                        self.update_idletasks()
                        # Adjusting height
                        if self.tree_row == 0:
                            height = 340
                        else:
                            height = new_item.winfo_height() * (self.tree_row + 1)
                        self.update_size_new_item(height)
                        # updating row, col numbers
                        self.tree_row, self.tree_col = self.update_row_column(self.tree_row,
                                                                              self.tree_col)
            else:
                pass
            client_store = None
        except NameError:
            return None

    @staticmethod
    def update_row_column(row, column):
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
        self.bind('<Delete>', self.delete_row)

    def item_select(self, event):
        tree_selection = list()
        for i in self.selection():
            tree_selection.append(self.item(i)['values'][0])
        global client_store
        client_store = tree_selection

    def get_tree_headings(self):
        for arg in self.args:
            self.heading(arg, text=str(arg))

    def delete_row(self, event):
        selected_items = self.selection()
        for item in selected_items:
            self.delete(item)


class CommandListTree(ttk.Treeview):
    def __init__(self, parent, *args):
        super().__init__(master=parent, columns=args, show='headings')
        self.args = args
        self.parent = parent
        self.get_tree_headings()
        tags = self.bindtags() + ("commands",)
        self.bindtags(tags)
        self.bind('<<TreeviewSelect>>', self.item_select)
        self.bind('<Delete>', self.delete_row)

    def item_select(self, event):
        tree_selection = list()
        for i in self.selection():
            tree_selection.append(self.item(i)['values'][0])
        global command_store
        command_store = tree_selection

    def get_tree_headings(self):
        for arg in self.args:
            self.heading(arg, text=str(arg))

    def delete_row(self, event):
        selected_items = self.selection()
        for item in selected_items:
            self.delete(item)


class TabBarTree(ttk.Treeview):
    def __init__(self, parent, *args):
        super().__init__(master=parent, columns=args, show='headings')
        self.args = args
        self.parent = parent
        self.get_tree_headings()
        self.bind('<ButtonRelease-1>', self.command_release)
        self.bind('<Delete>', self.delete_row)

    def get_tree_headings(self):
        for arg in self.args:
            self.heading(arg, text=str(arg))

    def command_release(self, event):
        global command_store
        start_x = self.winfo_pointerx() - self.winfo_rootx()
        start_y = self.winfo_pointery() - self.winfo_rooty()
        if command_store:
            if 0 <= start_x <= self.winfo_width() and 0 <= start_y <= self.winfo_height():
                # for index, _ in enumerate(command_store):
                #     self.insert(parent='', index=tk.END, values=(command_store[index]))
                item_index = 0
                while item_index < len(command_store):
                    print(command_store[item_index])
                    self.insert(parent='', index=tk.END, values=[(command_store[item_index])])
                    item_index += 1
                command_store = None
            else:
                command_store = None

    def delete_row(self, event):
        selected_items = self.selection()
        for item in selected_items:
            self.delete(item)


App('Glass Panel Control', (200, 200))
