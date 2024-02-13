import tkinter as tk
from tkinter import ttk
from Tree_Widgets import TabBarTree


class ClientDragManager:
    def __init__(self, m_update_size_new_item, target_frame):
        self.move_left_button = None
        self.new_button = None
        self.delete_button = None
        self.move_right_button = None
        self.button_frame = None
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
                self.button_frame = ttk.Frame(client_frame)
                self.button_frame.rowconfigure(0, weight=1, uniform='a')
                self.button_frame.columnconfigure(0, weight=1, uniform='a')
                self.button_frame.columnconfigure(1, weight=1, uniform='a')
                self.button_frame.columnconfigure(2, weight=1, uniform='a')
                self.button_frame.columnconfigure(3, weight=1, uniform='a')
                button_width = 5
                self.move_left_button = ttk.Button(self.button_frame, text="\u2B9C", width=button_width)
                self.new_button = ttk.Button(self.button_frame, text="+", width=button_width)
                self.delete_button = ttk.Button(self.button_frame, text=u"\U0001F5D1", width=button_width)
                self.move_right_button = ttk.Button(self.button_frame, text="\u2B9E", width=button_width)
                self.move_left_button.grid(row=0, column=0)
                self.new_button.grid(row=0, column=1)
                self.delete_button.grid(row=0, column=2)
                self.move_right_button.grid(row=0, column=3)
                TabTreeMouseOver(self.button_frame, client_frame)
                tree.pack(expand=True, fill='both')
                tree_padx = 5
                tree_pady = 10
                client_frame.grid(row=self.tree_row, column=self.tree_col, padx=tree_padx, pady=tree_pady, sticky="nsew")
                client_frame.grid_propagate(False)
                target.update_idletasks()
                height = client_frame.winfo_height() * (self.tree_row + 1) + (((self.tree_row + 1) * 2) * tree_pady)
                self.m_update_size_new_item(height)
                self.tree_row, self.tree_col = self.update_row_column(self.tree_row,
                                                                      self.tree_col)
                self.tab_tree_index += 1
        self.tree_selection.clear()

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
    def __init__(self, button_frame, client_frame):
        self.button_frame = button_frame
        self.client_frame = client_frame
        self.client_frame.bind('<Enter>', self.mouse_over)
        self.client_frame.bind('<Leave>', self.mouse_leave)

    def mouse_over(self, event):
        # self.button_frame = ttk.Frame(self.frame)
        # self.button_frame.rowconfigure(0, weight=1, uniform='a')
        # self.button_frame.columnconfigure(0, weight=1, uniform='a')
        # self.button_frame.columnconfigure(1, weight=1, uniform='a')
        # self.button_frame.columnconfigure(2, weight=1, uniform='a')
        # self.button_frame.columnconfigure(3, weight=1, uniform='a')
        #
        # self.move_left_button = ttk.Button(self.button_frame, text="Move Left")
        # self.new_button = ttk.Button(self.button_frame, text="New")
        # self.delete_button = ttk.Button(self.button_frame, text="Delete")
        # self.move_right_button = ttk.Button(self.button_frame, text="Move Right")
        #
        # self.move_left_button.grid(row=0, column=0)
        # self.new_button.grid(row=0, column=1)
        # self.delete_button.grid(row=0, column=2)
        # self.move_right_button.grid(row=0, column=3)

        self.button_frame.pack(side="bottom")


    def mouse_leave(self, event):
        self.button_frame.pack_forget()
