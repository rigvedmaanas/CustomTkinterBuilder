class PackArgs:
    def __init__(self):
        self.options = {}
        self.pack_options = {}


    def set_options(self, val):
        self.options = val

    def redraw(self, **kwargs):
        self.pack_options = kwargs
        #print(self.pack_options)
        self.pack_options.pop("in")

        self.properties.main.redraw(self.properties.main.widgets[self.properties.main.r])

    def default(self):
        #self.properties.add_seperator("Layout (Pack)")

        self.properties.add_option(self.properties.LAYOUT, "Fill", "COMBO", "Fill", {"vals": ["none", "x", "y", "both"], "default": str(self.pack_info()["fill"]), "callback": lambda val: self.redraw(fill=val, **{k: v for k, v in self.pack_info().items() if k != "fill"})})
        self.properties.add_option(self.properties.LAYOUT, "Expand", "COMBO", "Expand", {"vals": ["False", "True"], "default": str(bool(self.pack_info()["expand"])), "callback": lambda val: self.redraw(expand=self._bool_change(val), **{k: v for k, v in self.pack_info().items() if k != "expand"})})
        # self.properties.add_option(self.properties.STYLES, "Hover", "COMBO", "hover", {"vals": ["True", "False"], "default": str(bool(self.cget("hover"))), "callback": lambda val: self.save(lambda val: self.configure(hover=val), "hover", self._bool_change(val), self._bool_change(val))})

        self.properties.add_option(self.properties.LAYOUT, "Side", "COMBO", "Side", {"vals": ["top", "bottom", "left", "right"], "default": str(self.pack_info()["side"]), "callback": lambda val: self.redraw(side=val, **{k: v for k, v in self.pack_info().items() if k != "side"})})

        if type(self.pack_info()["padx"]) == int:
            self.properties.add_option(self.properties.LAYOUT, "Padx", "TUPLE", "Padx", {"to": 500, "from": 0, "val1": int(self.pack_info()["padx"]), "val2": int(self.pack_info()["padx"]), "callback": lambda val1, val2: self.redraw(padx=(val1, val2), **{k: v for k, v in self.pack_info().items() if k != "padx"})})

        else:
            self.properties.add_option(self.properties.LAYOUT, "Padx", "TUPLE", "Padx", {"to": 500, "from": 0, "val1": int(self.pack_info()["padx"][0]), "val2": int(self.pack_info()["padx"][1]), "callback": lambda val1, val2: self.redraw(padx=(val1, val2), **{k: v for k, v in self.pack_info().items() if k != "padx"})})

        if type(self.pack_info()["pady"]) == int:
            self.properties.add_option(self.properties.LAYOUT, "Pady", "TUPLE", "Pady", {"to": 500, "from": 0, "val1": int(self.pack_info()["pady"]), "val2": int(self.pack_info()["pady"]), "callback": lambda val1, val2: self.redraw(pady=(val1, val2), **{k: v for k, v in self.pack_info().items() if k != "pady"})})

        else:
            self.properties.add_option(self.properties.LAYOUT, "Pady", "TUPLE", "Pady", {"to": 500, "from": 0, "val1": int(self.pack_info()["pady"][0]), "val2": int(self.pack_info()["pady"][1]), "callback": lambda val1, val2: self.redraw(pady=(val1, val2), **{k: v for k, v in self.pack_info().items() if k != "pady"})})
