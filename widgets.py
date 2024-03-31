from customtkinter import CTkEntry, CTkButton, CTkLabel, CTkFrame


class PackArgs:
    def __init__(self):
        self.options = {}

    def set_options(self, val):
        self.options = val

    def redraw(self, **kwargs):
        self.pack_options = kwargs
        print(self.pack_options)
        self.pack_options.pop("in")

        self.properties.main.redraw(self.properties.main.widgets[self.properties.main.r])

    def default(self):
        self.properties.add_seperator("Layout (Pack)")

        self.properties.add_option("Fill", "COMBO", "Fill", {"vals": ["none", "x", "y", "both"], "default": str(self.pack_info()["fill"]), "callback": lambda val: self.redraw(fill=val, **{k: v for k, v in self.pack_info().items() if k != "fill"})})
        self.properties.add_option("Expand", "COMBO", "Expand", {"vals": ["false", "true"], "default": str(self.pack_info()["expand"]), "callback": lambda val: self.redraw(expand=val, **{k: v for k, v in self.pack_info().items() if k != "expand"})})
        self.properties.add_option("Side", "COMBO", "Side", {"vals": ["top", "bottom", "left", "right"], "default": str(self.pack_info()["side"]), "callback": lambda val: self.redraw(side=val, **{k: v for k, v in self.pack_info().items() if k != "side"})})

        if type(self.pack_info()["padx"]) == int:
            self.properties.add_option("Padx", "TUPLE", "Padx", {"to": 500, "from": 0, "val1": int(self.pack_info()["padx"]), "val2": int(self.pack_info()["padx"]), "callback": lambda val1, val2: self.redraw(padx=(val1, val2), **{k: v for k, v in self.pack_info().items() if k != "padx"})})

        else:
            self.properties.add_option("Padx", "TUPLE", "Padx", {"to": 500, "from": 0, "val1": int(self.pack_info()["padx"][0]), "val2": int(self.pack_info()["padx"][1]), "callback": lambda val1, val2: self.redraw(padx=(val1, val2), **{k: v for k, v in self.pack_info().items() if k != "padx"})})

        if type(self.pack_info()["pady"]) == int:
            self.properties.add_option("Pady", "TUPLE", "Pady", {"to": 500, "from": 0, "val1": int(self.pack_info()["pady"]), "val2": int(self.pack_info()["pady"]), "callback": lambda val1, val2: self.redraw(pady=(val1, val2), **{k: v for k, v in self.pack_info().items() if k != "pady"})})

        else:
            self.properties.add_option("Pady", "TUPLE", "Pady", {"to": 500, "from": 0, "val1": int(self.pack_info()["pady"][0]), "val2": int(self.pack_info()["pady"][1]), "callback": lambda val1, val2: self.redraw(pady=(val1, val2), **{k: v for k, v in self.pack_info().items() if k != "pady"})})

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



