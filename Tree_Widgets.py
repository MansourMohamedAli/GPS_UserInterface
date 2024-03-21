import tkinter as tk
from tkinter import ttk
from math import floor
from command_window import CommandWindow


class ClientListTree(ttk.Treeview):
    def __init__(self, parent, client_dictionary, headings):
        super().__init__(master=parent, columns=headings, show='headings')
        self.headings = headings
        self.parent = parent
        self.get_tree_headings()
        self.bind('<Delete>', self.delete_row_keyboard_button)
        self.client_dictionary = client_dictionary
        self.insert_clients()

    def get_tree_headings(self):
        for heading in self.headings:
            self.heading(heading, text=str(heading))

    def delete_row_keyboard_button(self, event):
        self.delete_row()

    def delete_row(self):
        selected_items = self.selection()
        for client in selected_items:
            client_full_tree_info = self.item(client)
            client_name = client_full_tree_info['values'][0]
            del self.client_dictionary[client_name]
            self.delete(client)

    def insert_clients(self):
        for new_client in self.client_dictionary:
            if new_client:
                self.insert(parent='', index=tk.END, values=[new_client])


class CommandListTree(ttk.Treeview):
    def __init__(self, parent, command_dictionary, headings):
        super().__init__(master=parent, columns=headings, show='headings')
        self.headings = headings
        self.parent = parent
        self.get_tree_headings()
        self.bind('<Delete>', self.delete_row_keyboard_button)
        self.command_dictionary = command_dictionary
        self.insert_commands()

    def get_tree_headings(self):
        for heading in self.headings:
            self.heading(heading, text=str(heading))

    def delete_row_keyboard_button(self, event):
        self.delete_row()

    def delete_row(self):
        selected_items = self.selection()
        for command in selected_items:
            command_full_tree_info = self.item(command)
            command_name = command_full_tree_info['values'][0]
            del self.command_dictionary[command_name]
            self.delete(command)

    def insert_commands(self):
        for new_command in self.command_dictionary:
            if new_command:
                self.insert(parent='', index=tk.END, values=[new_command])


class TabBarTree(ttk.Treeview):
    def __init__(self, parent, tree_index, tab_client_from_json, tab_commands_from_json, clients_dictionary,
                 commands_dictionary):
        super().__init__(master=parent, columns=tab_client_from_json, show='headings')
        self.headings = tab_client_from_json
        self.parent = parent
        self.get_tree_headings()
        self.bind('<Delete>', self.delete_row)
        self.tree_name = "tab_tree"
        self.tree_index = tree_index
        self.row = None
        self.column = None
        self.ip_address = None
        self.mac_address = None
        self.command_names = tab_commands_from_json
        self.commands = list()

        self.clients_dictionary = clients_dictionary
        self.commands_dictionary = commands_dictionary

        self.initialize_client_info()
        self.initialize_commands()
        # print(self.command_names)
        # print(self.commands)

        # print(self.ip_address, self.mac_address)

        self.no_scroll_tags = self.bindtags()
        # Adding new tag for frame to allow scroll on TabTree and background.
        self.scroll_tags = self.bindtags() + ("scroll_frame_widgets",)
        self.bindtags(self.scroll_tags)
        self.bind('<ButtonPress-1>', self.enable_scroll)
        self.bind('<<TreeviewSelect>>', self.disable_scroll)
        self.scroll_state = True

    # @classmethod
    # def from_json(cls,
    #               parent,
    #               tree_index,
    #               tab_client_from_json,
    #               tab_commands_from_json,
    #               clients_dictionary,
    #               commands_dictionary):
    #
    #     return

    def initialize_client_info(self):
        self.ip_address, self.mac_address = self.clients_dictionary[self.headings[0]]

    def initialize_commands(self):
        if self.command_names[0]:
            for command in self.command_names:
                self.insert(parent='', index=tk.END, values=[command])
            # self.update_command_list()
        else:
            self.command_names = list()

    def enable_scroll(self, event):
        if not self.scroll_state:
            self.bindtags(self.scroll_tags)
            self.selection_clear()
            self.scroll_state = True

    def disable_scroll(self, event):
        if self.scroll_state:
            self.bindtags(self.no_scroll_tags)
            self.scroll_state = False

    def get_tree_headings(self):
        for h in self.headings:
            self.heading(h, text=str(h))

    def delete_row(self, event):
        selected_items = self.selection()
        for item in selected_items:
            self.delete(item)
        self.update_command_list()

    def update_command_list(self):
        """
        Duplicate commands are allowed in the tree and using the .remove() method will always
        remove the first occurrence in a list. To get around this issue and allow the removal
        of later occurrences, The command_names and commands list are cleared. Then the
        command_names list is populated in order using the Tkinter get_children() method. Finally,
        the command_tree dictionary is searched using the command_name as a key and the appropriate
        command is added in the correct order back to the commands list.
        :return: None
        """
        self.command_names.clear()
        self.commands.clear()
        for item in self.get_children():
            command_name = self.item(item)['values'][0]
            self.command_names.append(command_name)
            command = self.commands_dictionary[command_name]
            self.commands.append(command)


class ClientTabFrame(ttk.Frame):
    def __init__(self, parent, index):
        super().__init__(master=parent)
        self.index = index


