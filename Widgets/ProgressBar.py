from customtkinter import CTkProgressBar
from PackArgs import PackArgs
from widgets import BaseWidgetClass
class ProgressBar(CTkProgressBar, PackArgs, BaseWidgetClass):
    def __init__(self, *args, properties, **kwargs):
        super(ProgressBar, self).__init__(*args, **kwargs)
        BaseWidgetClass.__init__(self)
        self.type = "PROGRESSBAR"
        self.properties = properties
        self.pack_options = {}
        self.pack_propagate(False)
        #self.configure(bg_color=self.master.cget("fg_color"))
        self.order = 0
        self.num = None
        self.name = None

        #self.bind("<B1-Motion>", self.on_drag_motion)
        self.props = {}
        self.bind_mouse(properties)

    def __repr__(self):

        return f"{self.type}_{str(self.order)}"

    def get_class(self):
        return "CTkProgressBar"

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

    def on_drag_start(self, event):
        #self._drag_start_x = event.x
        #self._drag_start_y = event.y
        self.properties.destroy_children()
        #self.properties.add_seperator("Properties")
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "ID", "SINGLELINE_TEXT", "id", {"val": self.name, "callback": lambda val: (self.properties.main.hierarchy.update_text(self.name, val), self.change_name(val))})

        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Width", "SPINBOX", "Width", {"to": 500, "from": 0, "val": int(self.cget("width")), "callback": lambda val: self.save(lambda val: self.configure(width=val), "width", int(val), int(val))})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Height", "SPINBOX", "Height", {"to": 500, "from": 0, "val": int(self.cget("height")), "callback": lambda val: self.save(lambda val: self.configure(height=val), "height", int(val), int(val))})
        # self.configure() Doesn't support it. I will add this option in V2
        # self.properties.add_option(self.properties.STYLES, "Orientation", "COMBO", "orientation", {"vals": ["horizontal", "vertical"], "default": self.cget("orientation"), "callback": lambda val: self.save(lambda val: self.configure(orientation=val), "orientation", val, val)})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Mode", "COMBO", "mode", {"vals": ["determinate", "indeterminate"], "default": self.cget("mode"), "callback": lambda val: self.save(lambda val: self.configure(mode=val), "mode", val, val)})

        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Corner Radius", "SPINBOX", "Corner Radius", {"to": 100, "from": 0, "val": self.cget("corner_radius"), "callback": lambda val: self.save(lambda val: self.configure(corner_radius=val), "corner_radius", int(val), int(val))})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Border Width", "SPINBOX", "Border Width", {"to": 100, "from": 0, "val": self.cget("border_width"), "callback": lambda val: self.save(lambda val: self.configure(border_width=val), "border_width", int(val), int(val))})
        self.properties.add_option(self.properties.STYLES, "FG Color", "COLOR_COMBO", "fg_color", {"color": self.cget("fg_color"), "key": "fg_color", "transparent": True, "callback": lambda val: self.save(lambda val: self.configure(fg_color=val), "fg_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "BG Color", "COLOR_COMBO", "bg_color", {"color": self.cget("bg_color"), "key": "bg_color", "transparent": True, "callback": lambda val: self.save(lambda val: self.configure(bg_color=val), "bg_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Border Color", "COLOR_COMBO", "border_color", {"color": self.cget("border_color"), "key": "border_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(border_color=val), "border_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Progress Color", "COLOR_COMBO", "progress_color", {"color": self.cget("progress_color"), "key": "progress_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(progress_color=val), "progress_color", val, val)})


        self.default()
        self.on_drag_motion(event)  # Some awkward problem

    def set_image(self, img, size):
        if img is not None:
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

            #self.properties.main.redraw(self.properties.main.widgets[self.properties.main.r])

            #self.properties.main.r.update()

            #print("redrawn")
    def set_compound(self, image):
        self.set_image(image, self.size)


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