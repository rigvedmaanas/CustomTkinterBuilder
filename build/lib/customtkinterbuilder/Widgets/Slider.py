from customtkinter import CTkSlider
from customtkinterbuilder.PackArgs import PackArgs
from customtkinterbuilder.widgets import BaseWidgetClass
class Slider(CTkSlider, PackArgs, BaseWidgetClass):
    def __init__(self, *args, properties, **kwargs):
        super(Slider, self).__init__(*args, **kwargs)
        BaseWidgetClass.__init__(self)
        self.type = "SLIDER"
        self.properties = properties
        self.pack_options = {}
        self.pack_propagate(False)
        self.configure(from_=0, to=100, number_of_steps=100)

        self.set(50)
        self.order = 0
        self.num = None
        self.name = None

        #self.bind("<B1-Motion>", self.on_drag_motion)
        self.props = {"from_": 0, "to":100, "number_of_steps":100}
        self.bind_mouse(properties)

    def __repr__(self):

        return f"{self.type}_{str(self.order)}"

    def get_class(self):
        return "CTkSlider"

    def get_name(self):
        return self.name.replace(" ", "_")

    def save(self, func, key, val, arg):
        self.props[key] = val
        func(arg)

    def configure(self, require_redraw=False, **kwargs):
        #print(kwargs)
        super().configure(require_redraw, **kwargs)


    def _bool_change(self, val):
        if val == "True":
            return True
        elif val == "False":
            return False

    def change_name(self, name):
        self.name = name

    def on_drag_start(self, event):
        #self._drag_start_x = event.x
        #self._drag_start_y = event.y
        self.properties.destroy_children()
        #self.properties.add_seperator("Properties")
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "ID", "SINGLELINE_TEXT", "id", {"val": self.name, "callback": lambda val: (self.properties.main.hierarchy.update_text(self.name, val), self.change_name(val))})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Width", "SPINBOX", "Width", {"to": 500, "from": 0, "val": int(self.cget("width")), "callback": lambda val: self.save(lambda val: self.configure(width=val), "width", int(val), int(val))})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Height", "SPINBOX", "Height", {"to": 500, "from": 0, "val": int(self.cget("height")), "callback": lambda val: self.save(lambda val: self.configure(height=val), "height", int(val), int(val))})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Button corner radius", "SPINBOX", "button_corner_radius", {"to": 100, "from": 0, "val": self.cget("button_corner_radius"), "callback": lambda val: self.save(lambda val: self.configure(button_corner_radius=val), "button_corner_radius", int(val), int(val))})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Button length", "SPINBOX", "button_length", {"to": 100, "from": 0, "val": self.cget("button_length"), "callback": lambda val: self.save(lambda val: self.configure(button_length=val), "button_length", int(val), int(val))})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "From_", "SPINBOX", "from_", {"to": 500, "from": 0, "val": int(self.cget("from_")), "callback": lambda val: self.save(lambda val: self.configure(from_=val), "from_", int(val), int(val))})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "To", "SPINBOX", "to", {"to": 500, "from": 0, "val": int(self.cget("to")), "callback": lambda val: self.save(lambda val: self.configure(to=val), "to", int(val), int(val))})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Number Of Steps", "SPINBOX", "number_of_steps", {"to": 500, "from": 0, "val": int(self.cget("number_of_steps")), "callback": lambda val: self.save(lambda val: self.configure(number_of_steps=val), "number_of_steps", int(val), int(val))})
        #self.properties.add_option(self.properties.ARRANGEMENT, "Orientation", "COMBO", "orientation", {"vals": ["vertical", "horizontal"], "default": self.cget("orientation"), "callback": lambda val: self.save(lambda val: (self.configure(width=self.cget("height"), height=self.cget("width")), self.configure(orientation=val)), "orientation", val, val)})



        self.properties.add_option(self.properties.STYLES, "Hover", "COMBO", "hover", {"vals": ["True", "False"], "default": str(bool(self.cget("hover"))), "callback": lambda val: self.save(lambda val: self.configure(hover=val), "hover", self._bool_change(val), self._bool_change(val))})
        self.properties.add_option(self.properties.STYLES, "State", "COMBO", "state", {"vals": ["normal", "disabled"], "default": self.cget("state"), "callback": lambda val: self.save(lambda val: self.configure(state=val), "state", val, val)})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Corner Radius", "SPINBOX", "Corner Radius", {"to": 100, "from": 0, "val": self.cget("corner_radius"), "callback": lambda val: self.save(lambda val: self.configure(corner_radius=val), "corner_radius", int(val), int(val))})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Border Width", "SPINBOX", "Border Width", {"to": 100, "from": 0, "val": self.cget("border_width"), "callback": lambda val: self.save(lambda val: self.configure(border_width=val), "border_width", int(val), int(val))})
        self.properties.add_option(self.properties.STYLES, "FG Color", "COLOR_COMBO", "fg_color", {"color": self.cget("fg_color"), "key": "fg_color", "transparent": True, "callback": lambda val: self.save(lambda val: self.configure(fg_color=val), "fg_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "BG Color", "COLOR_COMBO", "bg_color", {"color": self.cget("bg_color"), "key": "bg_color", "transparent": True, "callback": lambda val: self.save(lambda val: self.configure(bg_color=val), "bg_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Border Color", "COLOR_COMBO", "border_color", {"color": self.cget("border_color"), "key": "border_color", "transparent": True, "callback": lambda val: self.save(lambda val: self.configure(border_color=val), "border_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Progress Color", "COLOR_COMBO", "progress_color", {"color": self.cget("progress_color"), "key": "progress_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(progress_color=val), "progress_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Button Color", "COLOR_COMBO", "button_color", {"color": self.cget("button_color"), "key": "button_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(button_color=val), "button_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Button hover color", "COLOR_COMBO", "button_hover_color", {"color": self.cget("button_hover_color"), "key": "button_hover_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(button_hover_color=val), "button_hover_color", val, val)})





        self.default()
        self.on_drag_motion(event)  # Some awkward problem

    def on_drag_motion(self, event):
        #x = self.winfo_x() - self._drag_start_x + event.x
        #y = self.winfo_y() - self._drag_start_y + event.y
        #self.properties.update_options("X", "SPINBOX", {"val": int(x)})
        #self.properties.update_options("Y", "SPINBOX", {"val": int(y)})

        pass
        #self.properties.update_options("Width", "SPINBOX", {"val": int(self.cget("width"))})
        #self.properties.update_options("Height", "SPINBOX", {"val": int(self.cget("height"))})
        #self.properties.update_options("Text", "TEXT", {"val": self.cget("text")})
        #self.properties.update_options("Corner Radius", "SPINBOX", {"val": self.cget("corner_radius")})
        #self.properties.update_options("Border Width", "SPINBOX", {"val": self.cget("border_width")})

        #self.place(x=x, y=y)