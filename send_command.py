from ctypes import CDLL, c_int, c_char_p
import os

absolute_path = os.path.dirname(__file__)
relative_path = "GlassPanel\\SendCmd\\SendCmdClient\\Debug\\SendCmdClient.dll"
full_path = os.path.join(absolute_path, relative_path)
clibrary = CDLL(full_path, winmode=0)


def send_command(client_name, command):
    send_cmd_func = clibrary.send_cmd
    send_cmd_func.argtypes = [c_char_p]
    send_cmd_func.restype = c_int
    command_string = f"{client_name},{command}"
    byte_string = command_string.encode('utf-8')  # convert to bytes
    command = c_char_p(byte_string)
    send_cmd_func(command)
