import tkinter as tk
from configuration import ConfigurationManager
from send_command import send_cmd_client
import socket
import json
import ttkbootstrap as ttk

host = socket.gethostname()
ip_address = socket.gethostbyname(host)


class App(ttk.Window):
    config_names = list()
    active_config_name = None

    def __init__(self, title, dimensions, theme):
        # main setup
        super().__init__(themename=theme)
        self.title(title)
        self.geometry(f"{dimensions[0]}x{dimensions[1]}")
        self.minsize(100, 100)
        # self.resizable(False, False)
        self.maxsize(400, 500)

        self.configurations = self.load_data()
        App.config_names = list(self.configurations['configurations'].keys())
        App.active_config_name = self.configurations['active_config']
        self.active_config_data = self.get_active_config(self.configurations)
        commands = self.get_active_commands(self.active_config_data)
        clients = self.get_clients(self.active_config_data)
        self.tab_dict = self.tab_client_command_map(clients, commands)

        # Widgets
        self.menu = Menu(self, self.tab_dict, 39, self.config_selected)
        # Run
        self.mainloop()

    def config_selected(self, config):
        selected_config = config.get()
        if selected_config == App.active_config_name:
            return
        else:
            # Setting new active config
            App.active_config_name = selected_config
            self.write_active_config()
            # Getting Config Data
            selected_config_data = self.configurations['configurations'][selected_config]
            # commands = selected_config_data['tab_commands']
            commands = self.get_active_commands(selected_config_data)
            # clients = self.get_clients(self.active_config_name)
            clients = self.get_clients(selected_config_data)
            self.tab_dict = self.tab_client_command_map(clients, commands)
            # Destroying old config window
            self.menu.destroy()
            # Loading Configuration with new configuration data
            self.menu = Menu(self, self.tab_dict, 39, self.config_selected)


    def write_active_config(self):
        self.configurations['active_config'] = self.active_config_name
        with open('commandconfig.json', 'w') as f:
            json.dump(self.configurations, f, indent=2)


    @staticmethod
    def load_data():
        try:
            with open('commandconfig.json') as f:
                return json.load(f)

        except FileNotFoundError as e:
            print(e)
        except json.decoder.JSONDecodeError as e:
            print(e)

    @staticmethod
    def get_active_config(data):
        active_config_name = data['active_config']
        return data["configurations"][active_config_name]

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
    def __init__(self, parent, tab_dict, item_height, m_config_selected):
        super().__init__(parent)
        # widget data
        self.tab_dict = tab_dict
        item_number = len(tab_dict) + 2  # Plus two for configuration button and dropdown menu
        self.list_height = item_number * item_height
        self.m_config_selected = m_config_selected
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.config_button = ttk.Button(self, text='Configuration')
        self.columnconfigure(0, weight=1, uniform='a')

        # canvas
        self.canvas = tk.Canvas(self, background='red', scrollregion=(0, 0, self.winfo_width(), self.list_height))
        self.canvas.pack(expand=True, fill='both')
        # display frame
        self.frame = ttk.Frame(self)

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
        self.drop_down_menu(frame)
        self.grid_button_frames(button_frames_list)

        # Creating configuration button and putting at bottom.
        self.configuration_button(frame)
        return frame

    def drop_down_menu(self, frame):
        # Configuration Dropdown
        drop_down_frame = ttk.Frame(frame)
        # Configuration Combobox.
        config_names = App.config_names
        c = ttk.StringVar(value=App.active_config_name)
        combo = ttk.Combobox(drop_down_frame, textvariable=c)
        combo['values'] = config_names
        combo['state'] = 'readonly'
        combo.pack(expand=True, fill='x', padx=5)
        combo.bind('<<ComboboxSelected>>', lambda event: self.m_config_selected(c))
        # pack combo frame:
        # drop_down_frame.pack(expand=True, fill='x')
        drop_down_frame.grid(sticky='nsew', pady=5)

    def configuration_button(self, frame):
        config_button_frame = ttk.Frame(frame)
        config_button = ttk.Button(config_button_frame, text='Configuration',
                                   command=lambda: self.read_configuration('commandconfig.json'))
        config_button.pack(expand=True, fill='both')
        config_button_frame.grid(sticky='nsew', pady=5)


    @staticmethod
    def read_configuration(configuration_filename):
        ConfigurationManager.from_json(configuration_filename)


    @staticmethod
    def grid_button_frames(button_frames_list):
        for button_frame in button_frames_list:
            button_frame.grid(sticky='nsew', pady=5)

    @staticmethod
    def grid_button_destroy(button_frames_list):
        for button_frame in button_frames_list:
            button_frame.destroy()


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
                send_cmd_client(ip_address, command)

    @classmethod
    def from_dictionary(cls, tab_dict, menu_frame):
        button_frames_list = list()
        for button_name, client_commands in tab_dict.items():
            button_frame = ttk.Frame(menu_frame)
            cls(button_frame, button_name, client_commands[0], client_commands[1]).pack(expand=True, fill="both")
            button_frames_list.append(button_frame)
        return button_frames_list


App('Glass Panel Control', (400, 500), 'darkly')
