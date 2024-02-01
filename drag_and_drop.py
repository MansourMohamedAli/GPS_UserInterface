import tkinter as tk
from tkinter import ttk

class ClientDragManager:
    def __init__(self):
        self.command_name = None
        self.widget = None
        self.tree_selection = list()

    def add_dragable(self, widget):
        self.widget = widget
        widget.bind('<<TreeviewSelect>>', self.on_start)
        # widget.bind("<B1-Motion>", self.on_drag)
        widget.bind("<ButtonRelease-1>", self.on_drop)
        widget.configure(cursor="hand1")

    def on_start(self, event):
        for i in self.widget.selection():
            self.tree_selection.append(self.widget.item(i)['values'][0])

        # you could use this method to create a floating window
        # that represents what is being dragged.

    def on_drag(self, event):
        # you could use this method to move a floating window that
        # represents what you're dragging
        pass

    def on_drop(self, event):
        # find the widget under the cursor
        x, y = event.widget.winfo_pointerxy()
        target = event.widget.winfo_containing(x, y)
        try:
            if target.tree_name == "tab_tree":
                for item in self.tree_selection:
                    target.insert(parent='', index=tk.END, values=[item])
                print(self.tree_selection)
        except:
            pass
        self.tree_selection.clear()


class CommandDragManager:
    def __init__(self):
        self.command_name = None
        self.widget = None
        self.tree_selection = list()

    def add_dragable(self, widget):
        self.widget = widget
        widget.bind('<<TreeviewSelect>>', self.on_start)
        # widget.bind("<B1-Motion>", self.on_drag)
        widget.bind("<ButtonRelease-1>", self.on_drop)
        widget.configure(cursor="hand1")

    def on_start(self, event):
        for i in self.widget.selection():
            self.tree_selection.append(self.widget.item(i)['values'][0])

        # you could use this method to create a floating window
        # that represents what is being dragged.

    def on_drag(self, event):
        # you could use this method to move a floating window that
        # represents what you're dragging
        pass

    def on_drop(self, event):
        # find the widget under the cursor
        x, y = event.widget.winfo_pointerxy()
        target = event.widget.winfo_containing(x, y)
        try:
            if target.tree_name == "tab_tree":
                for item in self.tree_selection:
                    target.insert(parent='', index=tk.END, values=[item])
                print(self.tree_selection)
        except:
            pass
        self.tree_selection.clear()
