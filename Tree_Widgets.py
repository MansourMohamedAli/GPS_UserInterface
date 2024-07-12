import tkinter as tk
import ttkbootstrap as ttk
from add_button_dlg import CommandDlg


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
            del self.command_dictionary[str(command_name)]
            self.delete(command)


class TabBarTree(ttk.Treeview):
    def __init__(self, parent, client_name, tab_command_dict, command_list):
        super().__init__(master=parent, columns=client_name, show='headings', bootstyle='primary')
        self.client_name = client_name
        self.heading(client_name, text=str(client_name))
        # self.get_tree_headings()
        self.tree_name = "tab_tree"
        self.command_list = command_list
        self.tab_command_dict = tab_command_dict
        self.bind('<Delete>', self.delete_row_keyboard_button)
        self.tree_select = self.bindtags() + ("tree_select",)
        self.bindtags(self.tree_select)

        self.no_scroll_tags = self.bindtags()
        # Adding new tag for frame to allow scroll on TabTree and background.
        self.scroll_tags = self.bindtags() + ("scroll_frame_widgets",)
        self.bindtags(self.scroll_tags)
        self.scroll_state = True
        self.populate_tree()
        self.update_dict()

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
                tab_tree_list.append(cls(parent_frame, client_name, commands_dictionary, command_list))
        return tab_tree_list

    def enable_scroll(self):
        self.bindtags(self.scroll_tags)
        for item in self.selection():
            self.selection_remove(item)

    def disable_scroll(self):
        self.bindtags(self.no_scroll_tags)

    def delete_row_keyboard_button(self, event):
        self.delete_row()

    def delete_row(self):
        selected_items = self.selection()
        for command in selected_items:
            command_full_tree_info = self.item(command)
            self.delete(command)
        self.update_command_list()
        self.clean_dict()

    def update_command_list(self):
        """
        Clears list and repacks in order of tree widget children.
        """
        self.command_list.clear()
        for child in self.get_children():
            command_full_tree_info = self.item(child)
            command_name = command_full_tree_info['values'][0]
            self.command_list.append(str(command_name))

    def update_dict(self):
        """
        Re-ordering dictionary. Not necessary but it's nice to have dictionary
        in same order as command list (excluding repeat commands).
        """
        temp_dict = dict()
        for command in self.command_list:
            temp_dict[command] = self.tab_command_dict[command]
        self.tab_command_dict.clear()
        self.tab_command_dict.update(temp_dict)

    def clean_dict(self):
        """
        Clean up commands in command dictionary that aren't in the list
        """
        temp_dict = dict()
        for key, value in self.tab_command_dict.items():
            if key in self.command_list:
                temp_dict[key] = value
        self.tab_command_dict.clear()
        self.tab_command_dict.update(temp_dict)


class ClientTabFrame(ttk.Frame):
    def __init__(self, parent, index):
        super().__init__(master=parent)
        self.index = int(index)
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
                 client_tab_tree,
                 m_delete_client):
        super().__init__(master=client_tab_frame)

        self.client_tab_frame = client_tab_frame
        self.client_tab_tree = client_tab_tree
        self.m_delete_client = m_delete_client
        self.buttons_frame = ttk.Frame(self)
        self.client_tab_frame.bind('<Enter>', self.mouse_over)
        self.client_tab_frame.bind('<Leave>', self.mouse_leave)
        self.buttons_frame.rowconfigure(0, weight=1, uniform='a')
        self.buttons_frame.columnconfigure(0, weight=1, uniform='a')
        self.buttons_frame.columnconfigure(1, weight=1, uniform='a')
        self.buttons_frame.columnconfigure(2, weight=1, uniform='a')
        self.buttons_frame.columnconfigure(3, weight=1, uniform='a')
        self.buttons_frame.columnconfigure(4, weight=1, uniform='a')
        self.move_up_button = ttk.Button(self.buttons_frame,
                                         text="\u2B9D",
                                         width=5,
                                         command=self.move_up,
                                         bootstyle='info',
                                         state="enabled")

        self.move_down_button = ttk.Button(self.buttons_frame,
                                           text="\u2B9F",
                                           width=5,
                                           command=self.move_down,
                                           bootstyle='info',
                                           state="enabled")

        self.edit_command_button = ttk.Button(self.buttons_frame,
                                              text="Edit",
                                              width=5,
                                              command=self.edit_command,
                                              bootstyle='info',
                                              state="enabled")

        self.new_command_button = ttk.Button(self.buttons_frame,
                                             text="+",
                                             width=5,
                                             command=lambda: CommandDlg(self.client_tab_tree.tab_command_dict,
                                                                        self.insert_command,
                                                                        self.insert_another_command,
                                                                        "tab",
                                                                        command_list=self.client_tab_tree.command_list),
                                             bootstyle='info')

        self.del_command_button = ttk.Button(self.buttons_frame,
                                             text=u"\U0001F5D1",
                                             width=5,
                                             command=lambda: self.m_delete_client(self.client_tab_frame),
                                             bootstyle='danger')

        self.move_up_button.grid(row=0, column=0, sticky='nsew')
        self.move_down_button.grid(row=0, column=1, sticky='nsew')
        self.edit_command_button.grid(row=0, column=2, sticky='nsew')
        self.new_command_button.grid(row=0, column=3, sticky='nsew')
        self.del_command_button.grid(row=0, column=4, sticky='nsew')

        # Binding Scroll to widgets
        scroll_tags = self.move_up_button.bindtags() + ("scroll_frame_widgets",)
        self.move_up_button.bindtags(scroll_tags)
        self.new_command_button.bindtags(scroll_tags)
        self.del_command_button.bindtags(scroll_tags)
        self.move_down_button.bindtags(scroll_tags)
        self.edit_command_button.bindtags(scroll_tags)
        self.bindtags(scroll_tags)

    @classmethod
    def from_client_tab_frame_list(cls, client_tab_frame_list, tab_tree_list, m_delete_client):
        tt_mouse_over_list = list()
        for frame, tree in zip(client_tab_frame_list, tab_tree_list):
            tt_mouse_over_list.append(cls(frame, tree, m_delete_client))
        return tt_mouse_over_list

    def move_up(self):
        rows = self.client_tab_tree.selection()
        for row in rows:
            self.client_tab_tree.move(row, "", self.client_tab_tree.index(row) - 1)
        self.client_tab_tree.update_command_list()
        self.client_tab_tree.update_dict()

    def move_down(self):
        rows = self.client_tab_tree.selection()
        for row in reversed(rows):
            self.client_tab_tree.move(row, "", self.client_tab_tree.index(row) + 1)
        self.client_tab_tree.update_command_list()
        self.client_tab_tree.update_dict()

    def edit_command(self):
        tree_index = self.client_tab_tree.focus()
        if tree_index:
            command_name = self.client_tab_tree.item(tree_index)['values'][0]
            CommandDlg(self.client_tab_tree.tab_command_dict,
                       self.insert_command,
                       self.insert_another_command,
                       "tab",
                       command_list=self.client_tab_tree.command_list,
                       command_name=command_name)

    def mouse_over(self, event):
        self.buttons_frame.pack()

    def mouse_leave(self, event):
        self.buttons_frame.pack_forget()

    def insert_command(self, window_instance, new_command):
        if new_command:
            self.client_tab_tree.insert(parent='', index=tk.END, values=[new_command])
        window_instance.destroy()

    def insert_another_command(self, new_command):
        if new_command:
            self.client_tab_tree.insert(parent='', index=tk.END, values=[new_command])
