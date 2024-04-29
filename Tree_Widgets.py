import tkinter as tk
import ttkbootstrap as ttk
from add_button_dlg import TabCommandDlg


class ClientListTree(ttk.Treeview):
    def __init__(self, parent, client_dictionary, headings):
        super().__init__(master=parent, columns=headings, show='headings', bootstyle='primary')
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
        super().__init__(master=parent, columns=headings, show='headings', bootstyle='primary')
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
    def __init__(self, parent, client_name, command_list=None, tab_command_dict=None):
        super().__init__(master=parent, columns=client_name, show='headings', bootstyle='primary')
        self.client_name = client_name
        self.heading(client_name, text=str(client_name))
        # self.get_tree_headings()
        self.bind('<Delete>', self.delete_row)
        self.tree_name = "tab_tree"
        self.command_list = command_list
        self.tab_command_dict = tab_command_dict

        self.no_scroll_tags = self.bindtags()
        # Adding new tag for frame to allow scroll on TabTree and background.
        self.scroll_tags = self.bindtags() + ("scroll_frame_widgets",)
        self.bindtags(self.scroll_tags)
        self.bind('<ButtonPress-1>', self.enable_scroll)
        self.bind('<<TreeviewSelect>>', self.disable_scroll)
        self.scroll_state = True

        self.tree_select = self.bindtags() + ("tree_select",)
        self.bindtags(self.tree_select)
        self.populate_tree()

    def populate_tree(self):
        if self.command_list:
            for command in self.command_list:
                self.insert(parent='', index=tk.END, values=[command])  # Insert name on to tree.

    @classmethod
    def from_tab_data(cls,
                      parent_frame_list,
                      tab_data):
        tab_tree_list = list()
        if tab_data:
            for index, tree_info in enumerate(tab_data.values()):
                parent_frame = parent_frame_list[index]
                client_name = tree_info['client']
                commands_dictionary = tree_info['tree_commands']
                command_list = tree_info['command_list']
                tab_tree_list.append(cls(parent_frame, client_name, command_list, commands_dictionary))
        return tab_tree_list

        # @classmethod
        # def from_json(cls,
        #               parent,
        #               clients_dictionary,
        #               client_name,
        #               command_name_value_pair):
        # """
        # Initializes tree in scroll frame "Tab Tree". Assigns tree heading with client name
        # and initializes IP and MAC address using the client_dictionary.
        #
        # :param parent: The Client Tab Frame the tree is packed into.
        # :param clients_dictionary: Dictionary containing IP, MAC definitions.
        # :param client_name: The name of the client that this tree is made for.
        # :param command_name_value_pair: A list of Command Name, Command Value pairs. This is
        # passed here because the tree will modify it (adding and removing commands).
        # :return: New TabBarTree instance.
        # """
        # ip_address, mac_address = clients_dictionary[client_name[0]]
        #
        # tree = cls(parent,
        #            client_name,
        #            ip_address,
        #            mac_address,
        #            command_name_value_pair)
        #
        # if command_name_value_pair[0]:
        #     for name, value in command_name_value_pair:
        #         cls.insert(tree, parent='', index=tk.END, values=[name])  # Insert name on to tree.
        # else:
        #     # This clears the "None" that appears at the beginning of the list.
        #     # This line should execute when a new client is dropped in scroll frame.
        #     cls.command_name_value_pair = list()
        # return tree

    def enable_scroll(self, event):
        if not self.scroll_state:
            self.bindtags(self.scroll_tags)
            self.selection_clear()
            self.scroll_state = True

    def disable_scroll(self, event):
        if self.scroll_state:
            self.bindtags(self.no_scroll_tags)
            self.scroll_state = False

    # def get_tree_headings(self):
    #     for h in self.client_name:
    #         self.heading(h, text=str(h))

    def delete_row(self, event):
        selected_items = self.selection()
        for row in selected_items:
            index = self.get_selected_row_number(row)
            del self.tab_command_dict[index]
            self.delete(row)

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
        self.rowconfigure(0, weight=6, uniform='a')
        self.rowconfigure(1, weight=1, uniform='a')
        self.columnconfigure(0, weight=1, uniform='a')
        self.scroll_tags = self.bindtags() + ("scroll_frame_widgets",)
        self.bindtags(self.scroll_tags)

    @classmethod
    def from_tab_info(cls, parent, tab_data):
        tab_frame_list = list()
        if tab_data:
            for index in tab_data:
                tab_frame_list.append(cls(parent, index))
        return tab_frame_list


