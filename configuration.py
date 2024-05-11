import tkinter as tk
import ttkbootstrap as ttk
from add_button_dlg import CommandWindow, ClientWindow, NewTabWindow
from drag_and_drop import CommandDragManager, ClientDragManager
from Tree_Widgets import ClientListTree, CommandListTree, TabBarTree, ClientTabFrame, TabTreeMouseOver
from math import floor
import json


class ConfigurationManager(ttk.Toplevel):
    config_names = list()
    active_config_name = None
    configurations = None

    def __init__(self, configurations):
        super().__init__()
        self.title('Configuration')
        self.geometry("1340x600")
        self.resizable(True, True)
        ConfigurationManager.configurations = configurations

        ConfigurationManager.active_config_name = ConfigurationManager.configurations['active_config']
        active_config_data = ConfigurationManager.configurations['configurations'][
            ConfigurationManager.active_config_name]
        ConfigurationManager.config_names = list(ConfigurationManager.configurations['configurations'].keys())

        self.config_frame = Configuration.from_active_config(self,
                                                             active_config_data,
                                                             self.config_selected)

        # pack
        self.config_frame.pack(expand=True, fill='both')

        # Menu
        menu = WindowMenu()
        self.configure(menu=menu)

    def config_selected(self, config):
        selected_config = config.get()
        if selected_config == ConfigurationManager.active_config_name:
            return
        else:
            # Setting new active config
            ConfigurationManager.active_config_name = selected_config
            # Getting Config Data
            selected_config_data = ConfigurationManager.configurations['configurations'][selected_config]
            # Destroying old config window
            self.config_frame.destroy()
            # Loading Configuration with new configuration data
            self.config_frame = Configuration.from_active_config(self,
                                                                 selected_config_data,
                                                                 self.config_selected)
            # Repacking Configuration
            self.config_frame.pack(expand=True, fill='both')

    @classmethod
    def from_json(cls, json_name):
        try:
            with open(json_name) as f:
                cls(json.load(f))
        except FileNotFoundError as e:
            print(e)
        except json.decoder.JSONDecodeError as e:
            print(e)


