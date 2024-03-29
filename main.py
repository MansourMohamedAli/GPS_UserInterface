import tkinter as tk
from configuration import Configuration
from send_command import SendCMDClient
import socket
import json
import ttkbootstrap as ttk

host = socket.gethostname()
ip_address = socket.gethostbyname(host)


class App(ttk.Window):
    def __init__(self, title, dimensions, theme):
        # main setup
        super().__init__(themename=theme)
        self.title(title)
        self.geometry(f"{dimensions[0]}x{dimensions[1]}")
        self.minsize(200, 50)
        # self.resizable(False, False)
        # self.maxsize(300, 300)

        config = self.load_active_config()
        commands = self.get_active_commands(config)
        clients = self.get_clients(config)
        tab_dict = self.tab_client_command_map(clients, commands)

        # Widgets
        self.menu = Menu(self, tab_dict, 39)
        # Run
        self.mainloop()

    @staticmethod
    def read_configuration():
        try:
            with open('commandconfig.json') as f:
                json_data = json.load(f)
            Configuration.from_json(json_data)
        except FileNotFoundError as e:
            print(e)
        except json.decoder.JSONDecodeError as e:
            print(e)

    @staticmethod
    def load_active_config():
        try:
            with open('commandconfig.json') as f:
                json_data = json.load(f)
                active_config_name = (json_data['active_config'])
                active_config = json_data["configurations"][active_config_name]
                return active_config

        except FileNotFoundError as e:
            print(e)
        except json.decoder.JSONDecodeError as e:
            print(e)

    @staticmethod
    def get_active_commands(active_config):
        return active_config['tab_commands']

    @staticmethod
    def get_clients(active_config):
        return active_config['tab_clients']

    @staticmethod
    def tab_client_command_map(tab_clients, tab_commands):
        tab_dict = dict()
        for tab_index, (tab_name, client_list) in enumerate(tab_clients.items()):
            clients_in_tab = list()
            commands_in_tab = list()
            for i, client in enumerate(client_list):
                command_kv = tab_commands[str(tab_index + 1)][i]
                commands_list = list()
                for pair in command_kv:
                    commands_list.append(pair[1])
                commands_in_tab.append(commands_list)
                clients_in_tab.append(client)
            tab_dict[tab_name] = [clients_in_tab, commands_in_tab]
        return tab_dict


class Menu(ttk.Frame):
    def __init__(self, parent, tab_dict, item_height):
        super().__init__(parent)
        # widget data
        self.tab_dict = tab_dict
        item_number = len(tab_dict)
        self.list_height = item_number * item_height

        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.config_button = ttk.Button(self, text='Configuration')
        self.columnconfigure(0, weight=1, uniform='a')

        # canvas
        self.canvas = tk.Canvas(self, background='red', scrollregion=(0, 0, self.winfo_width(), self.list_height))
        self.canvas.pack(expand=True, fill='both')

        # display frame
        self.frame = ttk.Frame(self)
        # self.frame.columnconfigure()
        self.create_item().pack(expand=True, fill='both', pady=5, padx=5)

        # scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')

        # events
        self.canvas.bind_all('<MouseWheel>', lambda event: self.canvas.yview_scroll(-int(event.delta / 60), "units"))
        self.bind('<Configure>', self.update_size)

    def update_size(self, event):
        if self.list_height >= self.winfo_height():
            height = self.list_height
            self.canvas.bind_all('<MouseWheel>',
                                 lambda event: self.canvas.yview_scroll(-int(event.delta / 60), "units"))
            self.scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
        else:
            height = self.winfo_height()
            self.canvas.unbind_all('<MouseWheel>')
            self.scrollbar.place_forget()

        self.canvas.create_window(
            (0, 0),
            window=self.frame,
            anchor='nw',
            width=self.winfo_width(),
            height=height)

    def create_item(self):
        frame = ttk.Frame(self.frame)
        # grid layout
        frame.columnconfigure(0, weight=1)
        button_frames_list = CommandButtons.from_dictionary(self.tab_dict, frame)
        self.grid_button_frames(button_frames_list)
        return frame

    @staticmethod
    def grid_button_frames(button_frames_list):
        for button in button_frames_list:
            button.grid(sticky='nsew', padx=5, pady=5)

#f = Frame(master, height=32, width=32)
#f.pack_propagate(0) # don't shrink
#f.pack()
#
#b = Button(f, text="Sure!")
#b.pack(fill=BOTH, expand=1)


class CommandButtons(ttk.Button):
    """
    Buttons will be instantiated with client, and command info built in.
    """

    def __init__(self, parent, button_name, clients, commands):
        super().__init__(master=parent, text=button_name)
        self.clients = clients
        self.commands = commands
        self.bind('<ButtonPress-1>', self.send_cmd)

    def send_cmd(self, event):
        for client, commands in zip(self.clients, self.commands):
            for command in commands:
                SendCMDClient(ip_address, command)

    @classmethod
    def from_dictionary(cls, tab_dict, menu_frame):
        button_frames_list = list()
        for button_name, client_commands in tab_dict.items():
            button_frame = ttk.Frame(menu_frame)
            cls(button_frame, button_name, client_commands[0], client_commands[1]).pack(expand=True, fill="both")
            button_frames_list. append(button_frame)
        return button_frames_list


App('Glass Panel Control', (200, 290), 'darkly')