class TabTreeMouseOver:
    def __init__(self, client_tab_frame,
                 client_tab_frame_list,
                 client_tab_tree,
                 m_reduce_tab_tree_index,
                 m_update_scroll_area):

        self.client_tab_frame = client_tab_frame
        self.client_tab_frame_list = client_tab_frame_list
        self.client_tab_tree = client_tab_tree
        self.m_reduce_tab_tree_index = m_reduce_tab_tree_index
        self.m_update_scroll_area = m_update_scroll_area
        self.client_tab_frame.bind('<Enter>', self.mouse_over)
        self.client_tab_frame.bind('<Leave>', self.mouse_leave)
        self.button_frame = ttk.Frame(client_tab_frame)
        self.button_frame.rowconfigure(0, weight=1, uniform='a')
        self.button_frame.columnconfigure(0, weight=1, uniform='a')
        self.button_frame.columnconfigure(1, weight=1, uniform='a')
        self.button_frame.columnconfigure(2, weight=1, uniform='a')
        self.button_frame.columnconfigure(3, weight=1, uniform='a')
        self.move_left_button = ttk.Button(self.button_frame,
                                           text="\u2B9C",
                                           width=5,
                                           command=self.move_left)

        self.move_right_button = ttk.Button(self.button_frame,
                                            text="\u2B9E",
                                            width=5,
                                            command=self.move_right)

        self.new_button = ttk.Button(self.button_frame,
                                     text="+",
                                     width=5,
                                     command=lambda: CommandWindow(self.client_tab_tree.tab_tree_dictionary,
                                                                   self.insert_command,
                                                                   self.insert_another_command,
                                                                   ))

        self.delete_button = ttk.Button(self.button_frame,
                                        text=u"\U0001F5D1",
                                        width=5,
                                        command=self.delete_client)

        self.move_left_button.grid(row=0, column=0)
        self.new_button.grid(row=0, column=1)
        self.delete_button.grid(row=0, column=2)
        self.move_right_button.grid(row=0, column=3)

        scroll_tags = self.move_left_button.bindtags() + ("scroll_frame_widgets",)
        self.move_left_button.bindtags(scroll_tags)
        self.new_button.bindtags(scroll_tags)
        self.delete_button.bindtags(scroll_tags)
        self.move_right_button.bindtags(scroll_tags)

        scroll_tags = self.button_frame.bindtags() + ("scroll_frame_widgets",)
        self.button_frame.bindtags(scroll_tags)

    def mouse_over(self, event):
        self.button_frame.pack(side="bottom")
        scroll_tags = self.button_frame.bindtags() + ("scroll_frame_widgets",)
        self.button_frame.bindtags(scroll_tags)

    def mouse_leave(self, event):
        self.button_frame.pack_forget()

    def move_right(self):
        self.shift_index_up()
        self.re_sort(self.client_tab_frame_list)
        self.unpack_client_frame()
        for client_tab_frame in self.client_tab_frame_list:
            row, column = self.get_row_and_column(client_tab_frame.index)
            self.repack_client_frame(client_tab_frame, row, column)

    def move_left(self):
        self.shift_index_down()
        self.re_sort(self.client_tab_frame_list)
        self.unpack_client_frame()
        for client_tab_frame in self.client_tab_frame_list:
            row, column = self.get_row_and_column(client_tab_frame.index)
            self.repack_client_frame(client_tab_frame, row, column)

    def shift_index_up(self):
        if self.client_tab_frame.index < self.client_tab_frame_list[-1].index:  # Making sure frame is not last.
            for client_tab_frame in self.client_tab_frame_list:
                if client_tab_frame.index == (self.client_tab_frame.index + 1):  # One above
                    client_tab_frame.index -= 1
            self.client_tab_frame.index += 1

    def shift_index_down(self):
        for client_tab_frame in self.client_tab_frame_list:
            if client_tab_frame.index == (self.client_tab_frame.index - 1):  # One below
                client_tab_frame.index += 1
        self.client_tab_frame.index -= 1
        self.client_tab_frame.index = max(self.client_tab_frame.index, 0)  # Limit to 0

    def delete_client(self):
        self.unpack_client_frame()
        for index, client_tab_frame in enumerate(self.client_tab_frame_list):
            if client_tab_frame.index == self.client_tab_frame.index:
                del self.client_tab_frame_list[index]

        for client_tab_frame in self.client_tab_frame_list:
            if client_tab_frame.index > self.client_tab_frame.index:
                client_tab_frame.index -= 1

        self.re_sort(self.client_tab_frame_list)
        for client_tab_frame in self.client_tab_frame_list:
            row, column = self.get_row_and_column(client_tab_frame.index)
            self.repack_client_frame(client_tab_frame, row, column)

        # drop tab tree index by one so next client dragged and dropped doesn't skip # a number
        self.m_reduce_tab_tree_index()
        # Get index of last frame as that is what determines the scroll area. Or I could count items in frame list.
        last_frame = len(self.client_tab_frame_list)
        last_row, last_column = self.get_row_and_column(last_frame)
        scroll_frame_height = (self.client_tab_frame.winfo_height() * last_row
                               + ((last_row * 2) * 0))
        self.m_update_scroll_area(scroll_frame_height)

    def unpack_client_frame(self):
        for frame in self.client_tab_frame_list:
            frame.grid_forget()

    @staticmethod
    def get_row_and_column(client_frame_index):
        row = (floor(client_frame_index / 5)) + 1
        column = (client_frame_index % 5) + 1
        return row, column

    @staticmethod
    def re_sort(client_tab_frame_list):
        return client_tab_frame_list.sort(key=lambda x: x.index)

    @staticmethod
    def repack_client_frame(client_tab_frame, row, column):
        tree_pad_x = 5
        tree_pad_y = 0
        client_tab_frame.grid(row=row, column=column,
                              padx=tree_pad_x,
                              pady=tree_pad_y,
                              sticky="nsew")

    def insert_command(self, window_instance, new_command):
        if new_command:
            self.client_tab_tree.insert(parent='', index=tk.END, values=new_command)
        window_instance.destroy()

    def insert_another_command(self, new_command):
        if new_command:
            self.client_tab_tree.insert(parent='', index=tk.END, values=new_command)
