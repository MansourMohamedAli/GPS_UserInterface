import tkinter as tk
from tkinter import ttk
from math import floor
from command_window import CommandWindow


class ClientListTree(ttk.Treeview):
    def __init__(self, parent, clients, *args):
        super().__init__(master=parent, columns=args, show='headings')
        self.args = args
        self.parent = parent
        self.get_tree_headings()
        self.bind('<Delete>', self.delete_row_keyboard_button)
        # self.clients = clients
        self.client_list = list()
        self.insert_client(clients)

    def get_tree_headings(self):
        for arg in self.args:
            self.heading(arg, text=str(arg))

    def delete_row_keyboard_button(self, event):
        self.delete_row()

    def delete_row(self):
        selected_items = self.selection()
        clients_to_delete = list()
        for client in selected_items:
            client_full_tree_info = self.item(client)
            client_info = client_full_tree_info['values']
            c = list()
            for item in client_info:
                c.append(str(item))
            clients_to_delete.append(c)
            self.delete(client)

        for client in self.client_list:
            if client in clients_to_delete:
                self.client_list.remove(client)

    def append_client_list(self, client):
        self.client_list.append(client)

    def insert_client(self, new_client):
        for client in new_client:
            if client[0]:
                self.insert(parent='', index=tk.END, values=client)
                self.append_client_list(client)


class CommandListTree(ttk.Treeview):
    def __init__(self, parent, commands, *args):
        super().__init__(master=parent, columns=args, show='headings')
        self.args = args
        self.parent = parent
        self.get_tree_headings()
        self.bind('<Delete>', self.delete_row_keyboard_button)
        self.command_list = list()
        self.insert_command(commands)

    def get_tree_headings(self):
        for arg in self.args:
            self.heading(arg, text=str(arg))

    def delete_row_keyboard_button(self, event):
        self.delete_row()

    def delete_row(self):
        selected_items = self.selection()
        commands_to_delete = list()
        for command in selected_items:
            command_full_tree_info = self.item(command)
            command_info = command_full_tree_info['values']
            c = list()
            for item in command_info:
                c.append(str(item))
            commands_to_delete.append(c)
            self.delete(command)

        for command in self.command_list:
            if command in commands_to_delete:
                self.command_list.remove(command)

    def append_command_list(self, command):
        self.command_list.append(command)

    def insert_command(self, new_command):
        for command in new_command:
            if command[0]:
                self.insert(parent='', index=tk.END, values=command)
                self.append_command_list(command)


class TabBarTree(ttk.Treeview):
    def __init__(self, parent, tree_index, headings):
        super().__init__(master=parent, columns=headings, show='headings')
        self.headings = headings
        self.parent = parent
        self.get_tree_headings()
        self.bind('<Delete>', self.delete_row)
        self.tree_name = "tab_tree"
        self.tree_index = tree_index
        self.row = None
        self.column = None
        self.client_name = None
        self.mac_address = None

        self.no_scroll_tags = self.bindtags()
        # Adding new tag for frame to allow scroll on TabTree and background.
        self.scroll_tags = self.bindtags() + ("scroll_frame_widgets",)
        self.bindtags(self.scroll_tags)
        self.bind('<ButtonPress-1>', self.enable_scroll)
        self.bind('<<TreeviewSelect>>', self.disable_scroll)
        self.scroll_state = True

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


class ClientFrame(ttk.Frame):
    def __init__(self, parent, index):
        super().__init__(master=parent)
        self.index = index


class TabTreeMouseOver:
    def __init__(self, client_frame, tab_tree_frame_list, target_frame, client_tree, m_reduce_tab_tree_index):
        self.client_frame = client_frame
        self.target_frame = target_frame
        self.tab_tree_frame_list = tab_tree_frame_list
        self.client_tree = client_tree
        self.m_reduce_tab_tree_index = m_reduce_tab_tree_index
        self.client_frame.bind('<Enter>', self.mouse_over)
        self.client_frame.bind('<Leave>', self.mouse_leave)
        self.button_frame = ttk.Frame(client_frame)
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
                                     command=lambda: CommandWindow(self.insert_command,
                                                                   self.insert_another_command))

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
        self.re_sort(self.tab_tree_frame_list)
        self.unpack_client_frame()
        for client_frame in self.tab_tree_frame_list:
            row, column = self.get_row_and_column(client_frame.index)
            self.repack_client_frame(client_frame, row, column)

    def move_left(self):
        self.shift_index_down()
        self.re_sort(self.tab_tree_frame_list)
        self.unpack_client_frame()
        for client_frame in self.tab_tree_frame_list:
            row, column = self.get_row_and_column(client_frame.index)
            self.repack_client_frame(client_frame, row, column)

    def shift_index_up(self):
        if self.client_frame.index < self.tab_tree_frame_list[-1].index:  # Making sure frame is not last.
            for client_frame in self.tab_tree_frame_list:
                if client_frame.index == (self.client_frame.index + 1):  # One above
                    client_frame.index -= 1
            self.client_frame.index += 1

    def shift_index_down(self):
        for client_frame in self.tab_tree_frame_list:
            if client_frame.index == (self.client_frame.index - 1):  # One below
                client_frame.index += 1
        self.client_frame.index -= 1
        self.client_frame.index = max(self.client_frame.index, 0)  # Limit to 0

    def delete_client(self):
        self.unpack_client_frame()
        for index, client_frame in enumerate(self.tab_tree_frame_list):
            if client_frame.index == self.client_frame.index:
                del self.tab_tree_frame_list[index]

        for client_frame in self.tab_tree_frame_list:
            if client_frame.index > self.client_frame.index:
                client_frame.index -= 1

        self.re_sort(self.tab_tree_frame_list)
        for client_frame in self.tab_tree_frame_list:
            row, column = self.get_row_and_column(client_frame.index)
            self.repack_client_frame(client_frame, row, column)

        self.m_reduce_tab_tree_index()  # drop tab tree index by one so next client dragged and dropped doesn't skip
        # a number
        print(self.tab_tree_frame_list)

    def unpack_client_frame(self):
        for frame in self.tab_tree_frame_list:
            frame.grid_forget()

    @staticmethod
    def get_row_and_column(client_frame_index):
        row = (floor(client_frame_index / 5)) + 1
        column = (client_frame_index % 5) + 1
        return row, column

    @staticmethod
    def re_sort(tab_tree_frame_list):
        return tab_tree_frame_list.sort(key=lambda x: x.index)

    @staticmethod
    def repack_client_frame(client_frame, row, column):
        tree_pad_x = 5
        tree_pad_y = 0
        client_frame.grid(row=row, column=column,
                          padx=tree_pad_x,
                          pady=tree_pad_y,
                          sticky="nsew")

    def insert_command(self, window_instance, new_command):
        if new_command:
            self.client_tree.insert(parent='', index=tk.END, values=new_command)
        window_instance.destroy()

    def insert_another_command(self, new_command):
        if new_command:
            self.client_tree.insert(parent='', index=tk.END, values=new_command)
