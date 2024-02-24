import tkinter as tk
from tkinter import ttk
from Tree_Widgets import TabBarTree
from math import floor
from command_window import CommandWindow


class ClientDragManager:
    def __init__(self, m_update_size_new_item, target_frame):
        self.tab_tree_index = 0
        self.widget = None
        self.tree_selection = list()
        self.m_update_size_new_item = m_update_size_new_item
        self.target_frame = target_frame
        self.tree_list = list()
        self.client_frame_list = list()

    def add_dragable(self, widget):
        self.widget = widget
        widget.bind('<<TreeviewSelect>>', self.on_start)
        # widget.bind("<B1-Motion>", self.on_drag) # todo
        widget.bind("<ButtonRelease-1>", self.on_drop)
        widget.configure(cursor="hand1")

    def on_start(self, event):
        for i in self.widget.selection():
            self.tree_selection.append(self.widget.item(i)['values'][0])
        # you could use this method to create a floating window
        # that represents what is being dragged.
        # todo

    def on_drag(self, event):
        # you could use this method to move a floating window that
        # represents what you're dragging
        # todo
        pass

    def on_drop(self, event):
        # find the widget under the cursor
        x, y = event.widget.winfo_pointerxy()
        target = event.widget.winfo_containing(x, y)
        if target == self.target_frame:
            for item in self.tree_selection:
                self.pack_trees(item)
                self.tab_tree_index += 1
        self.tree_selection.clear()

    def pack_trees(self, item):
        client_frame = ClientFrame(self.target_frame, self.tab_tree_index)
        tree = TabBarTree(client_frame, self.tab_tree_index, item)
        client_frame_row, client_frame_col = self.assign_row_column(tree, self.tab_tree_index)
        self.target_frame.rowconfigure(client_frame_row, minsize=260)
        tree.pack(expand=False, fill='both')
        TabTreeMouseOver(client_frame, self.client_frame_list, self.target_frame, tree, self.reduce_tab_tree_index)

        tree_pad_x = 5
        tree_pad_y = 0

        client_frame.grid(row=client_frame_row, column=client_frame_col,
                          padx=tree_pad_x,
                          pady=tree_pad_y,
                          sticky="nsew")

        self.target_frame.grid_propagate(False)
        self.target_frame.update_idletasks()
        height = client_frame.winfo_height() * client_frame_row + ((client_frame_row * 2) * tree_pad_y)
        self.m_update_size_new_item(height)
        self.tree_list.append(tree)
        self.client_frame_list.append(client_frame)

    @staticmethod
    def assign_row_column(tree, tree_index):
        tree.row = (floor(tree_index / 5)) + 1
        tree.column = (tree_index % 5) + 1
        return tree.row, tree.column

    def reduce_tab_tree_index(self):
        self.tab_tree_index -= 1


class ClientFrame(ttk.Frame):
    def __init__(self, parent, index):
        super().__init__(master=parent)
        self.index = index


class TabTreeMouseOver:
    def __init__(self, client_frame, client_frame_list, target_frame, client_tree, m_reduce_tab_tree_index):
        self.client_frame = client_frame
        self.target_frame = target_frame
        self.client_frame_list = client_frame_list
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
        self.re_sort(self.client_frame_list)
        self.unpack_client_frame()
        for client_frame in self.client_frame_list:
            row, column = self.get_row_and_column(client_frame.index)
            self.repack_client_frame(client_frame, row, column)

    def move_left(self):
        self.shift_index_down()
        self.re_sort(self.client_frame_list)
        self.unpack_client_frame()
        for client_frame in self.client_frame_list:
            row, column = self.get_row_and_column(client_frame.index)
            self.repack_client_frame(client_frame, row, column)

    def shift_index_up(self):
        if self.client_frame.index < self.client_frame_list[-1].index:  # Making sure frame is not last.
            for client_frame in self.client_frame_list:
                if client_frame.index == (self.client_frame.index + 1):  # One above
                    client_frame.index -= 1
            self.client_frame.index += 1

    def shift_index_down(self):
        for client_frame in self.client_frame_list:
            if client_frame.index == (self.client_frame.index - 1):  # One below
                client_frame.index += 1
        self.client_frame.index -= 1
        self.client_frame.index = max(self.client_frame.index, 0)  # Limit to 0

    def delete_client(self):
        self.unpack_client_frame()
        for index, client_frame in enumerate(self.client_frame_list):
            if client_frame.index == self.client_frame.index:
                del self.client_frame_list[index]

        for client_frame in self.client_frame_list:
            if client_frame.index > self.client_frame.index:
                client_frame.index -= 1

        self.re_sort(self.client_frame_list)
        for client_frame in self.client_frame_list:
            row, column = self.get_row_and_column(client_frame.index)
            self.repack_client_frame(client_frame, row, column)

        self.m_reduce_tab_tree_index()  # drop tab tree index by one so next client dragged and dropped doesn't skip
        # a number

    def unpack_client_frame(self):
        for frame in self.client_frame_list:
            frame.grid_forget()

    @staticmethod
    def get_row_and_column(client_frame_index):
        row = (floor(client_frame_index / 5)) + 1
        column = (client_frame_index % 5) + 1
        return row, column

    @staticmethod
    def re_sort(client_frame_list):
        return client_frame_list.sort(key=lambda x: x.index)

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


class CommandDragManager:
    def __init__(self):
        self.widget = None
        self.tree_selection = list()

    def add_dragable(self, widget):
        self.widget = widget
        widget.bind('<<TreeviewSelect>>', self.on_start)
        # widget.bind("<B1-Motion>", self.on_drag)  # Todo
        widget.bind("<ButtonRelease-1>", self.on_drop)
        widget.configure(cursor="hand1")

    def on_start(self, event):
        for i in self.widget.selection():
            self.tree_selection.append(self.widget.item(i)['values'][0])
        # you could use this method to create a floating window
        # that represents what is being dragged.
        # Todo

    def on_drag(self, event):
        # you could use this method to move a floating window that
        # represents what you're dragging
        # Todo
        pass

    def on_drop(self, event):
        # find the widget under the cursor
        x, y = event.widget.winfo_pointerxy()
        target = event.widget.winfo_containing(x, y)
        try:
            if target.tree_name == "tab_tree":
                for item in self.tree_selection:
                    target.insert(parent='', index=tk.END, values=[item])
        except:
            pass
        self.tree_selection.clear()
