import tkinter as tk
from tkinter import ttk
from command_window import CommandWindow
from client_window import ClientWindow
from drag_and_drop import (CommandDragManager,
                           ClientDragManager)
from Tree_Widgets import (ClientListTree,
                          CommandListTree,
                          TabBarTree,
                          ClientTabFrame,
                          TabTreeMouseOver)
from math import floor


class Configuration(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Configuration')
        self.geometry("1340x600")
        self.resizable(False, False)
        # self.minsize(400, 300)
        self.tab_tree_list = dict()

        self.tab_frame = ttk.Frame(self, relief=tk.GROOVE)
        self.side_bar_frame = ttk.Frame(self, relief=tk.GROOVE)
        self.top_bar_frame = ttk.Frame(self, relief=tk.GROOVE)
        self.bot_bar_frame = ttk.Frame(self, relief=tk.GROOVE)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

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

        clients_dictionary = {'VB1': ('199.199.199.01', 'MAC1'),
                   'VB2': ('199.199.199.02', 'MAC2'),
                   'VB3': ('199.199.199.03', 'MAC3'),
                   'VB4': ('199.199.199.01', 'MAC4')}

        self.clients_tree = ClientListTree(self.client_frame, clients_dictionary, ["Clients"])

        # New Client Button
        self.new_client_button = ttk.Button(self.client_frame,
                                            text="New",
                                            command=lambda: ClientWindow(self.clients_tree.client_dictionary,
                                                                         self.insert_client,
                                                                         self.insert_another_client))

        # Delete Command Button
        self.delete_client_button = ttk.Button(self.client_frame,
                                               text="Delete",
                                               command=lambda: self.delete_row(self.clients_tree))

        # Adding command section to sidebar.
        self.clients_tree.grid(row=0, columnspan=2)
        self.new_client_button.grid(row=1, column=0, padx=5, pady=5)
        self.delete_client_button.grid(row=1, column=1, padx=5, pady=5)

        self.bot_side_bar_frame = ttk.Frame(self.side_bar_frame)
        self.bot_side_bar_frame.grid(row=1, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.command_frame = ttk.Frame(self.bot_side_bar_frame)
        self.command_frame.columnconfigure(0, weight=1, uniform='a')
        self.command_frame.columnconfigure(1, weight=1, uniform='a')
        self.command_frame.pack(fill='both', expand=True)

        commands_dictionary = {'Load Graphic 1': 'cd dsfasdf',
                    'Load Graphic 2': 'dfgbfdsxhb',
                    'Load Graphic 3': '123',
                    'Load Graphic 4': '345',
                    'Load Graphic 5': '567'}

        # Command List Tree
        self.commands_tree = CommandListTree(self.command_frame, commands_dictionary, ["Commands"])
        self.new_command_button = ttk.Button(self.command_frame,
                                             text="New",
                                             command=lambda: CommandWindow(self.commands_tree.command_dictionary,
                                                                           self.insert_command,
                                                                           self.insert_another_command,))

        # Delete Command Button
        self.delete_command_button = ttk.Button(self.command_frame,
                                                text="Delete",
                                                command=lambda: self.delete_row(self.commands_tree))

        # Adding command section to sidebar.
        self.commands_tree.grid(row=0, columnspan=2)
        self.new_command_button.grid(row=1, column=0, padx=5, pady=5)
        self.delete_command_button.grid(row=1, column=1, padx=5, pady=5)

        # Tab Frame configuration
        # self.tabs = ttk.Notebook(self.tab_frame, width=1080, height=self.tab_frame.winfo_height())
        self.tabs = ttk.Notebook(self.tab_frame, width=1080)
        self.tab_frame.rowconfigure(0, weight=1)
        self.tab_frame.columnconfigure(0, weight=1)

        # Initializing Tabs:

        tab1_clients = ["VB1", "VB2", "VB3"]
        tab1_commands = [["Load Graphic 1", "Load Graphic 2", "Load Graphic 3"],
                         [None],
                         [None]]

        # tab1_clients = ["Vb"]
        # tab1_commands = [[None]]

        # Creating Tab 1
        self.tab1 = tk.Frame(self.tabs)
        self.tab1_scroll = ScrollFrame(self.tab1,
                                       10,
                                       1,
                                       self.clients_tree,
                                       self.commands_tree,
                                       clients_dictionary,
                                       commands_dictionary,
                                       tab1_clients,
                                       tab1_commands)
        self.tab1_scroll.pack(expand=True, fill='both')

        # Creating Tab 2
        # self.tab2 = tk.Frame(self.tabs)
        # self.tab2_scroll = ScrollFrame(self.tab2,
        #                                10,
        #                                1,
        #                                self.clients_tree,
        #                                self.commands_tree)
        #
        # self.tab2_scroll.pack(expand=True, fill='both')

        # Adding tabs to Tab Notebook Frame
        self.tabs.add(self.tab1, text='First Tab')
        # self.tabs.add(self.tab2, text='Second Tab')

        self.tabs.grid(sticky='nsew')

        # Top Bar Configuration
        self.top_label = ttk.Label(self.top_bar_frame, text="Top Bar")
        self.top_label.pack(expand=True)

        # Bottom Bar Configuration
        self.bot_label = ttk.Label(self.bot_bar_frame, text="Bottom Bar")
        self.bot_label.pack(expand=True)

        self.tab_frame.grid(row=1, column=1, sticky='nsew', padx=(5, 5), pady=(10, 10))
        self.side_bar_frame.grid(row=0, column=0, sticky='nsew', rowspan=3, padx=(5, 5), pady=(10, 10))
        self.top_bar_frame.grid(row=0, column=1, sticky='nsew', padx=(5, 5), pady=(10, 10))
        self.bot_bar_frame.grid(row=2, column=1, sticky='nsew', padx=(5, 5), pady=(10, 10))

        style = ttk.Style(self)
        style.theme_use('clam')

    def insert_client(self, window_instance, new_client):
        if new_client:
            self.clients_tree.insert(parent='', index=tk.END, values=[new_client])
        window_instance.destroy()

    def insert_another_client(self, new_client):
        if new_client:
            self.clients_tree.insert(parent='', index=tk.END, values=[new_client])

    def insert_command(self, window_instance, new_command):
        if new_command:
            self.commands_tree.insert(parent='', index=tk.END, values=[new_command])
        window_instance.destroy()

    def insert_another_command(self, new_command):
        if new_command:
            self.commands_tree.insert(parent='', index=tk.END, values=[new_command])

    @staticmethod
    def delete_row(tree):
        tree.delete_row()


class ScrollFrame(ttk.Frame):
    def __init__(self, parent,
                 item_height,
                 tree_index,
                 clients_tree,
                 commands_tree,
                 clients_dictionary,
                 commands_dictionary,
                 tab_clients,
                 tab_commands):

        super().__init__(master=parent)

        # widget data
        self.tree_index = tree_index
        self.item_height = item_height
        self.list_height = (self.tree_index * item_height)  # Five items per row
        self.clients_tree = clients_tree
        self.commands_tree = commands_tree
        self.clients_dictionary = clients_dictionary
        self.commands_dictionary = commands_dictionary
        self.tab_clients = tab_clients
        self.tab_commands = tab_commands

        self.client_tab_tree_index = 0
        self.client_tab_frame_list = list()

        # canvas
        self.canvas = tk.Canvas(self, background='red')
        self.canvas.pack(expand=True, fill='both')

        # display frame
        self.scroll_frame = ttk.Frame(self)

        # Adding new tag for frame to allow scroll on TabTree and background.
        self.new_tags = self.scroll_frame.bindtags() + ("scroll_frame_widgets",)
        self.scroll_frame.bindtags(self.new_tags)

        # scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')

        # events
        self.canvas.bind_class('scroll_frame_widgets', '<MouseWheel>',
                               lambda event: self.canvas.yview_scroll(-int(event.delta / 60), "units"))
        self.bind('<Configure>', self.update_scroll_area_resize_event)

        self.initialize_tab_trees()

        client_dnd = ClientDragManager(self.scroll_frame,
                                       self.pack_trees,
                                       self.clients_dictionary,
                                       self.commands_dictionary)

        client_dnd.add_dragable(self.clients_tree)

        command_dnd = CommandDragManager(self.commands_tree)
        command_dnd.add_dragable(self.commands_tree)

    def update_scroll_area_resize_event(self, event):
        """Resizing Currently Disabled"""
        if self.list_height >= self.winfo_height():
            height = self.list_height
            self.canvas.bind_class('scroll_frame_widgets', '<MouseWheel>',
                                   lambda event: self.canvas.yview_scroll(-int(event.delta / 60), "units"))
            self.scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
        else:
            height = self.winfo_height()
            self.canvas.unbind_all('<MouseWheel>')
            self.scrollbar.place_forget()

        self.canvas.create_window(
            (0, 0),
            window=self.scroll_frame,
            anchor='nw',
            width=self.winfo_width(),
            height=height)

    def update_scroll_area(self, new_height):
        if new_height >= self.winfo_height():
            height = new_height
            self.canvas.bind_class('scroll_frame_widgets', '<MouseWheel>',
                                   lambda event: self.canvas.yview_scroll(-int(event.delta / 60), "units"))
            self.scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
        else:
            height = self.winfo_height()
            self.canvas.unbind_all('<MouseWheel>')
            self.scrollbar.place_forget()

        self.canvas.create_window(
            (0, 0),
            window=self.scroll_frame,
            anchor='nw',
            width=self.winfo_width(),
            height=height)

        self.canvas.configure(scrollregion=(0, 0, self.winfo_width(), height))
        self.list_height = height
        # print("Size Updated!")

    def initialize_tab_trees(self):
        for index, client_name in enumerate(self.tab_clients):
            # if self.tab_commands[index]:
            if self.tab_clients[index]:
                self.pack_trees([client_name, ],
                                self.clients_dictionary,
                                self.commands_dictionary,
                                self.tab_commands[index])

    def pack_trees(self, client_name, clients_dictionary, commands_dictionary, command_names=None):
        client_tab_frame = ClientTabFrame(self.scroll_frame, self.client_tab_tree_index)
        client_tab_tree = TabBarTree(client_tab_frame,
                                     self.client_tab_tree_index,
                                     client_name,
                                     command_names,
                                     clients_dictionary,
                                     commands_dictionary)
        client_tab_frame_row, client_tab_frame_col = self.assign_row_column(client_tab_tree, self.client_tab_tree_index)
        self.scroll_frame.rowconfigure(client_tab_frame_row, minsize=260)
        client_tab_tree.pack(expand=False, fill='both')

        TabTreeMouseOver(client_tab_frame,
                         self.client_tab_frame_list,
                         client_tab_tree,
                         self.reduce_tab_tree_index,
                         self.update_scroll_area)

        tree_pad_x = 5
        tree_pad_y = 0

        client_tab_frame.grid(row=client_tab_frame_row, column=client_tab_frame_col,
                              padx=tree_pad_x,
                              pady=tree_pad_y,
                              sticky="nsew")

        self.scroll_frame.grid_propagate(False)
        self.scroll_frame.update_idletasks()
        scroll_frame_height = (client_tab_frame.winfo_height() * client_tab_frame_row
                               + ((client_tab_frame_row * 2) * tree_pad_y))
        self.update_scroll_area(scroll_frame_height)
        self.client_tab_frame_list.append(client_tab_frame)
        self.client_tab_tree_index += 1

    @staticmethod
    def assign_row_column(client_tab_frame, client_tab_frame_index):
        client_tab_frame.row = (floor(client_tab_frame_index / 5)) + 1
        client_tab_frame.column = (client_tab_frame_index % 5) + 1
        return client_tab_frame.row, client_tab_frame.column

    def reduce_tab_tree_index(self):
        self.client_tab_tree_index -= 1
