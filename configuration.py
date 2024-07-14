import tkinter as tk
import ttkbootstrap as ttk
from add_button_dlg import CommandDlg, ClientDlg, NewTabWindow, RenameTabWindow, NewConfigDlg
from drag_and_drop import CommandDragManager, ClientDragManager
from Tree_Widgets import ClientListTree, CommandListTree, TabBarTree, ClientTabFrame, TabTreeMouseOver
from math import floor
import json


class ConfigurationManager(ttk.Toplevel):
    def __init__(self, configurations):
        super().__init__()

        self.title('Configuration')
        self.deleted_config = None
        x, y = self.get_dimensions()
        self.geometry(f'{int(x * 0.75)}x{int(y * 0.65)}')
        self.minsize(int(x * 0.65), int(y * 0.55))
        self.maxsize(int(x * 0.85), int(y * 0.75))
        self.resizable(True, True)
        self.configurations = configurations
        self.active_config_name = self.configurations['active_config']
        self.active_config_data = self.configurations['configurations'][
            self.active_config_name]
        self.config_names = list(self.configurations['configurations'].keys())

        self.config_frame = Configuration.from_active_config(self,
                                                             self.active_config_data,
                                                             self.write_json)

        # pack
        self.config_frame.pack(expand=True, fill='both', side="bottom")

        # combo frame
        self.combo_frame = ttk.Frame(self)

        # Configuration Dropdown
        self.drop_down_frame = ttk.Frame(self.combo_frame)
        # Configuration Combobox.
        c = ttk.StringVar(value=self.active_config_name)
        self.combo = ttk.Combobox(self.drop_down_frame, textvariable=c)
        self.combo['values'] = self.config_names
        self.combo['state'] = 'readonly'
        self.combo.pack(expand=True, fill='x', side='right')
        self.combo.bind('<<ComboboxSelected>>', lambda event: self.config_selected(c))

        self.new_config_button = ttk.Button(self.drop_down_frame,
                                            text="+",
                                            command=lambda: NewConfigDlg(self.insert_config))

        self.delete_config = ttk.Button(self.drop_down_frame,
                                        text=u"\U0001F5D1",
                                        command=self.delete_config)

        self.delete_config.pack(side='left')
        self.new_config_button.pack(side='left')
        # drop_down_frame.pack(expand=True, fill='both')
        self.drop_down_frame.pack(fill='x')

        # self.combo_frame.pack(expand=True, fill='both', side="top")
        self.combo_frame.pack(fill='x', side="top")

        # Menu
        menu = WindowMenu()
        self.configure(menu=menu)

        if __name__ == "__main__":
            self.main_loop()

    def main_loop(self):
        self.mainloop()

    def write_json(self):
        """
        Reset Active Config to first in list when saving in case Active Config is deleted.
        TODO: Handle this more elegantly with try/except in main.
        """
        if self.deleted_config == self.configurations['active_config']:
            self.configurations['active_config'] = self.combo['values'][0]
        with open('commandconfig.json', 'w') as f:
            json.dump(self.configurations, f, indent=2)

    def insert_config(self, window_instance, new_config):
        if new_config:
            self.combo['values'] = (*self.combo['values'], new_config)
            empty_config = dict()
            empty_config['clients'] = dict()
            empty_config['commands'] = dict()
            empty_config['tabs_info'] = dict()
            self.configurations['configurations'][new_config] = empty_config
        window_instance.destroy()

    def delete_config(self):
        temp_list = list(self.combo['values'])
        if len(temp_list) > 1:
            temp_list.remove(self.active_config_name)
            self.combo['values'] = tuple(temp_list)
            del self.configurations['configurations'][self.active_config_name]
            self.deleted_config = self.active_config_name
            c = ttk.StringVar(value=self.combo['values'][0])
            self.combo.set(self.combo['values'][0])
            self.config_selected(c)
            self.write_json()
        else:
            print('Last Config Frame')

    def config_selected(self, config):
        selected_config = config.get()
        if selected_config == self.active_config_name:
            return
        else:
            # Setting new active config
            self.active_config_name = selected_config
            # Getting Config Data
            selected_config_data = self.configurations['configurations'][selected_config]
            # Destroying old config window
            self.config_frame.destroy()
            # Loading Configuration with new configuration data
            self.config_frame = Configuration.from_active_config(self,
                                                                 selected_config_data,
                                                                 self.write_json)
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

    def get_dimensions(self):
        x = self.winfo_screenwidth()
        y = self.winfo_screenheight()
        return x, y


