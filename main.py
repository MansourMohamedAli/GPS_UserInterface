import tkinter as tk
from configuration import ConfigurationManager
from send_command import send_cmd_client
from send_local_command import send_local_cmd
import socket
import json
import ttkbootstrap as ttk

host = socket.gethostname()
ip_address = socket.gethostbyname(host)


class App(ttk.Window):
    config_names = list()
    active_config_name = None

    def __init__(self, title, theme):
        # main setup
        super().__init__(themename=theme)
        self.title(title)
        x, y = self.get_dimensions()
        self.geometry(f'{int(x * 0.25)}x{int(y * 0.35)}')
        self.minsize(int(x * 0.10), int(y * 0.15))
        self.maxsize(int(x * 0.35), int(y * 0.45))
        # self.resizable(False, False)
        self.configurations = self.load_data()
        App.config_names = list(self.configurations['configurations'].keys())
        App.active_config_name = self.configurations['active_config']
        active_config_data = self.configurations['configurations'][App.active_config_name]

        # Widgets
        self.menu = Menu.from_active_config_data(self, active_config_data, self.config_selected)

        window_menu = WindowMenu()
        self.configure(menu=window_menu)
        # Run
        self.mainloop()

    def get_dimensions(self):
        x = self.winfo_screenwidth()
        y = self.winfo_screenheight()
        return x, y

    def get_tab_name(self):
        pass

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
            buttons_info = selected_config_data['tabs_info']
            # Destroying old config window
            self.menu.destroy()
            # Loading Configuration with new configuration data
            self.menu = Menu(self, buttons_info, self.config_selected)

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


class WindowMenu(ttk.Menu):
    def __init__(self):
        super().__init__()
        # sub menu
        file_menu = ttk.Menu(self, tearoff=False)
        file_menu.add_command(label='New', command=lambda: print('New file'))
        file_menu.add_command(label='Open', command=lambda: print('Open file'))
        self.add_cascade(label='File', menu=file_menu)

        # another sub menu
        help_menu = ttk.Menu(self, tearoff=False)
        help_menu.add_command(label='Help entry', command=lambda: print("test"))
        self.add_cascade(label='Help', menu=help_menu)


class Menu(ttk.Frame):
    def __init__(self, parent, buttons_info, client_dict, m_config_selected):
        super().__init__(parent)
        # widget data
        # self.tab_dict = tab_dict
        # item_number = len(tab_dict) + 2  # Plus two for configuration button and dropdown menu
        item_number = len(buttons_info) + 2  # Plus two for configuration button and dropdown menu
        self.buttons_info = buttons_info
        self.client_dict = client_dict
        self.list_height = item_number * 39
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

    @classmethod
    def from_active_config_data(cls, parent, active_config_data, m_config_selected):
        buttons_info = active_config_data['tabs_info']
        client_dict = active_config_data["clients"]
        return cls(parent, buttons_info, client_dict, m_config_selected)

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
        button_frames_list = CommandButtons.from_buttons_info(self.buttons_info, self.client_dict, frame)
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

    def __init__(self, parent, button_name, client_ip_list, client_mac_list, command_name_lists, commands_dict):
        super().__init__(master=parent, text=button_name)
        self.client_ip_list = client_ip_list
        self.client_mac_list = client_mac_list
        self.commands_dict = commands_dict
        self.command_name_lists = command_name_lists
        self.command_list = list()
        self.client_list = list()
        self.create_commands_list()
        self.bind('<ButtonPress-1>', self.send_cmd)

    def send_cmd(self, event):
        for ip, command in zip(self.client_list, self.command_list):
            if ip == "local":
                send_local_cmd(command)
                print("sending local command:", command)
            else:
                send_cmd_client(ip, command)
                print("sending Remote command to: ", ip, command)

    def create_commands_list(self):
        for index, (client, command_name_list) in enumerate(zip(self.client_ip_list, self.command_name_lists)):
            for command_name in command_name_list:
                self.client_list.append(client)
                self.command_list.append(self.commands_dict[index][command_name])

    @classmethod
    def from_buttons_info(cls, buttons_info, client_dict, menu_frame):
        button_frames_list = list()
        for button_name, tree_indices in buttons_info.items():
            button_frame = ttk.Frame(menu_frame)
            client_ip_list = list()
            client_mac_list = list()
            command_name_lists = list()
            commands_dict = list()
            for tree_index in tree_indices:
                tree_info = tree_indices[tree_index]
                client_ip_list.append(client_dict[tree_info['client']][0])
                client_mac_list.append(client_dict[tree_info['client']][1])
                command_name_lists.append(tree_info['command_list'])
                commands_dict.append(tree_info['tree_commands'])
            cls(button_frame, button_name, client_ip_list, client_mac_list, command_name_lists, commands_dict).pack(expand=True, fill="both")
            button_frames_list.append(button_frame)
        return button_frames_list


if __name__ == "__main__":
    App('Glass Panel Control', 'darkly')
