from customtkinter import CTkScrollableFrame
from PackArgs import PackArgs

class ScrollableFrame(CTkScrollableFrame, PackArgs):
    def __init__(self, *args, properties, **kwargs):
        super(ScrollableFrame, self).__init__(*args, **kwargs)
        self.type = "SCROLLABLEFRAME"
        self.properties = properties
        self.pack_options = {}
        self.pack_propagate(False)
        #self.configure(bg_color=self.master.cget("fg_color"))
        self.order = 0
        self.num = None
        self.name = None
        print(self.master.master.master.pack_info())

        #self.bind("<B1-Motion>", self.on_drag_motion)
        self.props = {}

    def __repr__(self):

        return f"{self.type}_{str(self.order)}"

    def get_class(self):
        return "CTkScrollableFrame"

    def get_name(self):
        return self.name.replace(" ", "_")

    def save(self, func, key, val, arg):
        self.props[key] = val
        func(arg)

    def configure(self, require_redraw=False, **kwargs):
        print(kwargs)
        super().configure(**kwargs)


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
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Label Text", "TEXT", "label_text", {"val": self.cget("label_text"), "callback": lambda val: self.save(lambda val: self.configure(label_text=val), "label_text", val, val)})

        self.properties.add_option(self.properties.ARRANGEMENT, "Label Anchor", "COMBO", "label_anchor", {"vals": ["n", "ne", "e", "se", "s", "sw", "w", "nw", "center"], "default": self.cget("label_anchor"), "callback": lambda val: self.save(lambda val: self.configure(label_anchor=val), "label_anchor", val, val)})


        self.properties.add_option(self.properties.STYLES, "Font Family", "FONT_FAMILY", "font_family", {"key": "font_family", "default": self.cget("label_font").cget("family"), "callback": lambda val: self.save(lambda val: self.cget("label_font").configure(family=val), "font_family", val, val)})
        self.properties.add_option(self.properties.STYLES, "Font Size", "SPINBOX", "font_size", {"to": 500, "from": -500, "val": self.cget("label_font").cget("size"), "callback": lambda val: self.save(lambda val: self.cget("label_font").configure(size=int(val)), "font_size", int(val), int(val))})
        self.properties.add_option(self.properties.STYLES, "Font Weight", "COMBO", "font_weight", {"vals": ["bold", "normal"], "default": self.cget("label_font").cget("weight"), "callback": lambda val: self.save(lambda val: self.cget("label_font").configure(weight=val), "font_weight", val, val)})
        self.properties.add_option(self.properties.STYLES, "Font Slant", "COMBO", "font_slant", {"vals": ["italic", "roman"], "default": self.cget("label_font").cget("slant"), "callback": lambda val: self.save(lambda val: self.cget("label_font").configure(slant=val), "font_slant", val, val)})
        self.properties.add_option(self.properties.STYLES, "Font Underline", "COMBO", "font_underline", {"vals": ["True", "False"], "default": str(bool(self.cget("label_font").cget("underline"))), "callback": lambda val: self.save(lambda val: self.cget("label_font").configure(underline=val), "font_underline", self._bool_change(val), self._bool_change(val))})
        self.properties.add_option(self.properties.STYLES, "Font Overstrike", "COMBO", "font_overstrike", {"vals": ["True", "False"], "default": str(bool(self.cget("label_font").cget("overstrike"))), "callback": lambda val: self.save(lambda val: self.cget("label_font").configure(overstrike=val), "font_overstrike", self._bool_change(val), self._bool_change(val))})

        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Corner Radius", "SPINBOX", "Corner Radius", {"to": 100, "from": 0, "val": self.cget("corner_radius"), "callback": lambda val: self.save(lambda val: self.configure(corner_radius=val), "corner_radius", int(val), int(val))})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Border Width", "SPINBOX", "Border Width", {"to": 100, "from": 0, "val": self.cget("border_width"), "callback": lambda val: self.save(lambda val: self.configure(border_width=val), "border_width", int(val), int(val))})
        self.properties.add_option(self.properties.STYLES, "FG Color", "COLOR_COMBO", "fg_color", {"color": self.cget("fg_color"), "key": "fg_color", "transparent": True, "callback": lambda val: self.save(lambda val: self.configure(fg_color=val), "fg_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "BG Color", "COLOR_COMBO", "bg_color", {"color": self.cget("bg_color"), "key": "bg_color", "transparent": True, "callback": lambda val: self.save(lambda val: self.configure(bg_color=val), "bg_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Border Color", "COLOR_COMBO", "border_color", {"color": self.cget("border_color"), "key": "border_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(border_color=val), "border_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Scrollbar FG Color", "COLOR_COMBO", "scrollbar_fg_color", {"color": self.cget("scrollbar_fg_color"), "key": "scrollbar_fg_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(scrollbar_fg_color=val), "scrollbar_fg_color", val, val)})
        # self.properties.add_option(self.properties.STYLES, "Scrollbar Button Color", "COLOR_COMBO", "scrollbar_button_color", {"color": self.cget("scrollbar_button_color"), "key": "scrollbar_button_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(scrollbar_button_color=val), "scrollbar_button_color", val, val)})
        # self.properties.add_option(self.properties.STYLES, "Scrollbar Button Hover Color", "COLOR_COMBO", "scrollbar_button_hover_color", {"color": self.cget("scrollbar_button_hover_color"), "key": "scrollbar_button_hover_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(scrollbar_button_hover_color=val), "scrollbar_button_hover_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Label FG Color", "COLOR_COMBO", "label_fg_color", {"color": self.cget("label_fg_color"), "key": "label_fg_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(label_fg_color=val), "label_fg_color", val, val)})
        # self.properties.add_option(self.properties.STYLES, "Label Text Color", "COLOR_COMBO", "label_text_color", {"color": self.cget("label_text_color"), "key": "label_text_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(label_text_color=val), "label_text_color", val, val)})
        # self.properties.add_option(self.properties.ARRANGEMENT, "Orientation", "COMBO", "orientation", {"vals": ["vertical", "horizontal"], "default": self.cget("orientation"), "callback": lambda val: self.save(lambda val: self.configure(orientation=val), "orientation", val, val)})







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