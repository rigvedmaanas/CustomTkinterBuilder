from customtkinter import CTkLabel, CTkImage
from PIL import Image
from PackArgs import PackArgs
from widgets import BaseWidgetClass

class Label(CTkLabel, PackArgs, BaseWidgetClass):
    def __init__(self, *args, properties, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        BaseWidgetClass.__init__(self)
        self.type = "LABEL"
        self.properties = properties
        self.image = None
        self.img = None
        self.size = None
        self.pack_propagate(False)
        #self.configure(bg_color=self.master.cget("fg_color"))
        self.num = 0
        self.family = self.cget("font").cget("family")
        #print(self.family)
        self.configure(bg_color="transparent")
        #self.bind("<B1-Motion>", self.on_drag_motion)
        self.bind_mouse(properties)

    def get_class(self):
        return "CTkLabel"

    def save(self, func, key, val, arg):
        if key == "font_family":
            self.family = val
            #print("save", self.family)
        self.props[key] = val
        func(arg)

    def _get_font_family_default(self):
        return self.family

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

        super().configure(require_redraw, **kwargs)

    def on_drag_start(self, event):
        #print(self.cget("bg_color"))

        #self._drag_start_x = event.x
        #self._drag_start_y = event.y
        self._begin_drag_start()
        #self.properties.add_seperator("Properties")
        self._add_id_option()
        self._add_size_options()
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Text", "TEXT", "text", {"val": self.cget("text"), "callback": lambda val: self.save(lambda val: self.configure(text=val), "text", val, val)})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Image", "IMAGE", "image", {"image": self.image, "size": self.get_size, "key": "image", "callback": self.set_image})

        # Had to reset the image for compound option to take effect
        self.properties.add_option(self.properties.ARRANGEMENT, "Compound", "COMBO", "compound", {"vals": ["top", "bottom", "left", "right"], "default": self.cget("compound"), "callback": lambda val: self.save(lambda val: (self.configure(compound=val, image=None), self.set_compound(self.image)), "compound", val, val)})
        self.properties.add_option(self.properties.ARRANGEMENT, "Anchor", "COMBO", "anchor", {"vals": ["n", "ne", "e", "se", "s", "sw", "w", "nw", "center"], "default": self.cget("anchor"), "callback": lambda val: self.save(lambda val: self.configure(anchor=val), "anchor", val, val)})
        self.properties.add_option(self.properties.ARRANGEMENT, "Justify", "COMBO", "justify", {"vals": ["left", "right", "center"], "default": self.cget("justify"), "callback": lambda val: self.save(lambda val: self.configure(justify=val), "justify", val, val)})
        self.properties.add_option(self.properties.ARRANGEMENT, "Padx", "SPINBOX", "PADX", {"to": 500, "from": 0, "val": int(self.cget("padx")), "callback": lambda val: self.save(lambda val: self.configure(padx=val), "padx", int(val), int(val))})
        self.properties.add_option(self.properties.ARRANGEMENT, "Pady", "SPINBOX", "PADY", {"to": 500, "from": 0, "val": int(self.cget("pady")), "callback": lambda val: self.save(lambda val: self.configure(pady=val), "pady", int(val), int(val))})

        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Corner Radius", "SPINBOX", "Corner Radius", {"to": 100, "from": 0, "val": self.cget("corner_radius"), "callback": lambda val: self.save(lambda val: self.configure(corner_radius=val), "corner_radius", int(val), int(val))})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Wrap Length", "SPINBOX", "wraplength", {"to": 100, "from": 0, "val": self.cget("wraplength"), "callback": lambda val: self.save(lambda val: self.configure(wraplength=val), "wraplength", int(val), int(val))})

        #print("Properties", self.family)
        self._add_font_options()

        self.properties.add_option(self.properties.STYLES, "FG Color", "COLOR_COMBO", "fg_color", {"color": self.cget("fg_color"), "key": "fg_color", "transparent": True, "callback": lambda val: self.save(lambda val: self.configure(fg_color=val), "fg_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "BG Color", "COLOR_COMBO", "bg_color", {"color": self.cget("bg_color"), "key": "bg_color", "transparent": True, "callback": lambda val: self.save(lambda val: self.configure(bg_color=val), "bg_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Text Color", "COLOR_COMBO", "text_color", {"color": self.cget("text_color"), "key": "text_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(text_color=val), "text_color", val, val)})

        self.default()
        #self.on_drag_motion(event)  # Some awkward problem

    def get_size(self):
        return self.size

    def set_image(self, img, size):
        if img != "":
            self.image = img
            img = Image.open(img)
            img = CTkImage(light_image=img, dark_image=img, size=size)
            #print(img, int(self.cget("width"))+1, type(int(self.cget("width"))+1))
            # Image is not updating. Changing the width is the workaround I found. Need to change this if possible
            self.configure(image=img, width=int(self.cget("width"))+1)
            self.configure(width=int(self.cget("width"))-1)
            self.img = img
            self.size = size
            self.props["image"] = img
        else:
            self.image = None
            # Bug - 1
            # Image is not updating. Changing the width is the workaround I found. Need to change this if possible
            # An Artifact is seen when the image is removed. Changing the height is the workaround I found. Need to change this if possible
            # Images are facing this issue https://github.com/TomSchimansky/CustomTkinter/issues/1899 and the pull request resolving it - https://github.com/TomSchimansky/CustomTkinter/pull/1931
            # Bug - 2
            # This is done just because there is a big bug when the image is removed from a button.
            # When the image is removed from the button an unexpected button is seen underneath.

            # Is this my issue or just a hidden bug in the customtkinter library

            with_img_width = self.winfo_width()
            with_img_height = self.winfo_height()
            real_width = self.cget("width")
            real_height = self.cget("height")
            self.configure(image="", width=with_img_width, height=with_img_height)
            self.update()
            self.configure(width=real_width, height=real_height)
            self.props.pop("image")
            #self.properties.main.redraw(self.properties.main.widgets[self.properties.main.r])

            #self.properties.main.r.update()

            #print("redrawn")
        self.update()
        self.properties.main.draw_box(self.properties.main.hierarchy.widget)

    def set_compound(self, image):
        self.set_image(image, self.size)