class Configuration(ttk.Frame):
    def __init__(self,
                 parent,
                 clients_dictionary,
                 commands_dictionary,
                 tabs_info,
                 m_config_selected):
        super().__init__(master=parent)
        self.tab_trees_dict = None
        self.tab_id = None

        # self.minsize(400, 300)
        self.clients_dictionary = clients_dictionary
        self.commands_dictionary = commands_dictionary
        self.tabs_info = tabs_info
        self.tabs_list = list()
        self.active_scroll_frame = None
        self.active_tab_tree_frame = None
        self.client_tab_frame_list = None
        self.m_config_selected = m_config_selected


        self.tab_frame = ttk.Frame(self)
        self.side_bar_frame = ttk.Frame(self)

        self.rowconfigure(1, weight=10)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Side Bar Configuration
        self.side_bar_frame.rowconfigure(0, weight=1)
        self.side_bar_frame.rowconfigure(1, weight=1)
        self.side_bar_frame.columnconfigure(0, weight=1, uniform='a')

        self.client_frame = ttk.Frame(self.side_bar_frame)
        self.client_frame.columnconfigure(0, weight=1, uniform='a')
        self.client_frame.columnconfigure(1, weight=1, uniform='a')
        self.client_frame.grid(row=0, column=0, sticky='nsew', pady=(10, 10))

        self.clients_tree = ClientListTree.from_json(self.client_frame,
                                                     self.clients_dictionary,
                                                     ["Clients"])

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
        self.clients_tree.grid(row=0, columnspan=2, sticky='nsew')
        self.new_client_button.grid(row=1, column=0, padx=5, pady=5)
        self.delete_client_button.grid(row=1, column=1, padx=5, pady=5)

        self.command_frame = ttk.Frame(self.side_bar_frame)
        self.command_frame.columnconfigure(0, weight=1, uniform='a')
        self.command_frame.columnconfigure(1, weight=1, uniform='a')
        self.command_frame.grid(row=1, column=0, sticky='nsew', pady=(10, 10))

        # Command List Tree
        self.commands_tree = CommandListTree.from_json(self.command_frame,
                                                       self.commands_dictionary,
                                                       ["Commands"])

        # Making command tree items draggable.
        command_dnd = CommandDragManager(self.commands_tree)
        command_dnd.add_dragable(self.commands_tree)

        self.new_command_button = ttk.Button(self.command_frame,
                                             text="New",
                                             command=lambda: CommandWindow(self.commands_tree.command_dictionary,
                                                                           self.insert_command,
                                                                           self.insert_another_command))

        # Delete Command Button
        self.delete_command_button = ttk.Button(self.command_frame,
                                                text="Delete",
                                                command=lambda: self.delete_row(self.commands_tree))

        # Adding command section to sidebar.
        self.commands_tree.grid(row=0, columnspan=2, sticky='nsew')
        self.new_command_button.grid(row=1, column=0, padx=5, pady=5)
        self.delete_command_button.grid(row=1, column=1, padx=5, pady=5)

        self.save_button = ttk.Button(self.side_bar_frame, text='Save', command=self.write_json)
        self.save_button.grid(row=2)

        # Tab Frame configuration
        self.tab_frame.rowconfigure(0, weight=1)
        self.tab_frame.rowconfigure(1, weight=10)
        self.tab_frame.rowconfigure(2, weight=1)
        self.tab_frame.columnconfigure(0, weight=5, uniform='a')
        self.tab_frame.columnconfigure(1, weight=5, uniform='a')
        self.tab_frame.columnconfigure(2, weight=5, uniform='a')

        self.tabs_nb = ttk.Notebook(self.tab_frame, width=1080)

        tab_style = ttk.Style()
        tab_style.configure('TNotebook', tabposition='new')
        # tab_style.configure('TNotebook', tabposition='en')

        self.tabs_nb.bind("<<NotebookTabChanged>>", self.on_tab_selected)

        # Tree Control Buttons
        self.move_left_button = ttk.Button(self.tab_frame,
                                           text="\u2B9C",
                                           command=lambda: self.move_left(),
                                           bootstyle="outline")

        self.delete_button = ttk.Button(self.tab_frame,
                                        text="\U0001F5D1",
                                        command=lambda: self.delete_client(),
                                        bootstyle="outline")

        self.move_right_button = ttk.Button(self.tab_frame,
                                            text="\u2B9E",
                                            command=lambda: self.move_right(),
                                            bootstyle="outline")

        # New and Delete Buttons for tabs.
        self.tabs_nb.grid(row=1, column=0, columnspan=3, sticky='nsew')
        self.move_left_button.grid(row=2, column=0, sticky='new')
        self.delete_button.grid(row=2, column=1, sticky='new')
        self.move_right_button.grid(row=2, column=2, sticky='new')

        # Packing Tab Frame Widgets
        self.button_frame = ttk.Frame(self.tab_frame)
        self.button_frame.columnconfigure(0, weight=1, uniform='a')
        self.button_frame.columnconfigure(1, weight=1, uniform='a')
        self.button_frame.rowconfigure(0, weight=1)

        # Binding for tree select
        self.tree_select = self.move_left_button.bindtags() + ("tree_select",)
        self.move_left_button.bindtags(self.tree_select)
        self.tree_select = self.delete_button.bindtags() + ("tree_select",)
        self.delete_button.bindtags(self.tree_select)
        self.tree_select = self.move_right_button.bindtags() + ("tree_select",)
        self.move_right_button.bindtags(self.tree_select)

        # Tab buttons
        # self.new_tab_button_frame = ttk.Frame(self.button_frame)
        self.new_tab_button = ttk.Button(self.button_frame,
                                         text="New Tab",
                                         command=lambda: NewTabWindow(self.insert_tab, self.insert_another_tab))

        # self.delete_tab_button_frame = ttk.Frame(self.button_frame)
        self.delete_tab_button = ttk.Button(self.button_frame,
                                            text="Delete Tab",
                                            command=self.delete_tab)

        self.new_tab_button.pack(expand=True, fill='both', side='right')
        self.delete_tab_button.pack(expand=True, fill='both', side='right')

        self.button_frame.grid(row=0, column=2, sticky='se')

        # Configuration Dropdown
        drop_down_frame = ttk.Frame(self.tab_frame)
        # Configuration Combobox.
        config_names = ConfigurationManager.config_names
        c = ttk.StringVar(value=ConfigurationManager.active_config_name)
        combo = ttk.Combobox(drop_down_frame, textvariable=c)
        combo['values'] = config_names
        combo['state'] = 'readonly'
        combo.pack(expand=True, fill='x', side='right')
        combo.bind('<<ComboboxSelected>>', lambda event: self.m_config_selected(c))

        new_config = ttk.Button(drop_down_frame, text="+")
        delete_config = ttk.Button(drop_down_frame, text=u"\U0001F5D1")
        delete_config.pack(side='left')
        new_config.pack(side='left')

        # pack combo frame:
        drop_down_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')

        # inserting frames on to configuration frame.
        self.tab_frame.grid(row=1, column=1, sticky='nsew', padx=(5, 5))
        self.side_bar_frame.grid(row=0, column=0, sticky='new', rowspan=3, padx=(5, 5))

        # Creating Tabs. Class method appends to tabs to list and returns list of tab objects
        self.tabs_list = ScrollFrame.from_tabs_info(self.tabs_nb, self.tabs_info)
        for tab in self.tabs_list:
            self.tabs_nb.add(tab, text=f'{tab.tab_name}')

        self.buttons_list = [self.move_left_button, self.delete_button, self.move_right_button]
        self.bind_class("tree_select", '<Button-1>', self.enable_nav_buttons)

    def write_json(self):
        with open('commandconfig.json', 'w') as f:
            json.dump(ConfigurationManager.configurations, f, indent=2)

    @classmethod
    def from_active_config(cls, parent, active_config_data, m_config_selected):
        try:
            return cls(parent,
                       active_config_data['clients'],
                       active_config_data['commands'],
                       active_config_data['tabs_info'],
                       m_config_selected)
        except KeyError as e:
            print(f'Key {e} is incorrect.')

    def enable_nav_buttons(self, event):
        x, y = event.widget.winfo_pointerxy()
        target = event.widget.winfo_containing(x, y)
        master_target = event.widget.winfo_containing(x, y).master
        # if master_target in self.client_tab_frame_list:
        if master_target in self.active_scroll_frame.client_tab_frame_list:
            self.active_tab_tree_frame = master_target
        elif target in self.buttons_list:
            pass
        else:
            self.active_tab_tree_frame = None

    def on_start_hover(self, event):
        if self.active_tab_tree_frame:
            self.move_left_button.configure(state='enabled')

    def move_right(self):
        if self.active_tab_tree_frame:
            self.shift_index_up()
            self.re_sort(self.client_tab_frame_list)
            self.unpack_client_frame()
            for client_tab_frame in self.client_tab_frame_list:
                row, column = self.get_row_and_column(client_tab_frame.index)
                self.repack_client_frame(client_tab_frame, row, column)

    def move_left(self):
        if self.active_tab_tree_frame:
            self.shift_index_down()
            self.re_sort(self.client_tab_frame_list)
            self.unpack_client_frame()
            for client_tab_frame in self.client_tab_frame_list:
                row, column = self.get_row_and_column(client_tab_frame.index)
                self.repack_client_frame(client_tab_frame, row, column)

    def delete_client(self):
        if self.active_tab_tree_frame:
            self.unpack_client_frame()
            for index, client_tab_frame in enumerate(self.active_scroll_frame.client_tab_frame_list):
                if client_tab_frame.index == self.active_tab_tree_frame.index:
                    del self.active_scroll_frame.client_tab_frame_list[index]
                    del self.tab_trees_dict[str(index + 1)]

            for client_tab_frame in self.active_scroll_frame.client_tab_frame_list:
                if client_tab_frame.index > self.active_tab_tree_frame.index:
                    client_tab_frame.index -= 1
            print(self.active_tab_tree_frame.index)
            # Re-indexing trees to not have gaps in numbering by looping through dictionary and initializing
            # a new dictionary with the correct numbering as the key. Then updating with temp dictionary.
            temp_dict = dict()
            for index, (key, value) in enumerate(self.tab_trees_dict.items()):
                temp_dict[str(index + 1)] = self.tab_trees_dict[key]
            self.tab_trees_dict.clear()
            self.tab_trees_dict.update(temp_dict)
            self.re_sort(self.client_tab_frame_list)
            for client_tab_frame in self.client_tab_frame_list:
                row, column = self.get_row_and_column(client_tab_frame.index)
                self.repack_client_frame(client_tab_frame, row, column)

            # drop tab tree index by one so next client dragged and dropped doesn't skip a number
            self.active_scroll_frame.reduce_tab_tree_index()
            # Get index of last frame as that is what determines the scroll area. Or I could count items in frame list.
            last_frame = len(self.client_tab_frame_list) - 1
            # print(last_frame)
            last_row, last_column = self.get_row_and_column(last_frame)
            scroll_frame_height = (self.active_tab_tree_frame.winfo_height() * last_row
                                   + (last_row * 10))  # Row multiplied by pad (5 top + 5 bottom)
            self.active_scroll_frame.update_scroll_area(scroll_frame_height)
            # Setting active_tab_tree_frame to none.
            self.active_tab_tree_frame = None

    def shift_index_up(self):
        try:
            # Making sure frame is not last.
            if self.active_tab_tree_frame.index < self.client_tab_frame_list[-1].index:
                for client_tab_frame in self.client_tab_frame_list:
                    if client_tab_frame.index == (self.active_tab_tree_frame.index + 1):  # One above
                        client_tab_frame.index -= 1
                self.active_tab_tree_frame.index += 1
        except IndexError or AttributeError:
            pass

    def shift_index_down(self):
        for client_tab_frame in self.client_tab_frame_list:
            if client_tab_frame.index == (self.active_tab_tree_frame.index - 1):  # One below
                client_tab_frame.index += 1
        self.active_tab_tree_frame.index -= 1
        self.active_tab_tree_frame.index = max(self.active_tab_tree_frame.index, 0)  # Limit to 0

    def unpack_client_frame(self):
        for frame in self.client_tab_frame_list:
            frame.grid_forget()

    @staticmethod
    def re_sort(client_tab_frame_list):
        return client_tab_frame_list.sort(key=lambda x: x.index)

    @staticmethod
    def repack_client_frame(client_tab_frame, row, column):
        tree_pad_x = 5
        tree_pad_y = 5
        client_tab_frame.grid(row=row, column=column,
                              padx=tree_pad_x,
                              pady=tree_pad_y,
                              sticky="nsew")

    @staticmethod
    def get_row_and_column(client_frame_index):
        row = (floor(client_frame_index / 5)) + 1
        column = (client_frame_index % 5) + 1
        return row, column

    def on_tab_selected(self, event):
        if self.tabs_list:
            selected_tab = event.widget.select()
            self.tab_id = self.tabs_nb.index(selected_tab)
            scroll_frame = self.tabs_list[self.tab_id]
            self.active_scroll_frame = scroll_frame
            # Get the dictionary containing tree info for the selected tab.
            self.tab_trees_dict = self.tabs_info[self.active_scroll_frame.tab_name]
            client_dnd = ClientDragManager(scroll_frame, self.tab_trees_dict)
            client_dnd.add_dragable(self.clients_tree)
            self.client_tab_frame_list = scroll_frame.client_tab_frame_list

    def insert_tab(self, window_instance, new_tab):
        if new_tab:
            tab = ScrollFrame(self.tabs_nb,
                              self.clients_dictionary)
            self.tabs_list.append(tab)
            self.tabs_nb.add(tab, text=f'{new_tab}')
        window_instance.destroy()

    def insert_another_tab(self, new_tab):
        if new_tab:
            tab = ScrollFrame(self.tabs_nb,
                              self.clients_tree)
            self.tabs_list.append(tab)
            self.tabs_nb.add(tab, text=f'{new_tab}')

    def delete_tab(self):
        for item in self.tabs_nb.winfo_children():
            if str(item) == self.tabs_nb.select():
                item.pack_forget()  # To prevent scroll errors.
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
                 tab_name,
                 tab_data=None):
        super().__init__(master=parent)

        # widget data
        self.list_height = 0
        self.tab_name = tab_name
        self.tab_data = tab_data
        self.client_tab_frame_list = list()
        self.client_tab_tree_index = 0
        self.tab_tree_list = list()
        # canvas
        self.canvas = tk.Canvas(self)
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

        # Creating tree frame:
        client_tab_frame_list = ClientTabFrame.from_tab_info(self.scroll_frame, self.tab_data)
        self.tab_tree_list = TabBarTree.from_tab_data(client_tab_frame_list, self.tab_data)
        tt_mouse_over_list = TabTreeMouseOver.from_client_tab_frame_list(client_tab_frame_list, self.tab_tree_list)

        # packing trees and mouse_over frame to client tab_frame
        for tree, mouse_over_frame in zip(self.tab_tree_list, tt_mouse_over_list):
            tree.grid(sticky='nsew')

        # put client_tab_frame on the scroll frame
        for tab_frame in client_tab_frame_list:
            self.grid_tab_frame(tab_frame)

        # events
        self.canvas.bind_class('scroll_frame_widgets', '<MouseWheel>',
                               lambda event: self.canvas.yview_scroll(-int(event.delta / 60), "units"))
        self.bind('<Configure>', self.update_scroll_area_resize_event)

    def update_scroll_area_resize_event(self, event):
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
        self.canvas_configure(height)

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
        self.list_height = height
        self.canvas_configure(height)

    def canvas_configure(self, height):
        self.canvas.configure(scrollregion=(0, 0, self.winfo_width(), height))

    def create_canvas_window(self, height):
        self.canvas.create_window(
            (0, 0),
            window=self.scroll_frame,
            anchor='nw',
            width=self.winfo_width(),
            height=height)

    @classmethod
    def from_tabs_info(cls,
                       tabs_nb,
                       tabs_info):
        tabs_data_list = list()
        for tab_name, tab_data in tabs_info.items():
            tabs_data_list.append(cls(tabs_nb, tab_name, tab_data))
        return tabs_data_list

    def grid_tab_frame(self, tab_frame):
        client_tab_frame_row, client_tab_frame_col = self.assign_row_column(self.client_tab_tree_index)
        self.scroll_frame.rowconfigure(client_tab_frame_row)
        tab_frame.grid(row=client_tab_frame_row, column=client_tab_frame_col,
                       padx=5,
                       pady=5,
                       sticky="nsew")
        self.scroll_frame.grid_propagate(False)
        self.scroll_frame.update_idletasks()
        scroll_frame_height = (tab_frame.winfo_height() * client_tab_frame_row
                               + ((client_tab_frame_row * 2) * 5))
        self.update_scroll_area(scroll_frame_height)
        self.client_tab_frame_list.append(tab_frame)
        self.client_tab_tree_index += 1


    @staticmethod
    def assign_row_column(tab_frame_index):
        """
        ScrollFrame needs to be in charge of managing its trees.
        :param tab_frame_index: ScrollFrame attribute, Frame that tree and buttons are packed into.
        :return: row and column for frame that contains tree and buttons,
        """
        # row = (floor(int(tab_frame.index) / 5)) + 1
        # column = (int(tab_frame.index) % 5) + 1
        row = (floor(tab_frame_index / 5)) + 1
        column = (tab_frame_index % 5) + 1
        return row, column

    def reduce_tab_tree_index(self):
        self.client_tab_tree_index -= 1

    # def pack_trees(self, client_name, tab_commands, clients_dictionary):
    #     # todo simplify code below. client_tab_tree and TabTreeMouseOver can called from ClientTabFrame Class.
    #     client_tab_frame = ClientTabFrame(self.scroll_frame, self.client_tab_tree_index)
    #     client_tab_tree = TabBarTree.from_json(client_tab_frame,
    #                                            clients_dictionary,
    #                                            client_name,
    #                                            tab_commands)
    #     client_tab_frame_row, client_tab_frame_col = self.assign_row_column(client_tab_tree, self.client_tab_tree_index)
    #     self.scroll_frame.rowconfigure(client_tab_frame_row)
    #     client_tab_tree.grid(row=0, sticky='nsew')
    #
    #     TabTreeMouseOver(client_tab_frame,
    #                      client_tab_tree)
    #
    #     tree_pad_x = 5
    #     tree_pad_y = 5
    #
    #     client_tab_frame.grid(row=client_tab_frame_row, column=client_tab_frame_col,
    #                           padx=tree_pad_x,
    #                           pady=tree_pad_y,
    #                           sticky="nsew")
    #
    #     self.scroll_frame.grid_propagate(False)
    #     self.scroll_frame.update_idletasks()
    #     scroll_frame_height = (client_tab_frame.winfo_height() * client_tab_frame_row
    #                            + ((client_tab_frame_row * 2) * tree_pad_y))
    #     self.update_scroll_area(scroll_frame_height)
    #     self.client_tab_frame_list.append(client_tab_frame)
    #     self.client_tab_tree_index += 1


class WindowMenu(ttk.Menu):
    def __init__(self):
        super().__init__()
        # sub menu
        file_menu = ttk.Menu(self, tearoff=False)
        file_menu.add_command(label='New', command=lambda: print('New file'))
        file_menu.add_command(label='Open', command=lambda: print('Open file'))
        self.add_cascade(label='File', menu=file_menu)

        # another sub menu
        help_menu = ttk.Menu(self, tearoff=False)
        help_menu.add_command(label='Help entry', command=lambda: print("test"))
        self.add_cascade(label='Help', menu=help_menu)
