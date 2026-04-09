from customtkinter import CTkButton, CTkImage
from PIL import Image
from PackArgs import PackArgs
from widgets import BaseWidgetClass


class Button(CTkButton, PackArgs, BaseWidgetClass):
    def __init__(self, *args, properties, **kwargs):
        super().__init__(*args, **kwargs)
        BaseWidgetClass.__init__(self)
        self.type = "BUTTON"
        self.properties = properties
        self.image = None
        self.img = None
        self.size = None
        self.pack_propagate(False)
        #self.configure(bg_color=self.master.cget("fg_color"))

        #self.bind("<B1-Motion>", self.on_drag_motion)
        #print(self._inner_id)
        self.bind_mouse(properties)

    def get_class(self):
        return "CTkButton"

    def get_size(self):
        return self.size

    def on_drag_start(self, event):
        #self._drag_start_x = event.x
        #self._drag_start_y = event.y
        self._begin_drag_start()
        #self.properties.add_seperator("Properties")
        self._add_id_option()
        self._add_size_options()
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Text", "TEXT", "text", {"val": self.cget("text"), "callback": lambda val: self.save(lambda val: self.configure(text=val), "text", val, val)})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Image", "IMAGE", "image", {"image": self.image, "size":self.get_size ,"key": "image", "callback": self.set_image})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Corner Radius", "SPINBOX", "Corner Radius", {"to": 100, "from": 0, "val": self.cget("corner_radius"), "callback": lambda val: self.save(lambda val: self.configure(corner_radius=val), "corner_radius", int(val), int(val))})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Border Width", "SPINBOX", "Border Width", {"to": 100, "from": 0, "val": self.cget("border_width"), "callback": lambda val: self.save(lambda val: self.configure(border_width=val), "border_width", int(val), int(val))})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Border Spacing", "SPINBOX", "border_spacing", {"to": 100, "from": 0, "val": self.cget("border_spacing"), "callback": lambda val: self.save(lambda val: self.configure(border_spacing=val), "border_spacing", int(val), int(val))})

        # Had to reset the image for compound option to take effect
        self.properties.add_option(self.properties.ARRANGEMENT, "Compound", "COMBO", "compound", {"vals": ["top", "bottom", "left", "right"], "default": self.cget("compound"), "callback": lambda val: self.save(lambda val: (self.configure(compound=val, image=None), self.set_compound(self.image)), "compound", val, val)})
        self.properties.add_option(self.properties.ARRANGEMENT, "Anchor", "COMBO", "anchor", {"vals": ["n", "ne", "e", "se", "s", "sw", "w", "nw", "center"], "default": self.cget("anchor"), "callback": lambda val: self.save(lambda val: self.configure(anchor=val, image=None), "anchor", val, val)})

        self._add_font_options()

        self.properties.add_option(self.properties.STYLES, "Hover", "COMBO", "hover", {"vals": ["True", "False"], "default": str(bool(self.cget("hover"))), "callback": lambda val: self.save(lambda val: self.configure(hover=val), "hover", self._bool_change(val), self._bool_change(val))})
        self.properties.add_option(self.properties.STYLES, "State", "COMBO", "state", {"vals": ["normal", "disabled"], "default": self.cget("state"), "callback": lambda val: self.save(lambda val: self.configure(state=val), "state", val, val)})

        self.properties.add_option(self.properties.STYLES, "FG Color", "COLOR_COMBO", "fg_color", {"color": self.cget("fg_color"), "key": "fg_color", "transparent": True, "callback": lambda val: self.save(lambda val: self.configure(fg_color=val), "fg_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "BG Color", "COLOR_COMBO", "bg_color", {"color": self.cget("bg_color"), "key": "bg_color", "transparent": True, "callback": lambda val: self.save(lambda val: self.configure(bg_color=val), "bg_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Border Color", "COLOR_COMBO", "border_color", {"color": self.cget("border_color"), "key": "border_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(border_color=val), "border_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Hover Color", "COLOR_COMBO", "hover_color", {"color": self.cget("hover_color"), "key": "hover_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(hover_color=val), "hover_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Text Color", "COLOR_COMBO", "text_color", {"color": self.cget("text_color"), "key": "text_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(text_color=val), "text_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Text Disabled Color", "COLOR_COMBO", "text_color_disabled", {"color": self.cget("text_color_disabled"), "key": "text_color_disabled", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(text_color_disabled=val), "text_color_disabled", val, val)})

        self.default()
        self.on_drag_motion(event)  # Some awkward problem

    def set_image(self, img, size):
        if img != "":
            self.image = img
            img = Image.open(img)
            img = CTkImage(light_image=img, dark_image=img, size=size)

            # Image is not updating. Changing the width is the workaround I found. Need to change this if possible
            self.configure(image=img, width=int(self.cget("width"))+1)
            self.configure(width=int(self.cget("width"))-1)
            self.img = img
            self.size = size
            self.props["image"] = img
            #print("🎆", self.size)
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
            self.configure(image=None, width=with_img_width, height=with_img_height)
            self.update()
            self.configure(width=real_width, height=real_height)
            self.size = None
            self.props.pop("image")

            #self.properties.main.redraw(self.properties.main.widgets[self.properties.main.r])

            #self.properties.main.r.update()

            #print("redrawn")
        self.update()
        self.properties.main.draw_box(self.properties.main.hierarchy.widget)

    def set_compound(self, image):
        self.set_image(image, self.size)
