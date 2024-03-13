import tkinter as tk


class ClientDragManager:
    def __init__(self,
                 target_frame,
                 pack_trees,
                 clients_dictionary,
                 commands_dictionary):

        self.widget = None
        self.tree_selection = list()
        self.target_frame = target_frame
        self.pack_trees = pack_trees
        self.clients_dictionary = clients_dictionary
        self.commands_dictionary = commands_dictionary

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
                self.pack_trees([item, ], self.clients_dictionary, self.commands_dictionary, [None])
        self.tree_selection.clear()


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
                for item in self.tree_selection:
                    target.insert(parent='', index=tk.END, values=[item])
                    # Commands Dictionary for matching command name
                    command = self.commands_tree.command_dictionary[item]
                    # Add command names and commands to two separate lists.
                    # I want to allow duplicate commands so a dictionary wouldn't work.
                    target.command_names.append(item)
                    target.commands.append(command)
                    print(f'{target.command_names}')
                    print(f'{target.commands}')

        except:
            pass
        self.tree_selection.clear()
