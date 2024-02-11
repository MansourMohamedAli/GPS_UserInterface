import tkinter as tk
from tkinter import ttk


class ClientListTree(ttk.Treeview):
    def __init__(self, parent, *args):
        super().__init__(master=parent, columns=args, show='headings')
        self.args = args
        self.parent = parent
        self.get_tree_headings()
        self.bind('<Delete>', self.delete_row)

    def get_tree_headings(self):
        for arg in self.args:
            self.heading(arg, text=str(arg))

    def delete_row(self, event):
        selected_items = self.selection()
        for item in selected_items:
            self.delete(item)


class CommandListTree(ttk.Treeview):
    def __init__(self, parent, *args):
        super().__init__(master=parent, columns=args, show='headings')
        self.args = args
        self.parent = parent
        self.get_tree_headings()
        self.bind('<Delete>', self.delete_row)

    def get_tree_headings(self):
        for arg in self.args:
            self.heading(arg, text=str(arg))

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
        for arg in self.args:
            self.heading(arg, text=str(arg))

    def delete_row(self, event):
        selected_items = self.selection()
        for item in selected_items:
            self.delete(item)
