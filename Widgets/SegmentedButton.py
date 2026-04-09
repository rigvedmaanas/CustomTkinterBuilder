from customtkinter import CTkSegmentedButton
from PackArgs import PackArgs
from widgets import BaseWidgetClass

class SegmentedButton(CTkSegmentedButton, PackArgs, BaseWidgetClass):
    def __init__(self, *args, properties, **kwargs):
        super(SegmentedButton, self).__init__(*args, **kwargs)
        BaseWidgetClass.__init__(self)
        self.type = "SEGMENTEDBUTTON"
        self.properties = properties
        self.pack_propagate(False)
        #self.configure(bg_color=self.master.cget("fg_color"))

        #self.bind("<B1-Motion>", self.on_drag_motion)
        #self.bind_mouse(properties)

    def _set_appearance_mode(self, mode_string):
        for x in self._buttons_dict.values():
            #print(x)
            x._set_appearance_mode(mode_string)

    def get_class(self):
        return "CTkSegmentedButton"

    def configure(self, require_redraw=False, **kwargs):
        #print(kwargs)
        super().configure(**kwargs)
        self._set_appearance_mode("light" if self.properties.main.appearance.get() == 0 else "dark")

    def on_drag_start(self, event):
        #self._drag_start_x = event.x
        #self._drag_start_y = event.y
        self._begin_drag_start()
        #self.properties.add_seperator("Properties")
        self._add_id_option()
        self._add_size_options()

        self._add_font_options()

        # self.cget() doesn't support this. Why?
        # self.properties.add_option(self.properties.STYLES, "State", "COMBO", "state", {"vals": ["normal", "disabled"], "default": self.cget("state"), "callback": lambda val: self.save(lambda val: self.configure(state=val), "state", val, val)})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Corner Radius", "SPINBOX", "Corner Radius", {"to": 100, "from": 0, "val": self.cget("corner_radius"), "callback": lambda val: self.save(lambda val: self.configure(corner_radius=val), "corner_radius", int(val), int(val))})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Border Width", "SPINBOX", "Border Width", {"to": 100, "from": 0, "val": self.cget("border_width"), "callback": lambda val: self.save(lambda val: self.configure(border_width=val), "border_width", int(val), int(val))})
        self.properties.add_option(self.properties.STYLES, "FG Color", "COLOR_COMBO", "fg_color", {"color": self.cget("fg_color"), "key": "fg_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(fg_color=val), "fg_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "BG Color", "COLOR_COMBO", "bg_color", {"color": self.cget("bg_color"), "key": "bg_color", "transparent": True, "callback": lambda val: self.save(lambda val: self.configure(bg_color=val), "bg_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Selected Color", "COLOR_COMBO", "selected_color", {"color": self.cget("selected_color"), "key": "selected_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(selected_color=val), "selected_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Selected Hover Color", "COLOR_COMBO", "selected_hover_color", {"color": self.cget("selected_hover_color"), "key": "selected_hover_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(selected_hover_color=val), "selected_hover_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Unselected Color", "COLOR_COMBO", "unselected_color", {"color": self.cget("unselected_color"), "key": "unselected_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(unselected_color=val), "unselected_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Unselected Hover Color", "COLOR_COMBO", "unselected_hover_color", {"color": self.cget("unselected_hover_color"), "key": "unselected_hover_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(unselected_hover_color=val), "unselected_hover_color", val, val)})

        self.properties.add_option(self.properties.ARRANGEMENT, "Dynamic Resizing", "COMBO", "dynamic_resizing", {"vals": ["True", "False"], "default": str(bool(self.cget("dynamic_resizing"))), "callback": lambda val: self.save(lambda val: self.configure(dynamic_resizing=val), "dynamic_resizing", self._bool_change(val), self._bool_change(val))})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Values", "LISTBOX", "values",
                                   {"default_vals": self.cget("values"), "key": "values",
                                    "callback": lambda vals: self.save(lambda vals: self.configure(values=vals), "values", vals, vals)})

        self.properties.add_option(self.properties.STYLES, "Text Color", "COLOR_COMBO", "text_color", {"color": self.cget("text_color"), "key": "text_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(text_color=val), "text_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Text Disabled Color", "COLOR_COMBO", "text_color_disabled", {"color": self.cget("text_color_disabled"), "key": "text_color_disabled", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(text_color_disabled=val), "text_color_disabled", val, val)})

        self.default()
        self.on_drag_motion(event)  # Some awkward problem
