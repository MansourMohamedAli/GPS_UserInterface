from tkinter import *

############################################################
#
#                 Base Window Properties
#
############################################################
window = Tk()
"""Window Title (Not Visible)"""
window.title("GPS")
"""Setting Size"""
window.geometry("800x600")
"""Setting Color"""
window.configure(bg="#C8Ad7F")
"""Prevent resizing of X and Y"""
# window.resizable(False, False)
"""Remove Border"""
window.overrideredirect(False)


def exit_application():
    """Exit Button"""
    window.destroy()


"""Variables to store the mouse's initial position"""
start_x = 0
start_y = 0


def on_mouse_press(event):
    """Function to handle the mouse button press event"""
    global start_x, start_y
    start_x = event.x
    start_y = event.y


def on_mouse_motion(event):
    """Function to handle the mouse motion event"""
    x = window.winfo_x() + (event.x - start_x)
    y = window.winfo_y() + (event.y - start_y)
    window.geometry(f"+{x}+{y}")


"""Bind mouse button press and motion events to the window"""
window.bind("<ButtonPress-1>", on_mouse_press)
window.bind("<B1-Motion>", on_mouse_motion)

############################################################
#
#                     PAGE 1
#
############################################################
"""Initializing Frame Use same color as window."""
page1_frame = Frame(window, bg=window["bg"])
"""Show Page 1 and fill size of window"""
page1_frame.pack(fill="both", expand=True)





if __name__ == "__main__":
    window.mainloop()
