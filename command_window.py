import tkinter as tk
from tkinter import ttk


class CommandWindow(tk.Toplevel):
    def __init__(self, tree_dictionary, m_insert_command, m_insert_another_command):
        super().__init__()
        self.tree_dictionary = tree_dictionary
        self.m_insert_command = m_insert_command
        self.m_insert_another_command = m_insert_another_command
        self.title('Command Configuration')
        self.geometry("500x200")
        self.resizable(False, False)

        # Frame for left text
        self.labels_frame = ttk.Frame(self)
        # Command Name Label
        self.command_name_label = ttk.Label(self.labels_frame, text="Command Name:")
        # Command Name Label
        self.command_text_label = ttk.Label(self.labels_frame, text="Command:")
        # Placing Labels
        self.command_name_label.place(relx=0.1, rely=0.1)
        self.command_text_label.place(relx=0.1, rely=0.30)
        # Frame for text entries
        self.text_frame = ttk.Frame(self)
        # Text box for commands
        self.command_name_entry = tk.Entry(self.text_frame, width=53)
        # Text box for commands
        self.command_text_box = tk.Text(self.text_frame, width=40, height=5)
        # Placing Text Boxes
        self.command_name_entry.place(relx=0, rely=0.1)
        self.command_text_box.place(relx=0, rely=0.30)

        # Button Frame
        self.buttons_frame = ttk.Frame(self)
        # Done button

        #
        self.done_button = ttk.Button(self.buttons_frame,
                                      text="Done",
                                      command=lambda: self.m_insert_command(self, self.append_command_dictionary()))
        # Add Another Button
        self.add_another_button = ttk.Button(self.buttons_frame,
                                             text="Add Another",
                                             command=lambda: self.m_insert_another_command(self.append_command_dictionary()))
        # Placing Buttons
        self.done_button.place(relx=0.125, rely=0)
        self.add_another_button.place(relx=0.45, rely=0)

        # Configuring Grid
        self.rowconfigure(0, weight=5)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # Placing frames in grid
        self.labels_frame.grid(row=0, column=0, rowspan=2, sticky='nsew')
        self.text_frame.grid(row=0, column=1, rowspan=2, sticky='nsew')
        self.buttons_frame.grid(row=1, column=1, sticky='nsew')

    def append_command_dictionary(self):
        # Get Command name from entry.
        command_name = self.command_name_entry.get()
        if command_name and command_name not in self.tree_dictionary:
            # Get Command from text box.
            command_text_box = self.command_text_box.get("1.0", "end-1c")
            # Add command to dictionary.
            self.tree_dictionary[command_name] = command_text_box
            print(self.tree_dictionary)
            print("Command Added")
            return command_name
        else:
            print("Command Already Exists")
            return None
