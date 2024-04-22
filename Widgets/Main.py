from customtkinter import CTkFrame, CTkImage
from PIL import Image
from widgets import BaseWidgetClass
class Main(CTkFrame, BaseWidgetClass):
    def __init__(self, *args, properties, **kwargs):
        super().__init__(*args, **kwargs)
        BaseWidgetClass.__init__(self)
        self.type = "MAIN"
        self.properties = properties
        self.image = None
        self.img = None
        self.size = None
        self.pack_options = {}
        self.pack_propagate(False)
        #self.configure(bg_color=self.master.cget("fg_color"))
        self.order = 0
        self.num = None
        self.name = None

        #self.bind("<B1-Motion>", self.on_drag_motion)
        self.props = {}

    def __repr__(self):

        return f"{self.type}_{str(self.order)}"

    def get_class(self):
        return "CTk"

    def get_name(self):
        return self.name.replace(" ", "_")

    def save(self, func, key, val, arg):
        self.props[key] = val
        func(arg)
        if key in ["width", "height"]:
            main = self.properties.main
            main_window_panel = main.r.master.master
            main_window = main.r
            visible_area = main_window_panel.winfo_height()
            content_height = main_window.cget("height")
            hidden_area = (content_height - visible_area)
            offset = hidden_area // 2
            offset += 50
            print(offset, hidden_area, content_height, visible_area)

            main.vert_max_offset = abs(offset)

            visible_area = main_window_panel.winfo_width()
            content_height = main_window.cget("width")
            hidden_area = (content_height - visible_area)
            offset = hidden_area // 2
            offset += 50
            print(offset, hidden_area, content_height, visible_area)

            # self.vert_scrlbar.set(scrollbar_position, scrollbar_height+scrollbar_position)

            main.horiz_max_offset = abs(offset)

            main.horiz_scrl.set(0)
            main.vert_scrl.set(0)
            main_window.place(x=0, y=0)

    def configure(self, require_redraw=False, **kwargs):
        print(kwargs)
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
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Width", "SPINBOX", "Width", {"to": 500, "from": 0, "val": int(self.cget("width")), "callback": lambda val: self.save(lambda val: self.configure(width=val), "width", int(val), int(val))})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Height", "SPINBOX", "Height", {"to": 500, "from": 0, "val": int(self.cget("height")), "callback": lambda val: self.save(lambda val: self.configure(height=val), "height", int(val), int(val))})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Title", "TEXT", "title", {"val": self.properties.main.title, "callback": lambda val: self.save(lambda val: self.properties.main.change(title=val), "title", val, val)})
        self.properties.add_option(self.properties.STYLES, "FG Color", "COLOR_COMBO", "fg_color", {"color": self.cget("fg_color"), "key": "fg_color", "transparent": True, "callback": lambda val: self.save(lambda val: self.configure(fg_color=val), "fg_color", val, val)})

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
            print("🎆", self.size)
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

            print("redrawn")
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