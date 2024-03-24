import tkinter as tk
from tkinter import ttk
from math import floor
from add_button_dlg import CommandWindow


class ClientListTree(ttk.Treeview):
    def __init__(self, parent, client_dictionary, headings):
        super().__init__(master=parent, columns=headings, show='headings')
        self.headings = headings
        self.parent = parent
        self.bind('<Delete>', self.delete_row_keyboard_button)
        self.client_dictionary = client_dictionary

    @classmethod
    def from_json(cls, parent, client_dictionary, heading):
        tree = cls(parent, client_dictionary, heading)
        for new_client in client_dictionary:
            if new_client:
                cls.insert(tree, parent='', index=tk.END, values=[new_client])
            #  Initialize Tree Title
            for heading in tree.headings:
                tree.heading(heading, text=str(heading))
        return tree

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
        self.bind('<Delete>', self.delete_row_keyboard_button)
        self.command_dictionary = command_dictionary

    @classmethod
    def from_json(cls, parent, command_dictionary, heading):
        tree = cls(parent, command_dictionary, heading)
        for new_command in command_dictionary:
            if new_command:
                cls.insert(tree, parent='', index=tk.END, values=[new_command])
        #  Initialize Tree Title
        for heading in tree.headings:
            tree.heading(heading, text=str(heading))
        return tree

    def delete_row_keyboard_button(self, event):
        self.delete_row()

    def delete_row(self):
        selected_items = self.selection()
        for command in selected_items:
            command_full_tree_info = self.item(command)
            command_name = command_full_tree_info['values'][0]
            del self.command_dictionary[command_name]
            self.delete(command)


class TabBarTree(ttk.Treeview):
    def __init__(self, parent, client_name, ip_address, mac_address, command_name_value_pair):
        super().__init__(master=parent, columns=client_name, show='headings')
        self.headings = client_name
        self.parent = parent
        self.get_tree_headings()
        self.bind('<Delete>', self.delete_row)
        self.tree_name = "tab_tree"
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.command_name_value_pair = command_name_value_pair

        self.no_scroll_tags = self.bindtags()
        # Adding new tag for frame to allow scroll on TabTree and background.
        self.scroll_tags = self.bindtags() + ("scroll_frame_widgets",)
        self.bindtags(self.scroll_tags)
        self.bind('<ButtonPress-1>', self.enable_scroll)
        self.bind('<<TreeviewSelect>>', self.disable_scroll)
        self.scroll_state = True

    @classmethod
    def from_json(cls,
                  parent,
                  clients_dictionary,
                  client_name,
                  command_name_value_pair):
        """
        Initializes tree in scroll frame "Tab Tree". Assigns tree heading with client name
        and initializes IP and MAC address using the client_dictionary.

        :param parent: The Client Tab Frame the tree is packed into.
        :param clients_dictionary: Dictionary containing IP, MAC definitions.
        :param client_name: The name of the client that this tree is made for.
        :param command_name_value_pair: A list of Command Name, Command Value pairs. This is
        passed here because the tree will modify it (adding and removing commands).
        :return: New TabBarTree instance.
        """
        ip_address, mac_address = clients_dictionary[client_name[0]]

        tree = cls(parent,
                   client_name,
                   ip_address,
                   mac_address,
                   command_name_value_pair)

        if command_name_value_pair[0]:
            for name, value in command_name_value_pair:
                cls.insert(tree, parent='', index=tk.END, values=[name])  # Insert name on to tree.
        else:
            # This clears the "None" that appears at the beginning of the list.
            # This line should execute when a new client is dropped in scroll frame.
            cls.command_name_value_pair = list()
        return tree

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
        print(self.command_name_value_pair)
        selected_items = self.selection()
        for row in selected_items:
            index = self.get_selected_row_number(row)
            del self.command_name_value_pair[index]
            self.delete(row)
        print(self.command_name_value_pair)

    def get_selected_row_number(self, row):
        """
        Converts Tkinter 'I00*' notation to an integer.
        :param row: Tkinter row number
        :return: integer row number
        """
        return self.index(row)


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

        # drop tab tree index by one so next client dragged and dropped doesn't skip a number
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
