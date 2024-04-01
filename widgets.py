from customtkinter import CTkEntry, CTkButton, CTkLabel, CTkFrame, CTkFont, CTkImage
from PIL import Image
from PackArgs import PackArgs
"""
class Entry(CTkEntry, PackArgs):
    def __init__(self, *args, properties, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "ENTRY"
        self.properties = properties
        self.bind("<Button-1>", self.on_drag_start)
        self.bind("<B1-Motion>", self.on_drag_motion)
        self.configure(state="disabled")

    def on_drag_start(self, event):
        #self._drag_start_x = event.x
        #self._drag_start_y = event.y
        self.properties.destroy_children()
        self.properties.add_seperator("Properties")
        #self.properties.add_option("X", "SLIDER", "X", {"to": 500, "from": 0, "val": int(self.place_info()["x"]), "callback": lambda val: self.place(x=val, y=int(self.place_info()["y"]))})
        #self.properties.add_option("Y", "SLIDER", "Y", {"to": 500, "from": 0, "val": int(self.place_info()["y"]), "callback": lambda val: self.place(x=int(self.place_info()["x"]), y=val)})
        self.properties.add_option("Width", "SLIDER", "Width", {"to": 500, "from": 0, "val": int(self.cget("width")), "callback": lambda val: self.configure(width=val)})
        self.properties.add_option("Height", "SLIDER", "Height", {"to": 500, "from": 0, "val": int(self.cget("height")), "callback": lambda val: self.configure(height=val)})
        self.properties.add_option("Placeholder Text", "TEXT", "Text", {"val": self.cget("placeholder_text"), "callback": lambda val: (self.configure(state="normal"), self.configure(placeholder_text=val), self.configure(state="disabled"))})
        self.properties.add_option("Corner Radius", "SLIDER", "Corner Radius", {"to": 100, "from": 0, "val": self.cget("corner_radius"), "callback": lambda val: self.configure(corner_radius=int(val))})
        self.properties.add_option("Border Width", "SLIDER", "Border Width", {"to": 100, "from": 0, "val": self.cget("border_width"), "callback": lambda val: self.configure(border_width=int(val))})
        self.default()
        self.on_drag_motion(event)  # Some awkward problem



    def on_drag_motion(self, event):
        #x = self.winfo_x() - self._drag_start_x + event.x
        #y = self.winfo_y() - self._drag_start_y + event.y
        #self.properties.update_options("X", "SLIDER", {"val": int(x)})
        #self.properties.update_options("Y", "SLIDER", {"val": int(y)})
        self.properties.update_options("Width", "SLIDER", {"val": int(self.cget("width"))})
        self.properties.update_options("Height", "SLIDER", {"val": int(self.cget("height"))})
        self.properties.update_options("Placeholder Text", "TEXT", {"val": self.cget("placeholder_text")})
        self.properties.update_options("Corner Radius", "SLIDER", {"val": self.cget("corner_radius")})
        self.properties.update_options("Border Width", "SLIDER", {"val": self.cget("border_width")})


        #self.place(x=x, y=y)

"""