class Configuration(ttk.Frame):
    def __init__(self,
                 parent,
                 m_write_json,
                 clients_dictionary=None,
                 commands_dictionary=None,
                 tabs_info=None):
        super().__init__(master=parent)
        self.tab_id = None

        self.m_write_json = m_write_json

        if clients_dictionary is None:
            self.clients_dictionary = dict()
        else:
            self.clients_dictionary = clients_dictionary

        if commands_dictionary is None:
            self.commands_dictionary = dict()
        else:
            self.commands_dictionary = commands_dictionary

        if tabs_info is None:
            self.tabs_info = dict()
        else:
            self.tabs_info = tabs_info

        self.tabs_list = list()
        self.active_scroll_frame = None
        self.active_tab_tree_frame = None
        self.client_tab_frame_list = None
        self.tab_frame = ttk.Frame(self)
        self.side_bar_frame = ttk.Frame(self)

        self.rowconfigure(1, weight=10)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # Side Bar Configuration
        self.side_bar_frame.rowconfigure(0, weight=1)
        self.side_bar_frame.rowconfigure(1, weight=1)
        self.side_bar_frame.columnconfigure(0, weight=1, uniform='a')

        self.client_frame = ttk.Frame(self.side_bar_frame)
        self.client_frame.columnconfigure(0, weight=1, uniform='a')
        self.client_frame.columnconfigure(1, weight=1, uniform='a')
        self.client_frame.columnconfigure(2, weight=1, uniform='a')
        self.client_frame.grid(row=0, column=0, sticky='nsew', pady=(10, 10))

        self.clients_tree = ClientListTree.from_json(self.client_frame,
                                                     self.clients_dictionary,
                                                     ["Clients"])

        # New Client Button
        self.new_client_button = ttk.Button(self.client_frame,
                                            text="New",
                                            command=lambda: ClientDlg(self.clients_tree.client_dictionary,
                                                                      self.insert_client,
                                                                      self.insert_another_client))
        # Edit Client Button
        self.edit_client_button = ttk.Button(self.client_frame,
                                             text="Edit",
                                             command=self.edit_client)

        # Delete Command Button
        self.delete_client_button = ttk.Button(self.client_frame,
                                               text="Delete",
                                               command=lambda: self.delete_row(self.clients_tree))

        # Adding command section to sidebar.
        self.clients_tree.grid(row=0, columnspan=3, sticky='nsew')
        self.new_client_button.grid(row=1, column=0, padx=5, pady=5)
        self.edit_client_button.grid(row=1, column=1, padx=5, pady=5)
        self.delete_client_button.grid(row=1, column=2, padx=5, pady=5)

        self.command_frame = ttk.Frame(self.side_bar_frame)
        self.command_frame.columnconfigure(0, weight=1, uniform='a')
        self.command_frame.columnconfigure(1, weight=1, uniform='a')
        self.command_frame.columnconfigure(2, weight=1, uniform='a')
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
                                             command=lambda: CommandDlg(self.commands_tree.command_dictionary,
                                                                        self.insert_command,
                                                                        self.insert_another_command,
                                                                        "command"))

        # Edit Command Button
        self.edit_command_button = ttk.Button(self.command_frame,
                                              text="Edit",
                                              command=self.edit_command)

        # Delete Command Button
        self.delete_command_button = ttk.Button(self.command_frame,
                                                text="Delete",
                                                command=lambda: self.delete_row(self.commands_tree))

        # Adding command section to sidebar.
        self.commands_tree.grid(row=0, columnspan=3, sticky='nsew')
        self.new_command_button.grid(row=1, column=0, padx=5, pady=5)
        self.edit_command_button.grid(row=1, column=1, padx=5, pady=5)
        self.delete_command_button.grid(row=1, column=2, padx=5, pady=5)

        self.save_button = ttk.Button(self.side_bar_frame, text='Save', command=self.m_write_json)
        self.save_button.grid(row=2)

        # Tab Frame configuration
        self.tab_frame.rowconfigure(0, weight=1)
        self.tab_frame.rowconfigure(1, weight=10)
        self.tab_frame.rowconfigure(2, weight=1)
        self.tab_frame.columnconfigure(0, weight=5, uniform='a')
        self.tab_frame.columnconfigure(1, weight=5, uniform='a')
        self.tab_frame.columnconfigure(2, weight=5, uniform='a')
        self.tab_frame.columnconfigure(3, weight=5, uniform='a')

        self.tabs_nb = ttk.Notebook(self.tab_frame, width=1080)
        self.tabs_nb.bind("<B1-Motion>", self.reorder)
        self.tabs_nb.bind("<ButtonRelease-1>", self.reorder_save)
        self.tabs_nb.bind("<Double-Button-1>", self.change_tab_name)
        tab_style = ttk.Style()
        tab_style.configure('TNotebook', tabposition='new')
        # tab_style.configure('TNotebook', tabposition='en')

        self.tabs_nb.bind("<<NotebookTabChanged>>", self.on_tab_selected)

        # Tree Control Buttons
        self.move_left_button = ttk.Button(self.tab_frame,
                                           text="\u2B9C",
                                           command=lambda: self.move_left(),
                                           bootstyle="outline",
                                           state="disabled")

        self.move_right_button = ttk.Button(self.tab_frame,
                                            text="\u2B9E",
                                            command=lambda: self.move_right(),
                                            bootstyle="outline",
                                            state="disabled")

        # New and Delete Buttons for tabs.
        self.tabs_nb.grid(row=1, column=0, columnspan=4, sticky='nsew')
        self.move_left_button.grid(row=2, column=0, columnspan=2, sticky='new')
        self.move_right_button.grid(row=2, column=2, columnspan=2, sticky='new')

        # Packing Tab Frame Widgets
        self.button_frame = ttk.Frame(self.tab_frame)
        self.button_frame.columnconfigure(0, weight=1, uniform='a')
        self.button_frame.columnconfigure(1, weight=1, uniform='a')
        self.button_frame.rowconfigure(0, weight=1)

        # Binding for tree select
        self.tree_select = self.move_left_button.bindtags() + ("tree_select",)
        self.move_left_button.bindtags(self.tree_select)
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

        self.button_frame.grid(row=0, column=3, sticky='se')

        # inserting frames on to configuration frame.
        self.tab_frame.grid(row=1, column=1, sticky='nsew', padx=(5, 5))
        self.side_bar_frame.grid(row=0, column=0, sticky='new', rowspan=3, padx=(5, 5))

        # Creating Tabs. Class method appends to tabs to list and returns list of tab objects
        self.tabs_list = ScrollFrame.from_tabs_info(self.delete_client, self.tabs_nb, self.tabs_info)
        for tab in self.tabs_list:
            self.tabs_nb.add(tab, text=f'{tab.tab_name}')
            tab.update_scroll_height()

        self.buttons_list = [self.move_left_button, self.move_right_button]
        self.bind_class("tree_select", '<Button-1>', self.enable_nav_buttons)

    def edit_client(self):
        tree_index = self.clients_tree.focus()
        if tree_index:
            client_name = self.clients_tree.item(tree_index)['values'][0]
            ClientDlg(self.clients_tree.client_dictionary,
                      self.insert_client,
                      self.insert_another_client,
                      client_name=client_name)

    def edit_command(self):
        tree_index = self.commands_tree.focus()
        if tree_index:
            command_name = self.commands_tree.item(tree_index)['values'][0]
            CommandDlg(self.commands_tree.command_dictionary,
                       self.insert_command,
                       self.insert_another_command,
                       "command",
                       command_name=command_name)

    def change_tab_name(self, event):
        RenameTabWindow(self.tabs_nb, self.tab_id, self.tabs_info)

    def reorder_save(self, event):
        tab_names = [self.tabs_nb.tab(i, option="text") for i in self.tabs_nb.tabs()]
        temp_dict = dict()
        for tab in tab_names:
            temp_dict[tab] = self.tabs_info[tab]
        self.tabs_info.clear()
        for tab in tab_names:
            self.tabs_info[tab] = temp_dict[tab]

    def reorder(self, event):
        try:
            index = self.tabs_nb.index(f"@{event.x},{event.y}")
            self.tabs_nb.insert(index, child=self.tabs_nb.select())
        except tk.TclError:
            pass

    # @staticmethod
    # def write_json():
    #     with open('commandconfig.json', 'w') as f:
    #         json.dump(ConfigurationManager.configurations, f, indent=2)

    @classmethod
    def from_active_config(cls, parent, active_config_data, m_write_json):
        try:
            return cls(parent,
                       m_write_json,
                       active_config_data['clients'],
                       active_config_data['commands'],
                       active_config_data['tabs_info'])
        except KeyError as e:
            print(f'Key {e} is incorrect.')

    def enable_nav_buttons(self, event):
        x, y = event.widget.winfo_pointerxy()
        target = event.widget.winfo_containing(x, y)
        master_target = event.widget.winfo_containing(x, y).master
        if master_target in self.active_scroll_frame.client_tab_frame_list:
            self.active_tab_tree_frame = master_target
            for tree in self.active_scroll_frame.tab_tree_list:
                if tree == target:
                    tree.disable_scroll()
                    self.move_left_button.configure(state='enabled')
                    self.move_right_button.configure(state='enabled')
                else:
                    tree.enable_scroll()
        elif target in self.buttons_list:
            pass
        else:
            self.move_left_button.configure(state='disabled')
            self.move_right_button.configure(state='disabled')
            self.active_tab_tree_frame = None

    def move_right(self):
        if self.active_tab_tree_frame:
            self.shift_index_up()
            self.re_sort(self.client_tab_frame_list)
            self.re_sort_dict()
            self.unpack_client_frame()
            for client_tab_frame in self.client_tab_frame_list:
                row, column = self.get_row_and_column(client_tab_frame.index)
                self.repack_client_frame(client_tab_frame, row, column)

    def move_left(self):
        if self.active_tab_tree_frame:
            self.shift_index_down()
            self.re_sort(self.client_tab_frame_list)
            self.re_sort_dict()
            self.unpack_client_frame()
            for client_tab_frame in self.client_tab_frame_list:
                row, column = self.get_row_and_column(client_tab_frame.index)
                self.repack_client_frame(client_tab_frame, row, column)

    def delete_client(self, tree_frame):
        """
        This will be passed to TabTreeMouse Over.
        :return:None
        """
        self.unpack_client_frame()
        for i, client_tab_frame in enumerate(self.active_scroll_frame.client_tab_frame_list):
            if client_tab_frame.index == tree_frame.index:
                del self.active_scroll_frame.client_tab_frame_list[i]
                del self.tabs_info[self.active_scroll_frame.tab_name][str(i + 1)]

        for client_tab_frame in self.active_scroll_frame.client_tab_frame_list:
            if client_tab_frame.index > tree_frame.index:
                client_tab_frame.index -= 1

        self.re_sort_dict()
        self.re_sort(self.client_tab_frame_list)
        for client_tab_frame in self.client_tab_frame_list:
            row, column = self.get_row_and_column(client_tab_frame.index)
            self.repack_client_frame(client_tab_frame, row, column)

        # drop tab tree index by one so next client dragged and dropped doesn't skip a number
        self.active_scroll_frame.client_tab_tree_index -= 1

        # Get index of last frame as that is what determines the scroll area. Or I could count items in frame list.
        self.active_scroll_frame.update_scroll_height()

    def re_sort_dict(self):
        # Re-indexing trees to not have gaps in numbering by looping through dictionary and initializing
        # a new dictionary with the correct numbering as the key.
        temp_dict = dict()
        for index, (key, value) in enumerate(self.tabs_info[self.active_scroll_frame.tab_name].items()):
            temp_dict[str(index + 1)] = self.tabs_info[self.active_scroll_frame.tab_name][key]
        self.tabs_info[self.active_scroll_frame.tab_name].clear()
        self.tabs_info[self.active_scroll_frame.tab_name].update(temp_dict)

    def shift_index_up(self):
        try:
            # Making sure frame is not last.
            if self.active_tab_tree_frame.index < self.client_tab_frame_list[-1].index:
                for i, client_tab_frame in enumerate(self.client_tab_frame_list):
                    if client_tab_frame.index == (self.active_tab_tree_frame.index + 1):  # One above
                        client_tab_frame.index -= 1
                        temp = self.tabs_info[self.active_scroll_frame.tab_name][str(i)]
                        self.tabs_info[self.active_scroll_frame.tab_name][str(i)] = \
                            self.tabs_info[self.active_scroll_frame.tab_name][str(i + 1)]
                        self.tabs_info[self.active_scroll_frame.tab_name][str(i + 1)] = temp
                self.active_tab_tree_frame.index += 1
        except IndexError or AttributeError:
            pass

    def shift_index_down(self):
        for i, client_tab_frame in enumerate(self.client_tab_frame_list):
            if client_tab_frame.index == (self.active_tab_tree_frame.index - 1):  # One below
                client_tab_frame.index += 1
                temp = self.tabs_info[self.active_scroll_frame.tab_name][str(i + 1)]
                self.tabs_info[self.active_scroll_frame.tab_name][str(i + 1)] = \
                    self.tabs_info[self.active_scroll_frame.tab_name][str(i + 2)]
                self.tabs_info[self.active_scroll_frame.tab_name][str(i + 2)] = temp
        self.active_tab_tree_frame.index -= 1
        self.active_tab_tree_frame.index = max(self.active_tab_tree_frame.index, 1)  # Limit to 0

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
        row = (floor((client_frame_index - 1) / 5)) + 1
        column = ((client_frame_index - 1) % 5) + 1
        return row, column

    def on_tab_selected(self, event):
        if self.tabs_list:
            selected_tab = event.widget.select()
            self.tab_id = self.tabs_nb.index(selected_tab)
            scroll_frame = self.tabs_list[self.tab_id]
            # todo Verify how class memory is managed. Is the old one being replaced?
            client_dnd = ClientDragManager(scroll_frame, self.tabs_info[scroll_frame.tab_name], self.delete_client)
            client_dnd.add_dragable(self.clients_tree)
            self.active_scroll_frame = scroll_frame
            self.client_tab_frame_list = scroll_frame.client_tab_frame_list

    def insert_tab(self, window_instance, new_tab):
        if new_tab:
            tab = ScrollFrame(self.tabs_nb,
                              new_tab,
                              self.delete_client)
            self.tabs_list.append(tab)
            self.tabs_nb.add(tab, text=f'{new_tab}')
            # TODO Create proper structure
            self.tabs_info[new_tab] = dict()
        window_instance.destroy()

    def insert_another_tab(self, new_tab):
        if new_tab:
            tab = ScrollFrame(self.tabs_nb,
                              new_tab,
                              self.delete_client)
            self.tabs_list.append(tab)
            self.tabs_nb.add(tab, text=f'{new_tab}')
            self.tabs_info[new_tab] = dict()

    def delete_tab(self):
        # Todo Why am I looping through tabs instead of just using select?
        for item in self.tabs_nb.winfo_children():
            if str(item) == self.tabs_nb.select():
                name = self.tabs_nb.tab(self.tabs_nb.select(), "text")
                print(name)
                item.pack_forget()  # To prevent scroll errors.
                item.destroy()
                del self.tabs_list[self.tab_id]
                del self.tabs_info[name]
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
                 m_delete_client,
                 tab_data=None):
        super().__init__(master=parent)

        # widget data
        self.list_height = 0
        self.m_delete_client = m_delete_client
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
        self.new_tags = self.scroll_frame.bindtags() + ("scroll_frame_widgets", "tree_select",)
        self.scroll_frame.bindtags(self.new_tags)

        # scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')

        # Creating tree frame:
        client_tab_frame_list = ClientTabFrame.from_tab_info(self.scroll_frame, self.tab_data)
        self.tab_tree_list = TabBarTree.from_tab_data(client_tab_frame_list, self.tab_data)
        tt_mouse_over_list = TabTreeMouseOver.from_client_tab_frame_list(client_tab_frame_list, self.tab_tree_list,
                                                                         self.m_delete_client)

        # packing trees and mouse_over frame to client tab_frame
        for tree, mouse_over_frame in zip(self.tab_tree_list, tt_mouse_over_list):
            tree.grid(row=0, sticky='nsew')
            mouse_over_frame.grid(row=1, sticky='nsew')

        # put client_tab_frame on the scroll frame
        for tab_frame in client_tab_frame_list:
            row, column = self.get_row_and_column(tab_frame.index)
            self.grid_tab_frame(tab_frame, row, column)

        # events
        self.canvas.bind_class('scroll_frame_widgets', '<MouseWheel>',
                               lambda event: self.canvas.yview_scroll(-int(event.delta / 60), "units"))
        self.bind('<Configure>', self.update_scroll_area_resize_event)

    def update_scroll_height(self):
        self.update_idletasks()
        scroll_frame_height = (self.scroll_frame.grid_bbox()[-1])
        self.update_scroll_area(scroll_frame_height)

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
                       m_delete_client,
                       tabs_nb,
                       tabs_info):
        tabs_data_list = list()
        print(type(tabs_info))
        for tab_name, tab_data in tabs_info.items():
            tabs_data_list.append(cls(tabs_nb, tab_name, m_delete_client, tab_data))
        return tabs_data_list

    @staticmethod
    def get_row_and_column(client_frame_index):
        row = (floor((client_frame_index - 1) / 5)) + 1
        column = ((client_frame_index - 1) % 5) + 1
        return row, column

    def grid_tab_frame(self, client_tab_frame, row, column):
        tree_pad_x = 5
        tree_pad_y = 5
        self.scroll_frame.columnconfigure(1, weight=1, uniform='a')
        self.scroll_frame.columnconfigure(2, weight=1, uniform='a')
        self.scroll_frame.columnconfigure(3, weight=1, uniform='a')
        self.scroll_frame.columnconfigure(4, weight=1, uniform='a')
        self.scroll_frame.columnconfigure(5, weight=1, uniform='a')
        client_tab_frame.grid(row=row, column=column,
                              padx=tree_pad_x,
                              pady=tree_pad_y,
                              sticky="nsew")
        self.client_tab_frame_list.append(client_tab_frame)
        self.client_tab_tree_index += 1


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


if __name__ == "__main__":
    ConfigurationManager.from_json('commandconfig.json')
