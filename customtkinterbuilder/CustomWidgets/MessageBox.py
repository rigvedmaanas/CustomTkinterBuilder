from customtkinter import *

class MessageBox(CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.place_args = None
        self.place_kwargs = None
        self.fg_color = self.cget("fg_color")
        self.configure(fg_color="transparent")




    def disappear(self, frame):
        frame.destroy()
        if len(self.winfo_children()) == 0:
            self.configure(width=0, height=1, fg_color="transparent")



    def show(self, msg):
        frame = CTkFrame(self)
        frame.pack(pady=5)
        text = CTkLabel(frame, text=msg)
        text.pack(padx=5, pady=5)

        self.winfo_toplevel().after(2000, lambda text=text: self.disappear(frame))
