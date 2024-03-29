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
        self.minsize(200, 320)
        # self.maxsize(300, 300)

        # Widgets
        self.menu = Menu(self)

        # Run
        self.mainloop()


class Menu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.config_button = ttk.Button(self, text='Configuration', command=self.read_configuration)
        # create the grid
        self.columnconfigure(0, weight=1, uniform='a')
        config = self.load_active_config()
        commands = self.get_active_commands(config)
        clients = self.get_clients(config)
        buttons_list = CommandButtons.from_dictionary(self, self.tab_client_command_map(clients, commands))
        self.pack_buttons(buttons_list)
        self.config_button.grid(sticky='nsew', padx=5, pady=5)

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

    def load_active_config(self):
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

    @staticmethod
    def pack_buttons(buttons_list):
        for button in buttons_list:
            button.grid(sticky='nsew', padx=5, pady=5)


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
    def from_dictionary(cls, parent, tab_dict):
        buttons_list = list()
        for button_name, client_commands in tab_dict.items():
            button = cls(parent, button_name, client_commands[0], client_commands[1])
            buttons_list.append(button)
        return buttons_list


App('Glass Panel Control', (200, 200), 'darkly')
