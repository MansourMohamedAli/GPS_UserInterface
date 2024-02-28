from ctypes import CDLL, c_int, c_char_p
clibrary = CDLL("C:/Projects/Python/GPS_UserInterface/GlassPanel/SendCmd/SendCmdClient/debug/SendCmdClient.dll")


def send_command(client_name, command):
    send_cmd_func = clibrary.send_cmd
    send_cmd_func.argtypes = [c_char_p]
    send_cmd_func.restype = c_int
    command_string = f"{client_name},{command}"
    byte_string = command_string.encode('utf-8')  # convert to bytes
    command = c_char_p(byte_string)
    send_cmd_func(command)