class TabTreeMouseOver(ttk.Frame):
    def __init__(self,
                 client_tab_frame,
                 client_tab_tree):
        super().__init__(master=client_tab_frame)

        self.client_tab_frame = client_tab_frame
        self.client_tab_tree = client_tab_tree
        self.buttons_frame = ttk.Frame(self.client_tab_frame)
        self.client_tab_frame.bind('<Enter>', self.mouse_over)
        self.client_tab_frame.bind('<Leave>', self.mouse_leave)
        self.rowconfigure(0, weight=1, uniform='a')
        self.columnconfigure(0, weight=1, uniform='a')
        self.columnconfigure(1, weight=1, uniform='a')
        self.columnconfigure(2, weight=1, uniform='a')
        self.columnconfigure(3, weight=1, uniform='a')
        self.move_up_button = ttk.Button(self.buttons_frame,
                                         text="\u2B9D",
                                         width=5,
                                         command=self.move_up,
                                         bootstyle='info')

        self.move_down_button = ttk.Button(self.buttons_frame,
                                           text="\u2B9F",
                                           width=5,
                                           command=self.move_down,
                                           bootstyle='info')

        self.new_command_button = ttk.Button(self.buttons_frame,
                                             text="+",
                                             width=5,
                                             command=lambda: TabCommandDlg(self.client_tab_tree.tab_command_dict,
                                                                           self.insert_command,
                                                                           self.insert_another_command),
                                             bootstyle='success')
        self.del_command_button = ttk.Button(self.buttons_frame,
                                             text=u"\U0001F5D1",
                                             width=5,
                                             command=self.delete_command,
                                             bootstyle='danger')

        self.move_up_button.grid(row=0, column=0, sticky='nsew')
        self.move_down_button.grid(row=0, column=1, sticky='nsew')
        self.new_command_button.grid(row=0, column=2, sticky='nsew')
        self.del_command_button.grid(row=0, column=3, sticky='nsew')

        # Binding Scroll to widgets
        scroll_tags = self.move_up_button.bindtags() + ("scroll_frame_widgets",)
        self.move_up_button.bindtags(scroll_tags)
        self.new_command_button.bindtags(scroll_tags)
        self.del_command_button.bindtags(scroll_tags)
        self.move_down_button.bindtags(scroll_tags)
        self.bindtags(scroll_tags)

    @classmethod
    def from_client_tab_frame_list(cls, client_tab_frame_list, tab_tree_list):
        tt_mouse_over_list = list()
        for frame, tree in zip(client_tab_frame_list, tab_tree_list):
            tt_mouse_over_list.append(cls(frame, tree))
        # print(tt_mouse_over_list)
        return tt_mouse_over_list

    def move_up(self):
        rows = self.client_tab_tree.selection()
        for row in rows:
            self.client_tab_tree.move(row, "", self.client_tab_tree.index(row) - 1)

    def move_down(self):
        rows = self.client_tab_tree.selection()
        for row in reversed(rows):
            self.client_tab_tree.move(row, "", self.client_tab_tree.index(row) + 1)

    def delete_command(self):
        selected_items = self.client_tab_tree.selection()
        for command in selected_items:
            self.client_tab_tree.delete(command)

    def mouse_over(self, event):
        self.buttons_frame.grid(row=1, sticky='nsew')

    def mouse_leave(self, event):
        self.buttons_frame.grid_forget()

    def insert_command(self, window_instance, new_command):
        if new_command:
            self.client_tab_tree.insert(parent='', index=tk.END, values=new_command[0])
        window_instance.destroy()

    def insert_another_command(self, new_command):
        if new_command:
            self.client_tab_tree.insert(parent='', index=tk.END, values=new_command[0])
