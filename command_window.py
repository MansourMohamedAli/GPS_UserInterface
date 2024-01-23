import tkinter as tk
from tkinter import ttk


class CommandWindow(tk.Toplevel):
    def __init__(self, m_insert_command, m_insert_another_command):
        super().__init__()
        self.title('Configuration')
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
                                      command=lambda: m_insert_command(self, self.command_name_entry.get()))
        # Add Another Button
        self.add_another_button = ttk.Button(self.buttons_frame,
                                             text="Add Another",
                                             command=lambda: m_insert_another_command(self.command_name_entry.get()))
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
