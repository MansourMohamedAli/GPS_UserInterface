import tkinter as tk
from tkinter import ttk


class NewTabWindow(tk.Toplevel):
    def __init__(self, m_insert_tab, m_insert_another_tab):
        super().__init__()
        self.title('New Tab Creation')
        self.geometry("500x75")
        self.resizable(False, False)

        # Frame for left text
        self.labels_frame = ttk.Frame(self)
        # Command Name Label
        self.tab_name_label = ttk.Label(self.labels_frame, text="Tab Name:")
        # Placing Labels
        self.tab_name_label.place(relx=0.1, rely=0.1)
        # Frame for text entries
        self.text_frame = ttk.Frame(self)
        # Text box for commands
        self.tab_name_entry = tk.Entry(self.text_frame, width=53)
        # Placing Text Boxes
        self.tab_name_entry.place(relx=0, rely=0.1)

        # Button Frame
        self.buttons_frame = ttk.Frame(self)
        # Done button

        #
        self.done_button = ttk.Button(self.buttons_frame,
                                      text="Done",
                                      command=lambda: m_insert_tab(self, self.tab_name_entry.get()))
        # Add Another Button
        self.add_another_button = ttk.Button(self.buttons_frame,
                                             text="Add Another",
                                             command=lambda: m_insert_another_tab(self.tab_name_entry.get()))
        # Placing Buttons
        self.done_button.place(relx=0.125, rely=0)
        self.add_another_button.place(relx=0.45, rely=0)

        # Configuring Grid
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # Placing frames in grid
        self.labels_frame.grid(row=0, column=0, rowspan=2, sticky='nsew')
        self.text_frame.grid(row=0, column=1, rowspan=2, sticky='nsew')
        self.buttons_frame.grid(row=1, column=1, sticky='nsew')