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
        self.pack_propagate(False)
        #self.configure(bg_color=self.master.cget("fg_color"))

        #self.bind("<B1-Motion>", self.on_drag_motion)

    def _set_appearance_mode(self, mode_string):
        bg_color = ("grey10", "grey80")
        self.configure(bg_color=bg_color[self.properties.main.appearance.get()])
        super()._set_appearance_mode(mode_string)

    def get_class(self):
        return "CTk"

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
            #print(offset, hidden_area, content_height, visible_area)

            main.vert_max_offset = abs(offset)

            visible_area = main_window_panel.winfo_width()
            content_height = main_window.cget("width")
            hidden_area = (content_height - visible_area)
            offset = hidden_area // 2
            offset += 50
            #print(offset, hidden_area, content_height, visible_area)

            # self.vert_scrlbar.set(scrollbar_position, scrollbar_height+scrollbar_position)

            main.horiz_max_offset = abs(offset)

            main.horiz_scrl.set(0)
            main.vert_scrl.set(0)
            main_window.place(x=0, y=0)

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
