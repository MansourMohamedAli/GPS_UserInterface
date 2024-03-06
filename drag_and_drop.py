import tkinter as tk


class ClientDragManager:
    def __init__(self,
                 target_frame,
                 tab_tree_index,
                 pack_trees,
                 clients_tree):

        self.tab_tree_index = tab_tree_index
        self.widget = None
        self.tree_selection = list()
        self.target_frame = target_frame
        self.pack_trees = pack_trees
        self.clients_tree = clients_tree

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
                ip_address, mac_address = self.clients_tree.client_dictionary[item]
                self.pack_trees([item, ], ip_address, mac_address)
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
                # for item in self.tree_selection:
                #     target.insert(parent='', index=tk.END, values=[item])
                #     # Commands Dictionary for matching command name
                #     command = self.commands_tree.command_dictionary[item]
                #     # Add commands as values to client key.
                #     target.commands.append(command)
                #     print(f'{target.headings}:{target.commands}')

                for item in self.tree_selection:
                    target.insert(parent='', index=tk.END, values=[item])
                    # Commands Dictionary for matching command name
                    command = self.commands_tree.command_dictionary[item]
                    # Add commands as values to client key.
                    target.commands.append(command)
                    # print(f'{target.headings}:{target.commands}')
                    print(item)
                    print(command)

                    target.tab_tree_dictionary[item] = command
                print(target.tab_tree_dictionary)
        except:
            pass
        self.tree_selection.clear()
