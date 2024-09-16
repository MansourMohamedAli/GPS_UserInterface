import tkinter as tk
import ttkbootstrap as ttk
from logger import logger


class ClientDlg(tk.Toplevel):
    def __init__(self, client_dictionary, m_insert_client, m_insert_another_client, x, y, client_name=None):
        super().__init__()
        self.client_dictionary = client_dictionary
        self.m_insert_client = m_insert_client
        self.m_insert_another_client = m_insert_another_client
        # print(x, y)
        if client_name:
            self.client_name = str(client_name)
        else:
            self.client_name = client_name

        # Client
        self.client_frame = ttk.Frame(self)

        # IP
        self.ip_frame = ttk.Frame(self)

        # MAC
        self.mac_frame = ttk.Frame(self)

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

        if self.client_name:
            v = tk.StringVar(value=self.client_name)
            self.client_name_entry = tk.Entry(self.client_frame,
                                              width=53,
                                              state="disabled",
                                              textvariable=v)

            self.client_name_entry.insert(tk.END, self.client_name)

            ip, mac = self.client_dictionary[self.client_name]

            self.ip_entry = tk.Entry(self.ip_frame, width=53, textvariable=tk.StringVar(value=ip))
            self.mac_entry = tk.Entry(self.mac_frame, width=53, textvariable=tk.StringVar(value=mac))
            self.done_button.place(relx=0.5, rely=0.25)
        else:
            # Text box for commands
            self.client_name_entry = tk.Entry(self.client_frame, width=53)
            self.ip_entry = tk.Entry(self.ip_frame, width=53)
            self.mac_entry = tk.Entry(self.mac_frame, width=53)
            self.done_button.place(relx=0.32, rely=0.25)
            self.add_another_button.place(relx=0.58, rely=0.25)

        self.title('Client Configuration')
        width, height = self.get_dimensions()
        self.geometry(f'{int(width * 0.30)}x{int(height * 0.15)}+{x}+{y}')
        self.minsize(int(width * 0.25), int(height * 0.10))
        self.maxsize(int(width * 0.35), int(height * 0.25))
        self.resizable(False, False)

        self.client_name_label = ttk.Label(self.client_frame, text="Client Name:")
        self.client_name_label.place(relx=0.1, rely=0.5)
        self.client_name_entry.place(relx=0.30, rely=0.5)

        # IP
        self.ip_label = ttk.Label(self.ip_frame, text="IP Address:")

        self.ip_label.place(relx=0.1, rely=0.5)
        self.ip_entry.place(relx=0.30, rely=0.5)

        # MAC
        self.mac_label = ttk.Label(self.mac_frame, text="MAC Address:")

        self.mac_label.place(relx=0.1, rely=0.5)
        self.mac_entry.place(relx=0.30, rely=0.5)

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
        if self.client_name:  # edit command
            ip_address = self.ip_entry.get()
            mac_address = self.mac_entry.get()
            self.client_dictionary[self.client_name] = ip_address, mac_address
        else:
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

    def get_dimensions(self):
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        return width, height


