import Tkinter as tk

class Example(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        # add bindings to a new tag that we're going to be using
        self.bind_class("mytag", "<Enter>", self.on_enter)
        self.bind_class("mytag", "<Leave>", self.on_leave)

        # create some widgets and give them this tag
        for i in range(5):
            l = tk.Label(self, text="Button #%s" % i, background="white")
            l.pack(side="top")
            new_tags = l.bindtags() + ("mytag",)
            l.bindtags(new_tags)

    def on_enter(self, event):
        event.widget.configure(background="bisque")

    def on_leave(self, event):
        event.widget.configure(background="white")

if __name__ == "__main__":
    root = tk.Tk()
    view = Example()
    view.pack(side="top", fill="both", expand=True)
    root.mainloop()