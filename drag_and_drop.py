import tkinter as tk
import ttkbootstrap as ttk
from Tree_Widgets import ClientTabFrame, TabBarTree, TabTreeMouseOver, ApplyToAllFrame
from logger import logger


class ClientDragManager:
    def __init__(self,
                 target_frame,
                 tab_trees_dict,
                 m_delete_client):

        self.widget = None
        self.tree_selection = list()
        self.target_frame = target_frame
        self.tab_trees_dict = tab_trees_dict
        self.m_delete_client = m_delete_client

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
                self.create_new(str(client))
        self.tree_selection.clear()

    def create_new(self, client):
        frame = ClientTabFrame(self.target_frame.scroll_frame, self.target_frame.client_tab_tree_index + 1)
        new_index = str(frame.index)
        new_dict = dict()
        new_list = list()
        tree = TabBarTree(frame, client, new_dict, new_list)
        self.tab_trees_dict[new_index] = {"client": client,
                                          "tree_commands": new_dict,
                                          "command_list": new_list}
        mouse_over = TabTreeMouseOver(frame, tree, self.m_delete_client)
        tree.grid(sticky='nsew')
        mouse_over.grid(sticky='nsew')
        row, column = self.target_frame.get_row_and_column(frame.index)
        self.target_frame.grid_tab_frame(frame, row, column)
        self.target_frame.update_scroll_height()
        self.target_frame.tab_tree_list.append(tree)


# class ApplyToAllFrame(ttk.Frame):
#     def __init__(self, master, style):
#         super().__init__(master=master, style=style)


class CommandDragManager:
    def __init__(self, commands_tree, apply_to_all_frame, client_tab_frame_list):
        self.widget = None
        self.tree_selection = list()
        self.commands_tree = commands_tree
        self.apply_to_all_frame = apply_to_all_frame
        self.client_tab_frame_list = client_tab_frame_list
        # Create a style object
        style = ttk.Style()
        # Configure the TFrame style (background color)
        style.configure("MyFrame.TFrame", background="#FFDDC1")
        # self.apply_to_all_frame = ttk.Frame(self.tab_frame, style="MyFrame.TFrame")
        # self.apply_to_all_frame = ApplyToAllFrame(self.tab_frame, style="MyFrame.TFrame")

    def add_dragable(self, widget):
        self.widget = widget
        widget.bind('<<TreeviewSelect>>', self.on_start)
        widget.bind("<B1-Motion>", self.on_drag)  # Todo
        widget.bind("<ButtonRelease-1>", self.on_drop)
        widget.configure(cursor="hand1")

    def on_start(self, event):
        for i in self.widget.selection():
            self.tree_selection.append(self.widget.item(i)['values'][0])
        # you could use this method to create a floating window
        # that represents what is being dragged.
        print("drag")
        # self.apply_to_all_frame.grid(row=0, columnspan=4, sticky='ew')
        # self.apply_to_all_frame.grid(row=0, rowspan=3, column=1, sticky='nsew')
        self.apply_to_all_frame.place(relx=0.4, rely=0.9, relwidth=0.2, relheight=0.1)

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
        if isinstance(target, TabBarTree):
            for command_name in self.tree_selection:
                self.add_command(command_name, target)
        elif isinstance(target, ApplyToAllFrame):
            for command_name in self.tree_selection:
                for tree in self.client_tab_frame_list:
                    self.add_command(command_name, tree)
        self.apply_to_all_frame.place_forget()
        self.tree_selection.clear()

    def add_command(self, command_name, tree):
        command_name = str(command_name)
        tree.insert(parent='', index=tk.END, values=[command_name])
        # Commands Dictionary for matching command name
        command_value = self.commands_tree.command_dictionary[command_name]
        # Add command names and commands to two separate lists.
        tree.tab_command_dict[command_name] = command_value
        tree.command_list.append(command_name)
        logger.info(f'Adding {command_name} to {tree.client_name} tree.')
