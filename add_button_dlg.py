import tkinter as tk
import ttkbootstrap as ttk


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
        if new_client and new_client not in self.client_dictionary:
            # Get IP and MAC addresses from entries.
            ip_address = self.ip_entry.get()
            mac_address = self.mac_entry.get()
            # Add client name and info to dictionary.
            self.client_dictionary[new_client] = ip_address, mac_address
            print("Client Added")
            return new_client
        else:
            print("Client Already Exists")
            return None


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
                                             command=lambda: self.m_insert_another_command(
                                                 self.append_command_dictionary()))
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


class TabCommandDlg(tk.Toplevel):
    def __init__(self, tab_command_dict, command_list, m_insert_command, m_insert_another_command, command_name=None):
        super().__init__()
        self.tab_command_dict = tab_command_dict
        self.command_list = command_list
        self.m_insert_command = m_insert_command
        self.m_insert_another_command = m_insert_another_command
        self.command_name = command_name
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
        self.command_text_box = tk.Text(self.text_frame, width=40, height=5)
        if command_name:
            v = tk.StringVar(value=command_name)
            self.command_name_entry = tk.Entry(self.text_frame,
                                               width=53,
                                               state="disabled",
                                               textvariable=v)

            self.command_name_entry.insert(tk.END, command_name)
            self.commandText = tab_command_dict[command_name]
            self.command_text_box.insert(1.0, self.commandText)
        else:
            # Text box for commands
            self.command_name_entry = tk.Entry(self.text_frame, width=53)
        # Placing Text Boxes
        self.command_name_entry.place(relx=0, rely=0.1)
        self.command_text_box.place(relx=0, rely=0.30)

        # Button Frame
        self.buttons_frame = ttk.Frame(self)
        # Done button

        #
        self.done_button = ttk.Button(self.buttons_frame,
                                      text="Done",
                                      command=lambda: self.m_insert_command(self, self.append_command_list()))
        # Add Another Button
        self.add_another_button = ttk.Button(self.buttons_frame,
                                             text="Add Another",
                                             command=lambda: self.m_insert_another_command(self.append_command_list()))
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

    def append_command_list(self):
        command_text_box = self.command_text_box.get("1.0", "end-1c")
        if self.command_name:
            self.tab_command_dict[self.command_name] = command_text_box
        else:
            # Get Command name from entry.
            command_name = self.command_name_entry.get()
            self.tab_command_dict[command_name] = command_text_box
            self.command_list.append(command_name)
            return [command_name, command_text_box]


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


class RenameTabWindow(tk.Toplevel):
    def __init__(self, tabs_nb, tab_id, tabs_info):
        super().__init__()
        self.title('Rename Tab')
        self.geometry("600x100")
        self.tabs_nb = tabs_nb
        self.tab_id = tab_id
        self.tabs_info = tabs_info

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
                                      command=lambda: self.rename_tab(self.tab_name_entry.get()))
        # Placing Buttons
        # self.done_button.pack(expand=True, fill='both')
        self.done_button.pack()
        # Configuring Grid
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(1, weight=3)

        self.labels_frame.grid(row=0, column=0, rowspan=1, sticky='nsew')
        self.text_frame.grid(row=0, column=1, rowspan=1, sticky='nsew')
        self.buttons_frame.grid(row=0, column=2, sticky='nsew')

    def rename_tab(self, entry):
        old_key = self.tabs_nb.tab(self.tab_id, 'text')
        if entry:
            self.tabs_nb.tab(self.tab_id, text=entry)
            self.tabs_info[entry] = self.tabs_info.pop(old_key)
            tab_names = [self.tabs_nb.tab(i, option="text") for i in self.tabs_nb.tabs()]
            temp_dict = dict()
            for tab in tab_names:
                temp_dict[tab] = self.tabs_info[tab]
            self.tabs_info.clear()
            for tab in tab_names:
                self.tabs_info[tab] = temp_dict[tab]
