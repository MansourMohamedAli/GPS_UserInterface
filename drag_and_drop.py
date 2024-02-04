import tkinter as tk
from tkinter import ttk
from Tree_Widgets import TabBarTree


class ClientDragManager:
    def __init__(self, m_update_size_new_item):
        self.tree_row = 0
        self.tree_col = 0
        self.widget = None
        self.tree_selection = list()
        self.m_update_size_new_item = m_update_size_new_item

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
        # item = TabBarTree(target, self.tree_index, self.tab_dict, f'{clients}')
        client_frame = ttk.Frame(target)
        tree = TabBarTree(client_frame, 0, f'test')
        tree.pack(expand=True, fill='both')

        client_frame.grid(row=self.tree_row, column=self.tree_col)

        # target.update_idletasks()

        if self.tree_row == 0:
            height = 340
        else:
            height = client_frame.winfo_height() * (self.tree_row + 1)
        self.tree_row, self.tree_col = self.update_row_column(self.tree_row,
                                                              self.tree_col)

    @staticmethod
    def update_row_column(row, column):
        if column >= 4:
            row += 1
            column = 0
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
