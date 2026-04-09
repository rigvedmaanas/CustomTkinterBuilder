from customtkinter import CTkCheckBox
from PackArgs import PackArgs
from widgets import BaseWidgetClass

class CheckBox(CTkCheckBox, PackArgs, BaseWidgetClass):
    def __init__(self, *args, properties, **kwargs):
        super(CheckBox, self).__init__(*args, **kwargs)
        BaseWidgetClass.__init__(self)
        self.type = "CHECKBOX"
        self.properties = properties
        self.pack_propagate(False)
        #self.configure(bg_color=self.master.cget("fg_color"))

        #self.bind("<B1-Motion>", self.on_drag_motion)
        self.bind_mouse(properties)

    def get_class(self):
        return "CTkCheckBox"

    def on_drag_start(self, event):
        #self._drag_start_x = event.x
        #self._drag_start_y = event.y
        self._begin_drag_start()
        #self.properties.add_seperator("Properties")
        self._add_id_option()
        self._add_size_options()
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Text", "TEXT", "text", {"val": self.cget("text"), "callback": lambda val: self.save(lambda val: self.configure(text=val), "text", val, val)})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Checkbox Width", "SPINBOX", "checkbox_width",
                                   {"to": 500, "from": 0, "val": int(self.cget("checkbox_width")),
                                    "callback": lambda val: self.save(lambda val: self.configure(checkbox_width=val), "checkbox_width",
                                                                      int(val), int(val))})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Checkbox Height", "SPINBOX", "checkbox_height",
                                   {"to": 500, "from": 0, "val": int(self.cget("checkbox_height")),
                                    "callback": lambda val: self.save(lambda val: self.configure(checkbox_height=val), "checkbox_height",
                                                                      int(val), int(val))})

        self._add_font_options()

        self.properties.add_option(self.properties.STYLES, "Hover", "COMBO", "hover", {"vals": ["True", "False"], "default": str(bool(self.cget("hover"))), "callback": lambda val: self.save(lambda val: self.configure(hover=val), "hover", self._bool_change(val), self._bool_change(val))})
        self.properties.add_option(self.properties.STYLES, "State", "COMBO", "state", {"vals": ["normal", "disabled"], "default": self.cget("state"), "callback": lambda val: self.save(lambda val: self.configure(state=val), "state", val, val)})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Corner Radius", "SPINBOX", "Corner Radius", {"to": 100, "from": 0, "val": self.cget("corner_radius"), "callback": lambda val: self.save(lambda val: self.configure(corner_radius=val), "corner_radius", int(val), int(val))})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Border Width", "SPINBOX", "Border Width", {"to": 100, "from": 0, "val": self.cget("border_width"), "callback": lambda val: self.save(lambda val: self.configure(border_width=val), "border_width", int(val), int(val))})
        self.properties.add_option(self.properties.STYLES, "FG Color", "COLOR_COMBO", "fg_color", {"color": self.cget("fg_color"), "key": "fg_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(fg_color=val), "fg_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "BG Color", "COLOR_COMBO", "bg_color", {"color": self.cget("bg_color"), "key": "bg_color", "transparent": True, "callback": lambda val: self.save(lambda val: self.configure(bg_color=val), "bg_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Border Color", "COLOR_COMBO", "border_color", {"color": self.cget("border_color"), "key": "border_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(border_color=val), "border_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Hover Color", "COLOR_COMBO", "hover_color", {"color": self.cget("hover_color"), "key": "hover_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(hover_color=val), "hover_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Text Color", "COLOR_COMBO", "text_color", {"color": self.cget("text_color"), "key": "text_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(text_color=val), "text_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Text Disabled Color", "COLOR_COMBO", "text_color_disabled", {"color": self.cget("text_color_disabled"), "key": "text_color_disabled", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(text_color_disabled=val), "text_color_disabled", val, val)})

        self.default()
        self.on_drag_motion(event)  # Some awkward problem
