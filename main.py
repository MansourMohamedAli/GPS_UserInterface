import tkinter as tk
# from tkinter import ttk
from configuration import Configuration
from send_command import send_command
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
        self.minsize(200, 200)
        self.maxsize(300, 300)

        # Widgets
        self.menu = Menu(self)

        # Run
        self.mainloop()


class Menu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.menu_button_1 = ttk.Button(self, text='Button 1', command=lambda: send_command(ip_address, "dir"))
        self.menu_button_2 = ttk.Button(self, text='Button 2')
        self.menu_button_3 = ttk.Button(self, text='Button 3')
        self.menu_button_4 = ttk.Button(self, text='Button 4')
        self.menu_button_5 = ttk.Button(self, text='Button 5')
        self.menu_button_6 = ttk.Button(self, text='Button 6')
        self.config_button = ttk.Button(self, text='Configuration', command=self.read_configuration)

        # create the grid
        self.columnconfigure(0, weight=1, uniform='a')
        self.columnconfigure(1, weight=1, uniform='a')

        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=1, uniform='a')
        self.rowconfigure(2, weight=1, uniform='a')
        self.rowconfigure(3, weight=1, uniform='a')

        # place the widgets
        # self.menu_button_1.grid(row=0, column=0, sticky='nsew', columnspan=1, padx=(10, 5), pady=(10, 10))
        # self.menu_button_2.grid(row=0, column=1, sticky='nsew', columnspan=1, padx=(5, 10), pady=(10, 10))
        # self.menu_button_3.grid(row=1, column=0, sticky='nsew', columnspan=1, padx=(10, 5), pady=(10, 10))
        # self.menu_button_4.grid(row=1, column=1, sticky='nsew', columnspan=1, padx=(5, 10), pady=(10, 10))
        # self.menu_button_5.grid(row=2, column=0, sticky='nsew', columnspan=1, padx=(10, 5), pady=(10, 10))
        # self.menu_button_6.grid(row=2, column=1, sticky='nsew', columnspan=1, padx=(5, 10), pady=(10, 10))
        # self.config_button.grid(row=3, column=0, sticky='nsew', columnspan=2, padx=(5, 10), pady=(10, 10))

        config = self.load_active_config()
        commands = self.get_active_commands(config)
        clients = self.get_clients(config)
        buttons_list = CommandButtons.from_dictionary(self, self.tab_client_command_map(clients, commands))
        # print(buttons_list)
        self.pack_buttons(buttons_list)
        # print(buttons_list)
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

    def pack_buttons(self, buttons_list):
        for button in buttons_list:
            button.pack()


class CommandButtons(ttk.Button):
    """
    Buttons will be instantiated with client, and command info built in.
    """
    def __init__(self, parent, button_name, clients, commands):
        super().__init__(master=parent, text=button_name)
        self.clients = clients
        self.commands = commands

    @classmethod
    def from_dictionary(cls, parent, tab_dict):
        buttons_list = list()
        for button_name, client_commands in tab_dict.items():
            button = cls(parent, button_name, client_commands[0], client_commands[1])
            buttons_list.append(button)
        return buttons_list

App('Glass Panel Control', (200, 200), 'darkly')
