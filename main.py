import tkinter as tk
from configuration import ConfigurationManager
from send_command import send_cmd_client
from send_local_command import send_local_cmd
import json
import ttkbootstrap as ttk
from logger import logger


class App(ttk.Window):
    def __init__(self,
                 title,
                 theme):
        # main setup
        super().__init__(themename=theme)
        self.combo = None
        self.active_config_data = None
        self.title(title)
        x, y = self.get_dimensions()
        self.minsize(int(x * 0.10), int(y * 0.30))
        self.maxsize(int(x * 0.35), int(y * 0.45))
        self.configurations = self.load_data()
        self.config_names = list(self.configurations['configurations'].keys())
        self.active_config_name = self.configurations['active_config']

        # Widgets
        self.main_frame = ttk.Frame(self)
        self.combo_frame = ttk.Frame(self.main_frame)
        self.combo = self.create_combo(self.combo_frame)
        self.combo.pack(expand=False, fill='x', padx=5, side="top")
        self.menu_frame = ttk.Frame(self.main_frame)

        self.output_frame = ttk.Frame(self.main_frame)

        # Create a style object
        style = ttk.Style()
        # Configure the style for TLabel
        style.configure("Custom.TLabel", background="#FFDDC1", foreground="black", anchor="center")
        self.output_label = ttk.Label(self.output_frame, text="Output Window", style="Custom.TLabel")
        self.output_label.pack(side="top", fill='x', padx=5)
        self.output_window = ttk.Text(master=self.output_frame, height=6, state='disabled')
        self.output_window.pack(expand=False, fill='x', padx=5, side="top")
        self.output_frame.pack(expand=False, fill='x', padx=5, pady=(20, 10), side="bottom")

        self.clear_output_button = ttk.Button(self.output_frame, text="Clear Output", command=self.clear_output)
        self.clear_output_button.pack(expand=True, side='bottom', fill='x', padx=5)

        # self.clear_button_frame = ttk.Frame(self.output_frame)
        # self.clear_output_button = ttk.Button(self.clear_button_frame, width=self.output_frame.winfo_width())
        # self.clear_output_button.pack(expand=True, fill='both')
        # self.clear_button_frame.pack(side="bottom", fill='x', padx=5)
        try:
            self.active_config_data = self.configurations['configurations'][self.active_config_name]
        except KeyError:
            self.active_config_name = self.config_names[0]
            self.active_config_data = self.configurations['configurations'][self.active_config_name]
            self.combo.set(self.active_config_name)

        self.menu = Menu.from_active_config_data(self.menu_frame,
                                                 self.active_config_name,
                                                 self.active_config_data,
                                                 self.config_selected,
                                                 self.reload_menu,
                                                 self.output_window)

        self.pack_widget_frames()

        window_menu = WindowMenu()

        self.configure(menu=window_menu)
        # Run
        self.mainloop()

    def clear_output(self):
        self.output_window.configure(state='normal')
        self.output_window.delete("1.0", tk.END)
        self.output_window.configure(state='disabled')

    def reload_menu(self):
        self.combo_frame.destroy()
        self.combo_frame = ttk.Frame(self.main_frame)
        self.configurations = self.load_data()
        self.config_names = list(self.configurations['configurations'].keys())
        self.active_config_name = self.configurations['active_config']
        try:
            self.active_config_data = self.configurations['configurations'][self.active_config_name]
        except KeyError:
            self.active_config_name = self.config_names[0]
            self.active_config_data = self.configurations['configurations'][self.active_config_name]
        self.combo = self.create_combo(self.combo_frame)
        self.combo.pack(expand=False, fill='x', padx=5, side="top")
        self.combo.set(self.active_config_name)
        self.menu_frame.destroy()
        self.menu_frame = ttk.Frame(self.main_frame)
        self.menu = Menu.from_active_config_data(self.menu_frame,
                                                 self.active_config_name,
                                                 self.active_config_data,
                                                 self.config_selected,
                                                 self.reload_menu,
                                                 self.output_window)
        self.pack_widget_frames()

        # Write Json again to capture active Config.
        self.write_active_config()

    def re_load_dropdown(self):
        self.combo_frame.destroy()
        self.combo_frame = ttk.Frame(self.main_frame)
        self.combo = self.create_combo(self.combo_frame)
        self.combo.pack(expand=False, fill='x', padx=5, side="top")
        self.pack_widget_frames()

    def pack_widget_frames(self):
        self.combo_frame.pack(expand=False, fill='both', side="top")
        self.menu_frame.pack(expand=False, fill='both', side="bottom")
        self.main_frame.pack(expand=False, fill='x', side='top')

    def create_combo(self, combo_frame):
        config_names = self.config_names
        c = ttk.StringVar(value=self.active_config_name)
        combo = ttk.Combobox(combo_frame, textvariable=c)
        combo['values'] = config_names
        combo['state'] = 'readonly'
        combo.bind('<<ComboboxSelected>>', lambda event: self.config_selected(c))
        return combo

    def get_dimensions(self):
        x = self.winfo_screenwidth()
        y = self.winfo_screenheight()
        return x, y

    def config_selected(self, config):
        selected_config = config.get()
        if selected_config == self.active_config_name:
            return
        else:
            # Setting new active config
            self.active_config_name = selected_config
            self.write_active_config()
            # Getting Config Data
            selected_config_data = self.configurations['configurations'][selected_config]
            # Destroying old config window
            self.menu.destroy()
            # Loading Configuration with new configuration data
            self.menu = Menu.from_active_config_data(self.menu_frame,
                                                     self.active_config_name,
                                                     selected_config_data,
                                                     self.config_selected,
                                                     self.reload_menu,
                                                     self.output_window)
            self.re_load_dropdown()

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
            logger.error(f'{e}')
        except json.decoder.JSONDecodeError as e:
            logger.error(f'{e}')

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
    def __init__(self, parent,
                 buttons_info,
                 client_dict,
                 active_config_name,
                 m_config_selected,
                 m_reload_menu,
                 output_window):
        super().__init__(parent)
        item_number = len(buttons_info) + 2  # Plus two for configuration button and dropdown menu
        self.buttons_info = buttons_info
        self.client_dict = client_dict
        self.active_config_name = active_config_name
        self.list_height = item_number * 39
        self.m_config_selected = m_config_selected
        self.m_reload_menu = m_reload_menu
        self.output_window = output_window
        self.pack(expand=True, fill="both")
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
    def from_active_config_data(cls, parent, active_config_name, active_config_data, m_config_selected, m_reload_menu, output_window):
        buttons_info = active_config_data['tabs_info']
        client_dict = active_config_data["clients"]
        return cls(parent, buttons_info, client_dict, active_config_name, m_config_selected, m_reload_menu, output_window)

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
        button_frames_list = CommandButtons.from_buttons_info(self.buttons_info, self.client_dict, frame, self.output_window)
        # self.drop_down_menu(frame)
        self.grid_button_frames(button_frames_list)

        # Creating configuration button and putting at bottom.
        self.configuration_button(frame)
        return frame

    def configuration_button(self, frame):
        config_button_frame = ttk.Frame(frame)
        config_button = ttk.Button(config_button_frame, text='Configuration',
                                   command=lambda: self.read_configuration('commandconfig.json'))
        config_button.pack(expand=True, fill='both')
        config_button_frame.grid(sticky='nsew', pady=5)

    def read_configuration(self, configuration_filename):
        ConfigurationManager.from_json(configuration_filename,self.active_config_name, self.m_reload_menu)

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

    def __init__(self, parent,
                 button_name,
                 client_ip_list,
                 client_mac_list,
                 command_name_lists,
                 commands_dict,
                 output_window):

        super().__init__(master=parent, text=button_name)
        self.client_ip_list = client_ip_list
        self.client_mac_list = client_mac_list
        self.commands_dict = commands_dict
        self.output_window = output_window
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
            output = f'{ip}: {command}\n'
            self.output_window.configure(state='normal')
            self.output_window.insert(tk.END, output)
            self.output_window.configure(state='disabled')

    def create_commands_list(self):
        for index, (client, command_name_list) in enumerate(zip(self.client_ip_list, self.command_name_lists)):
            for command_name in command_name_list:
                self.client_list.append(client)
                self.command_list.append(self.commands_dict[index][command_name])

    @classmethod
    def from_buttons_info(cls, buttons_info, client_dict, menu_frame, output_window):
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
            cls(button_frame, button_name, client_ip_list, client_mac_list, command_name_lists, commands_dict, output_window).pack(
                expand=True, fill="both")
            button_frames_list.append(button_frame)
        return button_frames_list


if __name__ == "__main__":
    App('Glass Panel Control', 'darkly')
