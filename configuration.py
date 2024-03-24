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
from new_tab_window import NewTabWindow
from math import floor


class Configuration(tk.Toplevel):
    def __init__(self, clients_dictionary, commands_dictionary, tab_clients_dictionary, tab_commands_dictionary):
        super().__init__()
        self.tab_id = None
        self.title('Configuration')
        self.geometry("1340x600")
        self.resizable(False, False)
        # self.minsize(400, 300)
        self.clients_dictionary = clients_dictionary
        self.commands_dictionary = commands_dictionary
        self.tab_clients_dictionary = tab_clients_dictionary
        self.tab_commands_dictionary = tab_commands_dictionary
        self.tabs_list = list()

        self.tab_frame = ttk.Frame(self, relief=tk.GROOVE)
        self.side_bar_frame = ttk.Frame(self, relief=tk.GROOVE)
        # self.top_bar_frame = TopFrame(self, relief=tk.GROOVE)
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

        self.clients_tree = ClientListTree.from_json(self.client_frame, self.clients_dictionary, ["Clients"])

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

        # Command List Tree
        self.commands_tree = CommandListTree.from_json(self.command_frame, self.commands_dictionary, ["Commands"])
        # Making command tree items draggable.
        command_dnd = CommandDragManager(self.commands_tree)
        command_dnd.add_dragable(self.commands_tree)

        self.new_command_button = ttk.Button(self.command_frame,
                                             text="New",
                                             command=lambda: CommandWindow(self.commands_tree.command_dictionary,
                                                                           self.insert_command,
                                                                           self.insert_another_command, ))

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
        self.tabs.bind("<<NotebookTabChanged>>", self.on_tab_selected)
        self.tab_frame.rowconfigure(0, weight=1)
        self.tab_frame.columnconfigure(0, weight=1)

        # Creating Tabs
        ScrollFrame.from_json(self.tabs,  # passing in notebook for method to instantiate tabs
                              self.clients_dictionary,
                              self.tab_clients_dictionary,
                              self.tab_commands_dictionary,  # list containing list of command name, command pairs.
                              self.tabs_list)

        self.tabs.grid(sticky='nsew', pady=(20, 0))

        self.button_frame = ttk.Frame(self.tab_frame)
        self.button_frame.columnconfigure(0, weight=1, uniform='a')
        self.button_frame.columnconfigure(1, weight=1, uniform='a')
        self.button_frame.rowconfigure(0, weight=1)

        self.new_button = ttk.Button(self.button_frame,
                                     text="New Tab",
                                     command=lambda: NewTabWindow(self.insert_tab, self.insert_another_tab))
        self.delete_button = ttk.Button(self.button_frame,
                                        text="Delete Tab",
                                        command=self.delete_tab)

        self.new_button.grid(row=0, column=0, sticky='s', padx=5, pady=5)
        self.delete_button.grid(row=0, column=1, sticky='s', padx=5, pady=5)

        self.button_frame.place(relx=0.8, rely=0.001)

        # Bottom Bar Configuration
        self.bot_label = ttk.Label(self.bot_bar_frame, text="Bottom Bar")
        self.bot_label.pack(expand=True)

        # self.tab_frame.grid(row=1, column=1, sticky='nsew', padx=(5, 5), pady=(10, 10))
        self.tab_frame.grid(row=1, column=1, sticky='nsew', padx=(5, 5))
        self.side_bar_frame.grid(row=0, column=0, sticky='nsew', rowspan=3, padx=(5, 5), pady=(10, 10))
        # self.top_bar_frame.grid(row=0, column=1, sticky='nsew', padx=(5, 5), pady=(10, 10))
        # self.top_bar_frame.grid(row=0, column=1, sticky='nsew', padx=(5, 5))
        self.bot_bar_frame.grid(row=2, column=1, sticky='nsew', padx=(5, 5), pady=(10, 10))

    @classmethod
    def from_json(cls, json_data):
        try:
            active_config = (json_data['active_config'])
            config = (json_data['configurations'][active_config])
            return cls(config['clients'], config['commands'], config['tab_clients'], config['tab_commands'])
        except KeyError as e:
            print(f'Key {e} is incorrect.')

    def on_tab_selected(self, event):
        if self.tabs_list:
            selected_tab = event.widget.select()
            self.tab_id = self.tabs.index(selected_tab)
            scroll_frame = self.tabs_list[self.tab_id]
            # todo Verify how class memory is managed. Is the old one being replaced?
            client_dnd = ClientDragManager(scroll_frame,
                                           self.clients_dictionary)
            client_dnd.add_dragable(self.clients_tree)

    def insert_tab(self, window_instance, new_tab):
        if new_tab:
            tab = ScrollFrame(self.tabs,
                              self.clients_dictionary)
            self.tabs_list.append(tab)
            self.tabs.add(tab, text=f'{new_tab}')
        window_instance.destroy()

    def insert_another_tab(self, new_tab):
        if new_tab:
            tab = ScrollFrame(self.tabs,
                              self.clients_tree)
            self.tabs_list.append(tab)
            self.tabs.add(tab, text=f'{new_tab}')

    def delete_tab(self):
        # Don't delete if there is only one tab
        if len(self.tabs.winfo_children()) > 1:
            for item in self.tabs.winfo_children():
                if str(item) == self.tabs.select():
                    item.destroy()
                    del self.tabs_list[self.tab_id]
                    return

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
    def __init__(self,
                 parent,
                 clients_dictionary):

        super().__init__(master=parent)

        # widget data
        self.clients_dictionary = clients_dictionary
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

    @classmethod
    def from_json(cls,
                  tabs,
                  clients_dictionary,
                  tab_clients,
                  tab_commands,
                  tab_list):

        for index, (tab_name, clients) in enumerate(tab_clients.items()):
            tab = cls(tabs, clients_dictionary)
            tab_list.append(tab)

            for i, client in enumerate(clients):
                cls.pack_trees(tab,
                               [client],
                               tab_commands[str(index + 1)][i],
                               clients_dictionary)

            tab.pack(expand=True, fill='both')
            tabs.add(tab, text=tab_name)

    def pack_trees(self, client_name, tab_commands, clients_dictionary):
        client_tab_frame = ClientTabFrame(self.scroll_frame, self.client_tab_tree_index)
        client_tab_tree = TabBarTree.from_json(client_tab_frame,
                                               clients_dictionary,
                                               client_name,
                                               tab_commands)
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


class BottomFrame(ttk.Frame):
    def __init__(self):
        super().__init__()

        # self.save_button = ttk.Button(self, text="Save", command=lambda: self.save_pressed())
        self.run_button = ttk.Button(self, text="Run", command=lambda: self.run_pressed())
        self.run_button.pack()

    def save_pressed(self):
        pass

    def run_pressed(self):
        pass
