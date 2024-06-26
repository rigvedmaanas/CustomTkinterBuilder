from customtkinter import CTkOptionMenu
from PackArgs import PackArgs
from widgets import BaseWidgetClass
class OptionMenu(CTkOptionMenu, PackArgs, BaseWidgetClass):
    def __init__(self, *args, properties, **kwargs):
        super(OptionMenu, self).__init__(*args, **kwargs)
        BaseWidgetClass.__init__(self)
        self.type = "OPTIONMENU"
        self.properties = properties
        self.pack_options = {}
        self.pack_propagate(False)
        #self.configure(bg_color=self.master.cget("fg_color"))
        self.order = 0
        self.num = None
        self.name = None
        self.set_nonvisible_disable()

        #self.bind("<B1-Motion>", self.on_drag_motion)
        self.props = {}
        self.bind_mouse(properties)

    def set_nonvisible_disable(self):
        self.color_disabled = self.cget("text_color_disabled")
        self.configure(state="disabled", text_color_disabled=self.cget("text_color"))


    def change_disabled_color(self, color):
        self.color_disabled = color


    def __repr__(self):

        return f"{self.type}_{str(self.order)}"

    def get_class(self):
        return "CTkOptionMenu"

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

    def set_val(self, vals):
        if len(vals) != 0:
            self.set(vals[0])

    def on_drag_start(self, event):
        #self._drag_start_x = event.x
        #self._drag_start_y = event.y
        self.properties.destroy_children()
        #self.properties.add_seperator("Properties")
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "ID", "SINGLELINE_TEXT", "id", {"val": self.name, "callback": lambda val: (self.properties.main.hierarchy.update_text(self.name, val), self.change_name(val))})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Width", "SPINBOX", "Width", {"to": 500, "from": 0, "val": int(self.cget("width")), "callback": lambda val: self.save(lambda val: self.configure(width=val), "width", int(val), int(val))})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Height", "SPINBOX", "Height", {"to": 500, "from": 0, "val": int(self.cget("height")), "callback": lambda val: self.save(lambda val: self.configure(height=val), "height", int(val), int(val))})

        self.properties.add_option(self.properties.ARRANGEMENT, "Anchor", "COMBO", "anchor", {"vals": ["n", "ne", "e", "se", "s", "sw", "w", "nw", "center"], "default": self.cget("anchor"), "callback": lambda val: self.save(lambda val: self.configure(anchor=val), "anchor", val, val)})


        self.properties.add_option(self.properties.STYLES, "Font Family", "FONT_FAMILY", "font_family", {"key": "font_family", "default": self.cget("font").cget("family"), "callback": lambda val: self.save(lambda val: self.cget("font").configure(family=val), "font_family", val, val)})
        self.properties.add_option(self.properties.STYLES, "Font Size", "SPINBOX", "font_size", {"to": 500, "from": -500, "val": self.cget("font").cget("size"), "callback": lambda val: self.save(lambda val: self.cget("font").configure(size=int(val)), "font_size", int(val), int(val))})
        self.properties.add_option(self.properties.STYLES, "Font Weight", "COMBO", "font_weight", {"vals": ["bold", "normal"], "default": self.cget("font").cget("weight"), "callback": lambda val: self.save(lambda val: self.cget("font").configure(weight=val), "font_weight", val, val)})
        self.properties.add_option(self.properties.STYLES, "Font Slant", "COMBO", "font_slant", {"vals": ["italic", "roman"], "default": self.cget("font").cget("slant"), "callback": lambda val: self.save(lambda val: self.cget("font").configure(slant=val), "font_slant", val, val)})
        self.properties.add_option(self.properties.STYLES, "Font Underline", "COMBO", "font_underline", {"vals": ["True", "False"], "default": str(bool(self.cget("font").cget("underline"))), "callback": lambda val: self.save(lambda val: self.cget("font").configure(underline=val), "font_underline", self._bool_change(val), self._bool_change(val))})
        self.properties.add_option(self.properties.STYLES, "Font Overstrike", "COMBO", "font_overstrike", {"vals": ["True", "False"], "default": str(bool(self.cget("font").cget("overstrike"))), "callback": lambda val: self.save(lambda val: self.cget("font").configure(overstrike=val), "font_overstrike", self._bool_change(val), self._bool_change(val))})

        self.properties.add_option(self.properties.STYLES, "Hover", "COMBO", "hover", {"vals": ["True", "False"], "default": str(bool(self.cget("hover"))), "callback": lambda val: self.save(lambda val: self.configure(hover=val), "hover", self._bool_change(val), self._bool_change(val))})
        # Will probably add this in V2
        # self.properties.add_option(self.properties.STYLES, "State", "COMBO", "state", {"vals": ["normal", "disabled"], "default": self.current_state, "callback": lambda val: self.save(lambda val: self.change_current_state(val), "state", val, val)})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Corner Radius", "SPINBOX", "Corner Radius", {"to": 100, "from": 0, "val": self.cget("corner_radius"), "callback": lambda val: self.save(lambda val: self.configure(corner_radius=val), "corner_radius", int(val), int(val))})
        self.properties.add_option(self.properties.STYLES, "FG Color", "COLOR_COMBO", "fg_color", {"color": self.cget("fg_color"), "key": "fg_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(fg_color=val), "fg_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "BG Color", "COLOR_COMBO", "bg_color", {"color": self.cget("bg_color"), "key": "bg_color", "transparent": True, "callback": lambda val: self.save(lambda val: self.configure(bg_color=val), "bg_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Text Color", "COLOR_COMBO", "text_color", {"color": self.cget("text_color"), "key": "text_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(text_color=val, text_color_disabled=val), "text_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Text Disabled Color", "COLOR_COMBO", "text_color_disabled", {"color": self.color_disabled, "key": "text_color_disabled", "transparent": False, "callback": lambda val: self.save(lambda val: self.change_disabled_color(val), "text_color_disabled", val, val)})
        self.properties.add_option(self.properties.STYLES, "Button Color", "COLOR_COMBO", "button_color", {"color": self.cget("button_color"), "key": "button_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(button_color=val), "button_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Button Hover Color", "COLOR_COMBO", "button_hover_color", {"color": self.cget("button_hover_color"), "key": "button_hover_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(button_hover_color=val), "button_hover_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Dropdown FG Color", "COLOR_COMBO", "dropdown_fg_color", {"color": self.cget("dropdown_fg_color"), "key": "dropdown_fg_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(dropdown_fg_color=val), "dropdown_fg_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Dropdown Hover Color", "COLOR_COMBO", "dropdown_hover_color", {"color": self.cget("dropdown_hover_color"), "key": "dropdown_hover_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(dropdown_hover_color=val), "dropdown_hover_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Dropdown Text Color", "COLOR_COMBO", "dropdown_text_color", {"color": self.cget("dropdown_text_color"), "key": "dropdown_text_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(dropdown_text_color=val), "dropdown_text_color", val, val)})
        self.properties.add_option(self.properties.ARRANGEMENT, "Dynamic Resizing", "COMBO", "dynamic_resizing", {"vals": ["True", "False"], "default": str(bool(self.cget("dynamic_resizing"))), "callback": lambda val: self.save(lambda val: self.configure(dynamic_resizing=val), "dynamic_resizing", self._bool_change(val), self._bool_change(val))})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Values", "LISTBOX", "values",
                                   {"default_vals": self.cget("values"), "key": "values",
                                    "callback": lambda vals: self.save(lambda vals: (self.configure(values=vals), self.set_val(vals)),
                                                                       "values", vals, vals)})

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