class Button(CTkButton, PackArgs):
    def __init__(self, *args, properties, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "BUTTON"
        self.properties = properties
        self.pack_options = {}
        self.pack_propagate(False)
        self.configure(bg_color=self.master.master.cget("fg_color"))
        self.bind("<Button-1>", self.on_drag_start)
        #self.bind("<B1-Motion>", self.on_drag_motion)
        self.props = {}

    def save(self, func, key, val, arg):
        self.props[key] = val
        func(arg)



    def on_drag_start(self, event):
        #self._drag_start_x = event.x
        #self._drag_start_y = event.y
        self.properties.destroy_children()
        self.properties.add_seperator("Properties")
        self.properties.add_option("Width", "SLIDER", "Width", {"to": 500, "from": 0, "val": int(self.cget("width")), "callback": lambda val: self.save(lambda val: self.configure(width=val), "width", val, val)})
        self.properties.add_option("Height", "SLIDER", "Height", {"to": 500, "from": 0, "val": int(self.cget("height")), "callback": lambda val: self.save(lambda val: self.configure(height=val), "height", val, val)})

        self.properties.add_option("Corner Radius", "SLIDER", "Corner Radius", {"to": 100, "from": 0, "val": self.cget("corner_radius"), "callback": lambda val: self.save(lambda val: self.configure(corner_radius=val), "corner_radius", int(val), int(val))})
        self.properties.add_option("Border Width", "SLIDER", "Border Width", {"to": 100, "from": 0, "val": self.cget("border_width"), "callback": lambda val: self.save(lambda val: self.configure(border_width=val), "border_width", int(val), int(val))})
        self.properties.add_option("FG Color", "COLOR_COMBO", "fg_color", {"color": self.cget("fg_color"), "key": "fg_color", "transparent": True, "callback": lambda val: self.save(lambda val: self.configure(fg_color=val), "fg_color", val, val)})
        self.properties.add_option("Border Color", "COLOR_COMBO", "border_color", {"color": self.cget("border_color"), "key": "border_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(border_color=val), "border_color", val, val)})
        self.properties.add_option("Hover Color", "COLOR_COMBO", "hover_color", {"color": self.cget("hover_color"), "key": "hover_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(hover_color=val), "hover_color", val, val)})
        self.properties.add_option("Text Color", "COLOR_COMBO", "text_color", {"color": self.cget("text_color"), "key": "text_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(text_color=val), "text_color", val, val)})

        self.properties.add_option("State", "COMBO", "state", {"vals": ["normal", "disabled"], "default": self.cget("state"), "callback": lambda val: self.save(lambda val: self.configure(state=val), "state", val, val)})

        self.default()
        self.on_drag_motion(event)  # Some awkward problem

    def on_drag_motion(self, event):
        #x = self.winfo_x() - self._drag_start_x + event.x
        #y = self.winfo_y() - self._drag_start_y + event.y
        #self.properties.update_options("X", "SLIDER", {"val": int(x)})
        #self.properties.update_options("Y", "SLIDER", {"val": int(y)})


        self.properties.update_options("Width", "SLIDER", {"val": int(self.cget("width"))})
        self.properties.update_options("Height", "SLIDER", {"val": int(self.cget("height"))})
        #self.properties.update_options("Text", "TEXT", {"val": self.cget("text")})
        self.properties.update_options("Corner Radius", "SLIDER", {"val": self.cget("corner_radius")})
        self.properties.update_options("Border Width", "SLIDER", {"val": self.cget("border_width")})

        #self.place(x=x, y=y)
class Label(CTkLabel, PackArgs):
    def __init__(self, *args, properties, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "LABEL"
        self.properties = properties
        self.configure(bg_color=self.master.master.cget("fg_color"))

        self.bind("<Button-1>", self.on_drag_start)

        #self.bind("<B1-Motion>", self.on_drag_motion)
        self.props = {}

    def save(self, func, key, val, arg):
        self.props[key] = val
        func(arg)

    def on_drag_start(self, event):
        #self._drag_start_x = event.x
        #self._drag_start_y = event.y
        self.properties.destroy_children()
        self.properties.add_seperator("Properties")
        #self.properties.add_option("X", "SLIDER", "X", {"to": 500, "from": 0, "val": int(self.place_info()["x"]), "callback": lambda val: self.place(x=val, y=int(self.place_info()["y"]))})
        #self.properties.add_option("Y", "SLIDER", "Y", {"to": 500, "from": 0, "val": int(self.place_info()["y"]), "callback": lambda val: self.place(x=int(self.place_info()["x"]), y=val)})
        self.properties.add_option("Width", "SLIDER", "Width", {"to": 500, "from": 0, "val": int(self.cget("width")), "callback": lambda val: self.save(lambda val: self.configure(width=val), "width", val, val)})
        self.properties.add_option("Height", "SLIDER", "Height", {"to": 500, "from": 0, "val": int(self.cget("height")), "callback": lambda val: self.save(lambda val: self.configure(height=val), "height", val, val)})
        self.properties.add_option("Text", "TEXT", "Text", {"val": self.cget("text"), "callback": lambda val: self.save(lambda val: self.configure(text=val), "text", val, val)})
        self.properties.add_option("Corner Radius", "SLIDER", "Corner Radius", {"to": 100, "from": 0, "val": self.cget("corner_radius"), "callback": lambda val: self.save(lambda val: self.configure(corner_radius=val), "corner_radius", val, val)})
        self.default()
        self.on_drag_motion(event)  # Some awkward problem



    def on_drag_motion(self, event):
        #x = self.winfo_x() - self._drag_start_x + event.x
        #y = self.winfo_y() - self._drag_start_y + event.y
        #self.properties.update_options("X", "SLIDER", {"val": int(x)})
        #self.properties.update_options("Y", "SLIDER", {"val": int(y)})
        self.properties.update_options("Width", "SLIDER", {"val": self.cget("width")})
        self.properties.update_options("Height", "SLIDER", {"val": self.cget("height")})
        self.properties.update_options("Text", "TEXT", {"val": self.cget("text")})
        self.properties.update_options("Corner Radius", "SLIDER", {"val": self.cget("corner_radius")})

        #self.place(x=x, y=y)


class Frame(CTkFrame, PackArgs):
    def __init__(self, *args, properties, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "FRAME"
        self.properties = properties
        self.pack_options = {}
        self.pack_propagate(False)
        self.configure(bg_color=self.master.master.cget("fg_color"))
        self.bind("<Button-1>", self.on_drag_start)
        #self.bind("<B1-Motion>", self.on_drag_motion)
        self.props = {}

    def save(self, func, key, val, arg):
        self.props[key] = val
        func(arg)



    def on_drag_start(self, event):
        #self._drag_start_x = event.x
        #self._drag_start_y = event.y
        self.properties.destroy_children()
        self.properties.add_seperator("Properties")
        self.properties.add_option("Width", "SLIDER", "Width", {"to": 500, "from": 0, "val": int(self.cget("width")), "callback": lambda val: self.save(lambda val: self.configure(width=val), "width", val, val)})
        self.properties.add_option("Height", "SLIDER", "Height", {"to": 500, "from": 0, "val": int(self.cget("height")), "callback": lambda val: self.save(lambda val: self.configure(height=val), "height", val, val)})

        self.properties.add_option("Corner Radius", "SLIDER", "Corner Radius", {"to": 100, "from": 0, "val": self.cget("corner_radius"), "callback": lambda val: self.save(lambda val: self.configure(corner_radius=val), "corner_radius", int(val), int(val))})
        self.properties.add_option("Border Width", "SLIDER", "Border Width", {"to": 100, "from": 0, "val": self.cget("border_width"), "callback": lambda val: self.save(lambda val: self.configure(border_width=val), "border_width", int(val), int(val))})
        self.properties.add_option("FG Color", "COLOR_COMBO", "fg_color", {"color": self.cget("fg_color"), "key": "fg_color", "transparent": True, "callback": lambda val: self.save(lambda val: self.configure(fg_color=val), "fg_color", val, val)})
        self.properties.add_option("Border Color", "COLOR_COMBO", "border_color", {"color": self.cget("border_color"), "key": "border_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(border_color=val), "border_color", val, val)})

        self.default()
        self.on_drag_motion(event)  # Some awkward problem

    def on_drag_motion(self, event):
        #x = self.winfo_x() - self._drag_start_x + event.x
        #y = self.winfo_y() - self._drag_start_y + event.y
        #self.properties.update_options("X", "SLIDER", {"val": int(x)})
        #self.properties.update_options("Y", "SLIDER", {"val": int(y)})


        self.properties.update_options("Width", "SLIDER", {"val": int(self.cget("width"))})
        self.properties.update_options("Height", "SLIDER", {"val": int(self.cget("height"))})
        #self.properties.update_options("Text", "TEXT", {"val": self.cget("text")})
        self.properties.update_options("Corner Radius", "SLIDER", {"val": self.cget("corner_radius")})
        self.properties.update_options("Border Width", "SLIDER", {"val": self.cget("border_width")})

        #self.place(x=x, y=y)