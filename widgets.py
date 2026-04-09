import uuid

# Need to put all those default stuff of all widgets here
class BaseWidgetClass:
    def __init__(self, **kwargs):
        self._inner_id = str(uuid.uuid4())
        #self.configure(bg_color="transparent")
        if "master" in kwargs:
            self.parent = kwargs["master"]
        else:
            self.parent = self.master

        # Common widget state – subclasses may override these after calling super().__init__
        self.order = 0
        self.num = None
        self.name = None
        self.props = {}
        self.pack_options = {}

    def bind_mouse(self, properties):
        self.bind("<MouseWheel>", properties.main.on_vert_mouse)
        self.bind("<Shift-MouseWheel>", properties.main.on_horiz_mouse)

    # ------------------------------------------------------------------
    # Methods that are identical across every widget subclass
    # ------------------------------------------------------------------

    def __repr__(self):
        return f"{self.type}_{str(self.order)}"

    def get_name(self):
        return self.name.replace(" ", "_")

    def save(self, func, key, val, arg):
        self.props[key] = val
        func(arg)

    def _bool_change(self, val):
        if val == "True":
            return True
        elif val == "False":
            return False

    def change_name(self, name):
        self.name = name

    def on_drag_motion(self, event):
        pass

    # ------------------------------------------------------------------
    # Helpers for on_drag_start implementations
    # ------------------------------------------------------------------

    def _begin_drag_start(self):
        """Clear the properties panel – always the first step in on_drag_start."""
        self.properties.destroy_children()

    def _add_id_option(self):
        """Add the ID (name) field to the properties panel."""
        self.properties.add_option(
            self.properties.GEOMETRY_CONTENT, "ID", "SINGLELINE_TEXT", "id",
            {"val": self.name, "callback": lambda val: (
                self.properties.main.hierarchy.update_text(self.name, val),
                self.change_name(val)
            )}
        )

    def _add_size_options(self):
        """Add Width and Height spinboxes to the properties panel."""
        self.properties.add_option(
            self.properties.GEOMETRY_CONTENT, "Width", "SPINBOX", "Width",
            {"to": 500, "from": 0, "val": int(self.cget("width")),
             "callback": lambda val: self.save(lambda val: self.configure(width=val), "width", int(val), int(val))}
        )
        self.properties.add_option(
            self.properties.GEOMETRY_CONTENT, "Height", "SPINBOX", "Height",
            {"to": 500, "from": 0, "val": int(self.cget("height")),
             "callback": lambda val: self.save(lambda val: self.configure(height=val), "height", int(val), int(val))}
        )

    def _get_font_family_default(self):
        """Return the default value for the Font Family option.
        Override in subclasses that track the family separately (e.g. Label)."""
        return self.cget("font").cget("family")

    def _add_font_options(self):
        """Add the six standard font property options to the properties panel."""
        self.properties.add_option(
            self.properties.STYLES, "Font Family", "FONT_FAMILY", "font_family",
            {"key": "font_family", "default": self._get_font_family_default(),
             "callback": lambda val: self.save(lambda val: self.cget("font").configure(family=val), "font_family", val, val)}
        )
        self.properties.add_option(
            self.properties.STYLES, "Font Size", "SPINBOX", "font_size",
            {"to": 500, "from": -500, "val": self.cget("font").cget("size"),
             "callback": lambda val: self.save(lambda val: self.cget("font").configure(size=int(val)), "font_size", int(val), int(val))}
        )
        self.properties.add_option(
            self.properties.STYLES, "Font Weight", "COMBO", "font_weight",
            {"vals": ["bold", "normal"], "default": self.cget("font").cget("weight"),
             "callback": lambda val: self.save(lambda val: self.cget("font").configure(weight=val), "font_weight", val, val)}
        )
        self.properties.add_option(
            self.properties.STYLES, "Font Slant", "COMBO", "font_slant",
            {"vals": ["italic", "roman"], "default": self.cget("font").cget("slant"),
             "callback": lambda val: self.save(lambda val: self.cget("font").configure(slant=val), "font_slant", val, val)}
        )
        self.properties.add_option(
            self.properties.STYLES, "Font Underline", "COMBO", "font_underline",
            {"vals": ["True", "False"], "default": str(bool(self.cget("font").cget("underline"))),
             "callback": lambda val: self.save(lambda val: self.cget("font").configure(underline=val), "font_underline", self._bool_change(val), self._bool_change(val))}
        )
        self.properties.add_option(
            self.properties.STYLES, "Font Overstrike", "COMBO", "font_overstrike",
            {"vals": ["True", "False"], "default": str(bool(self.cget("font").cget("overstrike"))),
             "callback": lambda val: self.save(lambda val: self.cget("font").configure(overstrike=val), "font_overstrike", self._bool_change(val), self._bool_change(val))}
        )
