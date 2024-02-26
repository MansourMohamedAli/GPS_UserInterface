from ctypes import CDLL, c_int, c_char_p
clibrary = CDLL("C:/Projects/Python/GPS_UserInterface/GlassPanel/SendCmd/SendCmdClient/debug/SendCmdClient.dll")

send_cmd_func = clibrary.send_cmd
send_cmd_func.argtypes = [c_int, c_char_p]
send_cmd_func.restype = c_int

command = c_char_p(b"10.0.0.132 notepad")
send_cmd_func(2, command)
