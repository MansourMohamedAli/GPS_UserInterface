import tkinter as tk
from Tree_Widgets import ClientTabFrame, TabBarTree, TabTreeMouseOver


class ClientDragManager:
    def __init__(self,
                 target_frame):

        self.widget = None
        self.tree_selection = list()
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
        target_str = str(target)
        target_frame = str(self.target_frame) + ".!frame"
        if target_str == target_frame:
            for client in self.tree_selection:
                # self.create_new(self.target_frame, client, self.target_frame.client_tab_tree_index)
                self.create_new(client)
                # self.target_frame.pack_trees([item, ], [None], self.clients_dictionary)
        self.tree_selection.clear()

    def create_new(self, client):
        frame = ClientTabFrame(self.target_frame.scroll_frame, self.target_frame.client_tab_tree_index)
        tree = TabBarTree(frame, client)
        mouse_over = TabTreeMouseOver(frame, tree)
        tree.grid(sticky='nsew')
        mouse_over.grid(sticky='nsew')
        self.target_frame.grid_tab_frame(frame)


class CommandDragManager:
    def __init__(self, commands_tree):
        self.widget = None
        self.tree_selection = list()
        self.commands_tree = commands_tree

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
                print(self.tree_selection)
                for command_name in self.tree_selection:
                    print(command_name)
                    target.insert(parent='', index=tk.END, values=[command_name])

                    # Commands Dictionary for matching command name
                    command_value = self.commands_tree.command_dictionary[command_name]

                    # Add command names and commands to two separate lists.
                    # I want to allow duplicate commands so a dictionary wouldn't work.
                    # target.tab_command_dict.append([command_name, command_value])
                    target.tab_command_dict[command_name] = command_value
                    print(target.tab_command_dict)
        except AttributeError:
            pass
        self.tree_selection.clear()
