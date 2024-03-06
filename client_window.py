import tkinter as tk
from tkinter import ttk


class ClientWindow(tk.Toplevel):
    def __init__(self, client_dictionary, m_insert_client, m_insert_another_client):
        super().__init__()
        self.client_dictionary = client_dictionary
        self.m_insert_client = m_insert_client
        self.m_insert_another_client = m_insert_another_client

        self.title('Client Configuration')
        self.geometry("500x200")
        self.resizable(False, False)

        # Client
        self.client_frame = ttk.Frame(self)
        self.client_name_label = ttk.Label(self.client_frame, text="Client Name:")
        self.client_name_entry = tk.Entry(self.client_frame, width=53)

        self.client_name_label.place(relx=0.1, rely=0.5)
        self.client_name_entry.place(relx=0.30, rely=0.5)

        # IP
        self.ip_frame = ttk.Frame(self)
        self.ip_label = ttk.Label(self.ip_frame, text="IP Address:")
        self.ip_entry = tk.Entry(self.ip_frame, width=53)

        self.ip_label.place(relx=0.1, rely=0.5)
        self.ip_entry.place(relx=0.30, rely=0.5)

        # MAC
        self.mac_frame = ttk.Frame(self)
        self.mac_label = ttk.Label(self.mac_frame, text="MAC Address:")
        self.mac_entry = tk.Entry(self.mac_frame, width=53)

        self.mac_label.place(relx=0.1, rely=0.5)
        self.mac_entry.place(relx=0.30, rely=0.5)

        # Buttons
        self.buttons_frame = ttk.Frame(self)
        self.done_button = ttk.Button(self.buttons_frame,
                                      text="Done",
                                      command=lambda: self.m_insert_client(self, self.append_client_dictionary()))
        # Add Another Button
        self.add_another_button = ttk.Button(self.buttons_frame,
                                             text="Add Another",
                                             command=lambda: self.m_insert_another_client(
                                                 self.append_client_dictionary()))
        self.done_button.place(relx=0.32, rely=0.25)
        self.add_another_button.place(relx=0.58, rely=0.25)

        # Configuring Grid
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)

        self.client_frame.grid(row=0, column=0, sticky='nsew')
        self.ip_frame.grid(row=1, column=0, sticky='nsew')
        self.mac_frame.grid(row=2, column=0, sticky='nsew')
        self.buttons_frame.grid(row=3, column=0, sticky='nsew')

    def append_client_dictionary(self):
        # Get Client name from entry.
        new_client = self.client_name_entry.get()
        if new_client:
            # Get IP and MAC addresses from entries.
            ip_address = self.ip_entry.get()
            mac_address = self.mac_entry.get()
            # Add client name and info to dictionary.
            self.client_dictionary[new_client] = ip_address, mac_address
            return new_client



