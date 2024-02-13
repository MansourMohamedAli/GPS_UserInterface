import tkinter as tk
from tkinter import ttk
from command_window import CommandWindow
from client_window import ClientWindow
from drag_and_drop import (CommandDragManager,
                           ClientDragManager)
from Tree_Widgets import (ClientListTree,
                          CommandListTree)


class Configuration(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Configuration')
        self.geometry("1340x600")
        self.resizable(False, False)
        # seZlf.minsize(400, 300)

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

        self.clients_tree = ClientListTree(self.client_frame, "Clients")
        i = 0
        while i < 15:
            self.clients_tree.insert(parent='', index=i, values=[f"VB{i + 1}"])
            i += 1

        # self.clients_tree.insert(parent='', index=0, values=["VB1"])
        # self.clients_tree.insert(parent='', index=1, values=["VB2"])
        # self.clients_tree.insert(parent='', index=2, values=["VB3"])

        # New Command Button
        self.new_client_button = ttk.Button(self.client_frame,
                                            text="New",
                                            command=lambda: ClientWindow(self.insert_client,
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

        # Command List Tree
        self.commands_tree = CommandListTree(self.command_frame, "Commands")

        i = 0
        while i < 15:
            self.commands_tree.insert(parent='', index=i, values=[f"Load VB{i + 1}"])
            i += 1

        # self.commands_tree.insert(parent='', index=0, values=["Load VB1"])
        # self.commands_tree.insert(parent='', index=1, values=["Load VB2"])
        # self.commands_tree.insert(parent='', index=2, values=["Load VB3"])

        self.new_command_button = ttk.Button(self.command_frame,
                                             text="New",
                                             command=lambda: CommandWindow(self.insert_command,
                                                                           self.insert_another_command))

        # Delete Command Button
        self.delete_command_button = ttk.Button(self.command_frame,
                                                text="Delete",
                                                command=lambda: self.delete_row(self.commands_tree))

        # Adding command section to sidebar.
        self.commands_tree.grid(row=0, columnspan=2)
        self.new_command_button.grid(row=1, column=0, padx=5, pady=5)
        self.delete_command_button.grid(row=1, column=1, padx=5, pady=5)

        # Tab Frame configuration
        self.tabs = ttk.Notebook(self.tab_frame, width=1080, height=self.tab_frame.winfo_height())
        self.tab_frame.rowconfigure(0, weight=1)
        self.tab_frame.columnconfigure(0, weight=1)

        # Creating Tab 1
        self.tab1 = tk.Frame(self.tabs)
        self.tab1_dict = dict()
        self.tab1_scroll = ScrollFrame(self.tab1, 10, 1, self.clients_tree, self.commands_tree)

        # Creating Tab 2
        self.tab2 = tk.Frame(self.tabs)

        # Adding tabs to Tab Notebook Frame
        self.tabs.add(self.tab1, text='First Tab')
        self.tabs.add(self.tab2, text='Second Tab')

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

    def insert_command(self, window_instance, new_command):
        if new_command:
            self.commands_tree.insert(parent='', index=tk.END, values=new_command)
        window_instance.destroy()

    def insert_another_command(self, new_command):
        if new_command:
            self.commands_tree.insert(parent='', index=tk.END, values=new_command)

    def insert_client(self, window_instance, new_client):
        if new_client:
            self.clients_tree.insert(parent='', index=tk.END, values=new_client)
        window_instance.destroy()

    def insert_another_client(self, new_client):
        if new_client:
            self.clients_tree.insert(parent='', index=tk.END, values=new_client)

    @staticmethod
    def delete_row(tree_list):
        selected_items = tree_list.selection()
        for item in selected_items:
            tree_list.delete(item)


class ScrollFrame(ttk.Frame):
    def __init__(self, parent, item_height, tree_index, clients_tree, commands_tree):
        super().__init__(master=parent)
        self.pack(expand=True, fill='both')

        # widget data
        self.tree_index = tree_index
        self.tree_row = 0
        self.tree_col = 0
        self.item_height = item_height
        self.list_height = (self.tree_index * item_height)  # Five items per row
        self.clients_tree = clients_tree
        self.commands_tree = commands_tree

        # canvas
        self.canvas = tk.Canvas(self, background='red')
        self.canvas.pack(expand=True, fill='both')

        # display frame
        self.frame = ttk.Frame(self)
        # self.frame.rowconfigure(self.tree_row, minsize=280)

        # Adding new tag for frame to allow scroll on TabTree and background.
        self.new_tags = self.frame.bindtags() + ("scroll_frame_widgets",)
        self.frame.bindtags(self.new_tags)

        # scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')

        # events
        self.canvas.bind_class('scroll_frame_widgets', '<MouseWheel>',
                               lambda event: self.canvas.yview_scroll(-int(event.delta / 60), "units"))
        self.bind('<Configure>', self.update_size_event)

        client_dnd = ClientDragManager(self.update_size_new_item, self.frame)
        client_dnd.add_dragable(self.clients_tree)

        command_dnd = CommandDragManager()
        command_dnd.add_dragable(self.commands_tree)

    def update_size_event(self, event):
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
            window=self.frame,
            anchor='nw',
            width=self.winfo_width(),
            height=height)

    def update_size_new_item(self, new_height):
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
            window=self.frame,
            anchor='nw',
            width=self.winfo_width(),
            height=height)

        self.canvas.configure(scrollregion=(0, 0, self.winfo_width(), height))
        self.list_height = height
