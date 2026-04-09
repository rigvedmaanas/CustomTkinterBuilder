from customtkinter import CTkScrollbar
from PackArgs import PackArgs
from widgets import BaseWidgetClass

class Scrollbar(CTkScrollbar, PackArgs, BaseWidgetClass):
    def __init__(self, *args, properties, **kwargs):
        super(Scrollbar, self).__init__(*args, **kwargs)
        BaseWidgetClass.__init__(self)
        self.type = "SCROLLBAR"
        self.properties = properties
        self.pack_propagate(False)
        #self.configure(bg_color=self.master.cget("fg_color"))

        #self.bind("<B1-Motion>", self.on_drag_motion)
        self.bind_mouse(properties)

    def get_class(self):
        return "CTkScrollbar"

    def on_drag_start(self, event):
        #self._drag_start_x = event.x
        #self._drag_start_y = event.y
        self._begin_drag_start()
        #self.properties.add_seperator("Properties")
        self._add_id_option()
        self._add_size_options()

        self.properties.add_option(self.properties.STYLES, "Hover", "COMBO", "hover", {"vals": ["True", "False"], "default": str(bool(self.cget("hover"))), "callback": lambda val: self.save(lambda val: self.configure(hover=val), "hover", self._bool_change(val), self._bool_change(val))})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Corner Radius", "SPINBOX", "Corner Radius", {"to": 100, "from": 0, "val": self.cget("corner_radius"), "callback": lambda val: self.save(lambda val: self.configure(corner_radius=val), "corner_radius", int(val), int(val))})
        self.properties.add_option(self.properties.STYLES, "FG Color", "COLOR_COMBO", "fg_color", {"color": self.cget("fg_color"), "key": "fg_color", "transparent": True, "callback": lambda val: self.save(lambda val: self.configure(fg_color=val), "fg_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "BG Color", "COLOR_COMBO", "bg_color", {"color": self.cget("bg_color"), "key": "bg_color", "transparent": True, "callback": lambda val: self.save(lambda val: self.configure(bg_color=val), "bg_color", val, val)})
        # self.cget() doesn't support these
        # self.properties.add_option(self.properties.STYLES, "Button Hover Color", "COLOR_COMBO", "button_hover_color", {"color": self.cget("button_hover_color"), "key": "button_hover_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(button_hover_color=val), "button_hover_color", val, val)})
        # self.properties.add_option(self.properties.STYLES, "Button Color", "COLOR_COMBO", "button_color", {"color": self.cget("button_color"), "key": "button_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(button_color=val), "button_color", val, val)})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Border Spacing", "SPINBOX", "border_spacing", {"to": 100, "from": 0, "val": self.cget("border_spacing"), "callback": lambda val: self.save(lambda val: self.configure(border_spacing=val), "border_spacing", int(val), int(val))})
        # self.configure() doesn't support this
        # self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Orientation", "COMBO", "orientation", {"vals": ["vertical", "horizontal"], "default": self.cget("orientation"), "callback": lambda val: self.save(lambda val: self.configure(orientation=val), "orientation", val, val)})
        # self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Minimum Pixel Length", "SPINBOX", "minimum_pixel_length", {"to": 500, "from": 0, "val": int(self.cget("minimum_pixel_length")), "callback": lambda val: self.save(lambda val: self.configure(minimum_pixel_length=val), "minimum_pixel_length", int(val), int(val))})

        self.default()
        self.on_drag_motion(event)  # Some awkward problem
