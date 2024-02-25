#from ctypes import CDLL, c_int, c_char_p
from ctypes import *
clibrary = CDLL("C:/Projects/Python/GPS_UserInterface/GlassPanel/SendCmd/SendCmdClient/debug/SendCmdClient.dll")

#func = clibrary.python_display_int_arg
#func.argtypes = [c_int, c_int]
#func.restype = c_int
#print(func(2, 7))

#func2 = clibrary.python_display_void_return
#func2.argtypes = [c_int, c_int]
#func2.restype = None
#func2(2, 5)

func2 = clibrary.main
func2.argtypes = [c_int, c_char_p]
func2.restype = c_int
print(func2(2, "Test"))

