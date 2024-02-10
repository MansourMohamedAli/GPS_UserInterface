import tkinter as tk
from tkinter import ttk
from Tree_Widgets import TabBarTree


class ClientDragManager:
    def __init__(self, m_update_size_new_item, target_frame):
        self.tree_row = 0
        self.tree_col = 0
        self.tab_tree_index = 1
        self.widget = None
        self.tree_selection = list()
        self.m_update_size_new_item = m_update_size_new_item
        self.target_frame = target_frame

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
                client_frame = ttk.Frame(target)
                tree = TabBarTree(client_frame, self.tab_tree_index, item)
                # print(f'Tab Tree Index {self.tab_tree_index}')
                tree.pack(expand=True, fill='both')
                tree_padx = 10
                tree_pady = 10
                client_frame.grid(row=self.tree_row, column=self.tree_col, padx=tree_padx, pady=tree_pady)
                target.update_idletasks()
                if self.tree_row == 0:
                    height = 340 + (2 * tree_pady)
                else:
                    height = client_frame.winfo_height() * (self.tree_row + 1) + (((self.tree_row + 1) * 2) * tree_pady)
                    print(self.tree_row)
                print(height)
                self.m_update_size_new_item(height)
                self.tree_row, self.tree_col = self.update_row_column(self.tree_row,
                                                                      self.tree_col)
                self.tab_tree_index += 1
        self.tree_selection.clear()

    @staticmethod
    def update_row_column(row, column):
        if column >= 2:
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
