import tkinter as tk
from tkinter import ttk


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
