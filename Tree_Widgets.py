import tkinter as tk
from tkinter import ttk


class ClientListTree(ttk.Treeview):
    def __init__(self, parent, *args):
        super().__init__(master=parent, columns=args, show='headings')
        self.args = args
        self.parent = parent
        self.bind('<Delete>', self.delete_row)

    def delete_row(self, event):
        selected_items = self.selection()
        for item in selected_items:
            self.delete(item)


class CommandListTree(ttk.Treeview):
    def __init__(self, parent, *args):
        super().__init__(master=parent, columns=args, show='headings')
        self.args = args
        self.parent = parent
        self.bind('<Delete>', self.delete_row)

    def delete_row(self, event):
        selected_items = self.selection()
        for item in selected_items:
            self.delete(item)


class TabBarTree(ttk.Treeview):
    def __init__(self, parent, tab_tree_index, *args):
        # todo change "*args" argument to a list
        super().__init__(master=parent, columns=args, show='headings')
        self.args = args
        self.parent = parent
        self.get_tree_headings()
        self.bind('<Delete>', self.delete_row)
        self.tab_tree_index = tab_tree_index
        self.tree_name = "tab_tree"

        self.no_scroll_tags = self.bindtags()
        # Adding new tag for frame to allow scroll on TabTree and background.
        self.scroll_tags = self.bindtags() + ("scroll_frame_widgets",)
        self.bindtags(self.scroll_tags)

        self.bind('<<TreeviewSelect>>', self.on_row_click)

    def on_row_click(self, event):
        # get the column index being clicked
        col = self.identify_column(event.x)
        print(col)
        # get the column name of the clicked column
        # name = self.column(col, 'id')
        # if name == 'blankspace':
        #     # clear the selection
        #     self.selection_set()
        #     # disable default mouse click handler
        #     return 'break'

    # def disable_scroll(self, event):
    #     print("Scrolling disabled")
    #     self.bindtags(self.no_scroll_tags)
    #     print(self.bindtags)

    def get_tree_headings(self):
        for arg in self.args:
            self.heading(arg, text=str(arg))

    def delete_row(self, event):
        selected_items = self.selection()
        for item in selected_items:
            self.delete(item)