class CommandDlg(tk.Toplevel):
    def __init__(self, command_dict, m_insert_command, m_insert_another_command, x, y, tree_type,
                 tab_tree_list=None, tabs_list=None, command_list=None, command_name=None):
        super().__init__()
        self.command_dict = command_dict
        self.tab_tree_list = tab_tree_list
        self.command_list = command_list
        self.tabs_list = tabs_list
        self.m_insert_command = m_insert_command
        self.m_insert_another_command = m_insert_another_command
        self.tree_type = tree_type
        if command_name:
            self.command_name = str(command_name)
        else:
            self.command_name = command_name
        self.title('Command Configuration')
        width, height = self.get_dimensions()
        self.geometry(f'{int(width * 0.40)}x{int(height * 0.30)}+{x}+{y}')
        self.minsize(int(width * 0.25), int(height * 0.10))
        self.maxsize(int(width * 0.35), int(height * 0.25))
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
        # Button Frame
        self.buttons_frame = ttk.Frame(self)
        # Tab Command
        self.done_button = ttk.Button(self.buttons_frame,
                                      text="Done",
                                      command=lambda: self.m_insert_command(self, self.update_dictionary()))

        if self.command_name:
            v = tk.StringVar(value=self.command_name)
            self.command_name_entry = tk.Entry(self.text_frame,
                                               width=53,
                                               state="disabled",
                                               textvariable=v)

            self.command_name_entry.insert(tk.END, self.command_name)
            self.commandText = self.command_dict[self.command_name]
            self.command_text_box.insert(1.0, self.commandText)
            self.done_button.place(relx=0.2, rely=0)
            if self.tree_type == "command":
                self.var1 = tk.IntVar()
                self.propagate_to_tab_option = ttk.Checkbutton(self.buttons_frame, text='Apply to All in Current Tab with Same Name.',
                                                        variable=self.var1,
                                                        onvalue=1,
                                                        offvalue=0)
                self.propagate_to_tab_option.state(["!selected"])
                self.propagate_to_tab_option.place(relx=0.4, rely=0)

                self.var2 = tk.IntVar()
                self.propagate_to_all_option = ttk.Checkbutton(self.buttons_frame, text='Apply to All with Same Name.',
                                                        variable=self.var2,
                                                        onvalue=1,
                                                        offvalue=0)
                self.propagate_to_all_option.state(["!selected"])
                self.propagate_to_all_option.place(relx=0.4, rely=0.5)
        else:
            self.add_another_button = ttk.Button(self.buttons_frame,
                                                 text="Add Another",
                                                 command=lambda: self.m_insert_another_command(
                                                     self.update_dictionary()))

            self.command_name_entry = tk.Entry(self.text_frame, width=53)
            self.done_button.place(relx=0.125, rely=0)
            self.add_another_button.place(relx=0.45, rely=0)

        # Placing Text Boxes
        self.command_name_entry.place(relx=0, rely=0.1)
        self.command_text_box.place(relx=0, rely=0.30)

        # Configuring Grid
        self.rowconfigure(0, weight=5)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # Placing frames in grid
        self.labels_frame.grid(row=0, column=0, rowspan=2, sticky='nsew')
        self.text_frame.grid(row=0, column=1, rowspan=2, sticky='nsew')
        self.buttons_frame.grid(row=1, column=1, sticky='nsew')

    def update_dictionary(self):
        command_text_box = self.command_text_box.get("1.0", "end-1c")
        if self.command_name:  # edit command
            self.command_dict[self.command_name] = command_text_box
            if self.tree_type == "command":
                if 'selected' in self.propagate_to_all_option.state():
                    for tab in self.tabs_list:
                        for tree in tab.tab_tree_list:
                            if self.command_name in tree.tab_command_dict:
                                logger.info(f'{self.command_name} is in the {tree.client_name} tab tree.')
                                tree.tab_command_dict[self.command_name] = command_text_box
                elif 'selected' in self.propagate_to_tab_option.state():
                    for tree in self.tab_tree_list:
                        if self.command_name in tree.tab_command_dict:
                            logger.info(f'{self.command_name} is in the {tree.client_name} tab tree.')
                            tree.tab_command_dict[self.command_name] = command_text_box
        else:  # NEW
            self.command_name = str(self.command_name_entry.get())
            # Add command to dictionary.
            if self.tree_type == "command":
                if self.command_name not in self.command_dict:
                    self.command_dict[self.command_name] = command_text_box
                    return self.command_name
                else:
                    logger.info(f'{self.command_name} is already in dictionary.')
            elif self.tree_type == "tab":
                # todo let user know that this will add command name but overwrite all commands with same name.
                # todo Putting redundant code here for until todo is addressed.
                self.command_dict[self.command_name] = command_text_box
                self.command_list.append(self.command_name)
                return self.command_name

    def get_dimensions(self):
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        return width, height


class NewTabWindow(tk.Toplevel):
    def __init__(self, m_insert_tab, m_insert_another_tab):
        super().__init__()
        self.title('New Tab Creation')
        width, height = self.get_dimensions()
        self.geometry(f'{int(width * 0.30)}x{int(height * 0.05)}')
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

        # done button
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

    def get_dimensions(self):
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        return width, height


class RenameTabWindow(tk.Toplevel):
    def __init__(self, tabs_nb, tab_id, tabs_info):
        super().__init__()
        self.title('Rename Tab')
        width, height = self.get_dimensions()
        self.geometry(f'{int(width * 0.30)}x{int(height * 0.05)}')
        self.resizable(False, False)
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

    def get_dimensions(self):
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        return width, height


class NewConfigDlg(tk.Toplevel):
    def __init__(self, m_insert_config):
        super().__init__()
        self.title('New Configuration Creation')
        width, height = self.get_dimensions()
        self.geometry(f'{int(width * 0.30)}x{int(height * 0.05)}')
        self.resizable(False, False)

        # Frame for left text
        self.labels_frame = ttk.Frame(self)
        # Command Name Label
        self.config_name_label = ttk.Label(self.labels_frame, text="Configuration Name:")
        # Placing Labels
        self.config_name_label.place(relx=0.1, rely=0.1)
        # Frame for text entries
        self.text_frame = ttk.Frame(self)
        # Text box for commands
        self.config_name_entry = tk.Entry(self.text_frame, width=53)
        # Placing Text Boxes
        self.config_name_entry.place(relx=0, rely=0.1)

        # Button Frame
        self.buttons_frame = ttk.Frame(self)
        # Done button

        #
        self.done_button = ttk.Button(self.buttons_frame,
                                      text="Done",
                                      command=lambda: m_insert_config(self, self.config_name_entry.get()))
        # Placing Buttons
        self.done_button.place(relx=0.125, rely=0)

        # Configuring Grid
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # Placing frames in grid
        self.labels_frame.grid(row=0, column=0, rowspan=2, sticky='nsew')
        self.text_frame.grid(row=0, column=1, rowspan=2, sticky='nsew')
        self.buttons_frame.grid(row=1, column=1, sticky='nsew')

    def get_dimensions(self):
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        return width, height
