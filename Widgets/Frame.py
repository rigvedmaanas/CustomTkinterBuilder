from customtkinter import CTkFrame
from PackArgs import PackArgs
from widgets import BaseWidgetClass

class Frame(CTkFrame, PackArgs, BaseWidgetClass):
    def __init__(self, *args, properties, **kwargs):
        super(Frame, self).__init__(*args, **kwargs)
        BaseWidgetClass.__init__(self)
        self.type = "FRAME"
        self.properties = properties
        self.propagate_on_pack = "False"
        self.pack_propagate(False)
        """if type(self.master.master.cget("fg_color")) == str:
            self.configure(bg_color=(self.master.cget("fg_color"), self.master.cget("fg_color")))
        else:
            self.configure(bg_color=self.master.cget("fg_color"))
"""
        self.num = 0

        #self.bind("<B1-Motion>", self.on_drag_motion)
        self.bind_mouse(properties)

    def get_class(self):
        return "CTkFrame"

    def get_not_transparent_color(self, widget):
        try:
            c = widget.get_class()
            if widget.master.cget("fg_color") != "transparent":
                return widget.master.cget("fg_color")
            else:
                return self.get_not_transparent_color(widget.master)
        except Exception as e:
            return self.get_not_transparent_color(widget.master)

    def configure(self, require_redraw=False, **kwargs):
        ##print(kwargs)
        if "bg_color" in kwargs:
            if kwargs["bg_color"] == "transparent":
                kwargs["bg_color"] = self.get_not_transparent_color(self)
        #print(kwargs)
        super().configure(require_redraw, **kwargs)

    def change_pack_propagate(self, val):
        self.propagate_on_pack = val

        self.pack_propagate(self._bool_change(val))
        #self.pack_propagate(False)
        self.configure(width=self.cget("width"), height=self.cget("height"))
        #self.properties.main.redraw(self.properties.main.widgets[self.properties.main.r])

    def on_drag_start(self, event):
        #self._drag_start_x = event.x
        #self._drag_start_y = event.y
        self._begin_drag_start()
        #self.properties.add_seperator("Properties")
        self._add_id_option()
        self._add_size_options()
        self.properties.add_option(self.properties.LAYOUT, "Pack Propagate", "COMBO", "pack_propagate", {"vals": ["True", "False"], "default": self.propagate_on_pack, "callback": lambda val: self.change_pack_propagate(val)})

        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Corner Radius", "SPINBOX", "Corner Radius", {"to": 100, "from": 0, "val": self.cget("corner_radius"), "callback": lambda val: self.save(lambda val: self.configure(corner_radius=val), "corner_radius", int(val), int(val))})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Border Width", "SPINBOX", "Border Width", {"to": 100, "from": 0, "val": self.cget("border_width"), "callback": lambda val: self.save(lambda val: self.configure(border_width=val), "border_width", int(val), int(val))})
        self.properties.add_option(self.properties.STYLES, "FG Color", "COLOR_COMBO", "fg_color", {"color": self.cget("fg_color"), "key": "fg_color", "transparent": True, "callback": lambda val: self.save(lambda val: self.configure(fg_color=val), "fg_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "BG Color", "COLOR_COMBO", "bg_color", {"color": self.cget("bg_color"), "key": "bg_color", "transparent": True, "callback": lambda val: self.save(lambda val: self.configure(bg_color=val), "bg_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Border Color", "COLOR_COMBO", "border_color", {"color": self.cget("border_color"), "key": "border_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(border_color=val), "border_color", val, val)})

        self.default()
        self.on_drag_motion(event)  # Some awkward problem
