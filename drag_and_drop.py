import tkinter as tk
from tkinter import ttk
from Tree_Widgets import TabBarTree
from math import floor
import time


class ClientDragManager:
    def __init__(self, m_update_size_new_item, target_frame):
        self.move_left_button = None
        self.new_button = None
        self.delete_button = None
        self.move_right_button = None
        self.button_frame = None
        self.tree_row = 1
        self.tree_col = 1
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
                target.rowconfigure(self.tree_row, minsize=260)
                client_frame = ttk.Frame(target)
                tree = TabBarTree(client_frame, self.tab_tree_index, item)
                tree.pack(expand=False, fill='both')
                TabTreeMouseOver(tree, client_frame, self.tree_list, self.client_frame_list)
                tree_pad_x = 5
                tree_pad_y = 0
                client_frame.grid(row=self.tree_row, column=self.tree_col,
                                  padx=tree_pad_x,
                                  pady=tree_pad_y,
                                  sticky="nsew")
                target.grid_propagate(False)
                target.update_idletasks()
                height = client_frame.winfo_height() * self.tree_row + ((self.tree_row * 2) * tree_pad_y)
                self.m_update_size_new_item(height)
                self.tree_row, self.tree_col = self.update_row_column(self.tree_row,
                                                                      self.tree_col)
                self.tree_list.append(tree)
                self.client_frame_list.append(client_frame)
                self.tab_tree_index += 1
        self.tree_selection.clear()

    @staticmethod
    def update_row_column(row, column):
        if column >= 5:
            row += 1
            column = 1
        else:
            column += 1
        return row, column


class CommandDragManager:
    def __init__(self):
        self.widget = None
        self.tree_selection = list()

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
        try:
            if target.tree_name == "tab_tree":
                for item in self.tree_selection:
                    target.insert(parent='', index=tk.END, values=[item])
        except:
            pass
        self.tree_selection.clear()


class TabTreeMouseOver:
    def __init__(self, tree, client_frame, tree_list, client_frame_list):
        self.tree = tree
        self.client_frame = client_frame
        self.tree_list = tree_list
        self.client_frame_list = client_frame_list
        # self.scroll_tags = self.button_frame.bindtags() + ("scroll_frame_widgets",)
        # self.button_frame.bindtags(self.scroll_tags)
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
        self.new_button = ttk.Button(self.button_frame, text="+", width=5)
        self.delete_button = ttk.Button(self.button_frame, text=u"\U0001F5D1", width=5)
        self.move_right_button = ttk.Button(self.button_frame, text="\u2B9E", width=5)
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

    def move_left(self):
        print("Before Left Press")
        print(f'Clicked on {self.tree.args[0]}, tree index: {self.tree.tree_index}')

        for tree in self.tree_list:
            print(f'{tree.args[0]}, tree index: {tree.tree_index}')

        self.shift_index_down()
        self.re_sort(self.tree_list)

        print("\nAfter Left Press")
        for tree in self.tree_list:
            print(f'{tree.args[0]}, tree index: {tree.tree_index}')

        # self.unpack_tree()

    def unpack_tree(self):
        for frame in self.client_frame_list:
            frame.grid_forget()
        self.client_frame_list.clear()

    def shift_index_down(self):
        for item in self.tree_list:
            if (self.tree.tree_index - item.tree_index) == 1:  # one below
                item.tree_index += 1
        self.tree.tree_index -= 1
        self.tree.tree_index = max(self.tree.tree_index, 0)  # Limit to 0

    @staticmethod
    def shift_row_and_col_left(tree_index):
        row = (floor(tree_index / 5)) + 1
        column = (tree_index % 5) + 1
        # print(f'Tree Row:{row}, Tree Column:{column}')
        old_row = row
        old_col = column
        if row != 1:
            if column > 1:
                column -= 1
            elif column == 1:
                row -= 1
                column = 5
        elif column > 1:
            column -= 1
        return row, column

    @staticmethod
    def re_sort(tree_list):
        return tree_list.sort(key=lambda x: x.tree_index)

    def repack_trees(self):
        pass
