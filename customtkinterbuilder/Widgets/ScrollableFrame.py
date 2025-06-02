from customtkinter import CTkFrame, CTkScrollbar, CTkFont
from icecream import ic

from customtkinterbuilder.PackArgs import PackArgs

from customtkinterbuilder.widgets import BaseWidgetClass

from typing import Union, Tuple, Optional, Any
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
import tkinter
from customtkinter.windows.widgets.core_widget_classes import CTkBaseClass


class ScrollFrame(CTkFrame):
    def __init__(self, master: Any,
                 width: int = 200,
                 height: int = 200,
                 corner_radius: Optional[Union[int, str]] = None,
                 border_width: Optional[Union[int, str]] = None,

                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 border_color: Optional[Union[str, Tuple[str, str]]] = None,
                 scrollbar_fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 scrollbar_button_color: Optional[Union[str, Tuple[str, str]]] = None,
                 scrollbar_button_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                 label_fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 label_text_color: Optional[Union[str, Tuple[str, str]]] = None,

                 label_text: str = "",
                 label_font: Optional[Union[tuple, CTkFont]] = None,
                 label_anchor: str = "center",
                 orientation: Literal["vertical", "horizontal"] = "vertical"):
        super().__init__(master=master, corner_radius=corner_radius,
                            border_width=border_width, bg_color=bg_color, fg_color=fg_color, border_color=border_color)
        self._desired_width = width
        self._desired_height = height
        outerFrame = self
        canv = tkinter.Canvas(outerFrame, highlightthickness=0)
        self.orientation = orientation
        if self.orientation == "vertical":
            vsb = CTkScrollbar(outerFrame, orientation="vertical", fg_color=scrollbar_fg_color,
                               button_color=scrollbar_button_color, button_hover_color=scrollbar_button_hover_color,
                               command=canv.yview)

            vsb.pack(side="right", fill="y", pady=self.cget("corner_radius") + self.cget("border_width"))
            canv.pack(fill="both", expand=1, anchor="nw",
                      padx=(self.cget("corner_radius") + self.cget("border_width"), 0),
                      pady=self.cget("corner_radius") + self.cget("border_width"))

        else:
            vsb = CTkScrollbar(outerFrame, orientation="horizontal", fg_color=scrollbar_fg_color,
                               button_color=scrollbar_button_color, button_hover_color=scrollbar_button_hover_color,
                               command=canv.xview)

            canv.pack(fill="both", expand=1, anchor="nw",
                      padx=self.cget("corner_radius") + self.cget("border_width"),
                      pady=(self.cget("corner_radius") + self.cget("border_width"), 0))

            vsb.pack(fill="x", padx=self.cget("corner_radius") + self.cget("border_width"))


        frame = tkinter.Frame(canv, highlightthickness=0)
        canv.configure(width=width, height=height)
        wrapFrameId = canv.create_window((0,0), window=frame, anchor="nw")
        if self.orientation == "vertical":
            canv.config(yscrollcommand=vsb.set)
        else:
            canv.config(xscrollcommand=vsb.set)

        canv.bind("<Configure>", lambda event: self.onFrameConfigure())
        canv.bind("<Enter>", lambda event: canv.bind_all("<MouseWheel>", self.on_mouse_wheel)) # on mouse enter
        canv.bind("<Leave>", lambda event: canv.unbind_all("<MouseWheel>")) # on mouse leave
        frame.bind('<Configure>', lambda event: self.onFrameConfigure())
        frame.bind('<Enter>', lambda event: canv.bind_all("<MouseWheel>", self.on_mouse_wheel))
        frame.bind('<Leave>', lambda event: canv.unbind_all("<MouseWheel>"))
        if self.cget("fg_color") == "transparent":
            frame.configure(bg=self._apply_appearance_mode(self.cget("bg_color")))
            canv.configure(bg=self._apply_appearance_mode(self.cget("bg_color")))
        else:
            frame.configure(bg=self._apply_appearance_mode(self.cget("fg_color")))
            canv.configure(bg=self._apply_appearance_mode(self.cget("fg_color")))

        self.outerFrame, self.canv, self.vsb, self.scrollwindow, self.wrapFrameId = outerFrame, canv, vsb, frame, wrapFrameId

    def _set_dimensions(self, width=None, height=None):
        if width is not None:
            self._desired_width = width
        if height is not None:
            self._desired_height = height

        self.canv.configure(width=self._apply_widget_scaling(self._desired_width),
                                      height=self._apply_widget_scaling(self._desired_height))


    def onFrameConfigure(self):
        canv = self.canv
        '''Reset the scroll region to encompass the inner frame'''
        canv.configure(scrollregion=canv.bbox("all"))
        if self.orientation == "vertical":
            canv.itemconfigure(self.wrapFrameId, width=canv.winfo_width())
        else:
            canv.itemconfigure(self.wrapFrameId, height=canv.winfo_height())

    def on_mouse_wheel(self, event, scale=3):
        canv = self.canv
        #only care event.delta is - or +, scroll down or up
        if event.delta<0:
            if self.orientation == "vertical":
                canv.yview_scroll(scale, "units")
            else:
                canv.xview_scroll(scale, "units")

        else:
            if self.orientation == "vertical":
                canv.yview_scroll(-scale, "units")
            else:
                canv.xview_scroll(-scale, "units")


    def _bound_to_mousewheel(self, event):
        self.canv.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canv.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        if self.orientation == "vertical":
            self.canv.yview_scroll(int(-1 * (event.delta / 120)), "units")
        else:
            self.canv.xview_scroll(int(-1 * (event.delta / 120)), "units")

    def get_me(self):
        return self.scrollwindow



    def _set_appearance_mode(self, mode_string):
        super()._set_appearance_mode(mode_string)

        if self.cget("fg_color") == "transparent":
            self.scrollwindow.configure(bg=self._apply_appearance_mode(self.cget("fg_color")))
            self.canv.configure(bg=self._apply_appearance_mode(self.cget("fg_color")))
            #self.configure(bg=self._apply_appearance_mode(self.cget("fg_color")))


        else:
            self.scrollwindow.configure(bg=self._apply_appearance_mode(self.cget("fg_color")))
            self.canv.configure(bg=self._apply_appearance_mode(self.cget("fg_color")))

        self.vsb._set_appearance_mode(mode_string)

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

        if "width" in kwargs:
            self._set_dimensions(width=kwargs.pop("width"))

        if "height" in kwargs:
            self._set_dimensions(height=kwargs.pop("height"))

        if "fg_color" in kwargs:
            super().configure(fg_color=kwargs.pop("fg_color"))

            if self.cget("fg_color") == "transparent":
                self.scrollwindow.configure(bg=self._apply_appearance_mode(self.cget("bg_color")))
                self.canv.configure(bg=self._apply_appearance_mode(self.cget("bg_color")))
                self.vsb.configure(fg_color=self.cget("bg_color"))

            else:
                self.scrollwindow.configure(bg=self._apply_appearance_mode(self.cget("fg_color")))
                self.canv.configure(bg=self._apply_appearance_mode(self.cget("fg_color")))
                self.vsb.configure(fg_color=self.cget("fg_color"))


            for child in self.scrollwindow.winfo_children():
                if isinstance(child, CTkBaseClass):
                    child.configure(bg_color=self.cget("fg_color"))

        if "scrollbar_fg_color" in kwargs:
            new_fg_color = kwargs.pop("scrollbar_fg_color")
            if new_fg_color == "transparent":
                self.vsb.configure(fg_color=self.cget("fg_color"))
                ic("transparent", self.vsb.cget("fg_color"))

            else:
                self.vsb.configure(fg_color=new_fg_color)
                ic("something else", self.vsb.cget("fg_color"))

        if "corner_radius" in kwargs:
            self.canv.pack_forget()
            #self.scrollwindow.destroy()
            self.vsb.pack_forget()
            new_corner_radius = kwargs.pop("corner_radius")
            if self.orientation == "vertical":
                self.vsb.pack(side="right", fill="y", pady=self.cget("corner_radius") + self.cget("border_width"))
                self.canv.pack(fill="both", expand=1, anchor="nw",
                          padx=(self.cget("corner_radius") + self.cget("border_width"), 0),
                          pady=self.cget("corner_radius") + self.cget("border_width"))

            else:
                self.canv.pack(fill="both", expand=1, anchor="nw",
                               padx=self.cget("corner_radius") + self.cget("border_width"),
                               pady=(self.cget("corner_radius") + self.cget("border_width"), 0))

                self.vsb.pack(fill="x", padx=self.cget("corner_radius") + self.cget("border_width"))

            super().configure(corner_radius=new_corner_radius)

        ic(kwargs)
        super().configure(**kwargs)

    def cget(self, attribute_name):
        return CTkFrame.cget(self, attribute_name)
    def winfo_children(self):
        return self.scrollwindow.winfo_children()



class ScrollableFrame(ScrollFrame, PackArgs, BaseWidgetClass):
    def __init__(self, *args, properties, **kwargs):
        super().__init__(*args, **kwargs)
        BaseWidgetClass.__init__(self)
        self.type = "SCROLLABLEFRAME"
        self.properties = properties
        #print(self.properties)
        self.pack_options = {}
        self.self_configure(bg_color="transparent")
        #self.pack_propagate(False)
        #self.configure(bg_color=self.master.cget("fg_color"))
        self.order = 0
        self.num = None
        self.name = None



        #self.bind("<B1-Motion>", self.on_drag_motion)
        self.props = {}
        self.scrollwindow.bind("<MouseWheel>", properties.main.on_vert_mouse)
        self.scrollwindow.bind("<Shift-MouseWheel>", properties.main.on_horiz_mouse)
        self.canv.bind("<MouseWheel>", properties.main.on_vert_mouse)
        self.canv.bind("<Shift-MouseWheel>", properties.main.on_horiz_mouse)

    def __repr__(self):

        return f"{self.type}_{str(self.order)}"

    def get_class(self):
        return "CTkScrollableFrame"


    def get_name(self):
        return self.name.replace(" ", "_")

    def save(self, func, key, val, arg):
        self.props[key] = val
        func(arg)



    def self_configure(self, require_redraw=False, **kwargs):
        kwargs["require_redraw"] = require_redraw
        super().configure(**kwargs)



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
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Width", "SPINBOX", "Width", {"to": 500, "from": 0, "val": int(self.cget("width")), "callback": lambda val: self.save(lambda val: self.self_configure(width=val), "width", int(val), int(val))})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Height", "SPINBOX", "Height", {"to": 500, "from": 0, "val": int(self.cget("height")), "callback": lambda val: self.save(lambda val: self.self_configure(height=val), "height", int(val), int(val))})
        #self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Label Text", "TEXT", "label_text", {"val": self.cget("label_text"), "callback": lambda val: self.save(lambda val: self.self_configure(label_text=val), "label_text", val, val)})

        #self.properties.add_option(self.properties.ARRANGEMENT, "Label Anchor", "COMBO", "label_anchor", {"vals": ["n", "ne", "e", "se", "s", "sw", "w", "nw", "center"], "default": self.cget("label_anchor"), "callback": lambda val: self.save(lambda val: self.self_configure(label_anchor=val), "label_anchor", val, val)})


        #self.properties.add_option(self.properties.STYLES, "Font Family", "FONT_FAMILY", "font_family", {"key": "font_family", "default": self.cget("label_font").cget("family"), "callback": lambda val: self.save(lambda val: self.cget("label_font").configure(family=val), "font_family", val, val)})
        #self.properties.add_option(self.properties.STYLES, "Font Size", "SPINBOX", "font_size", {"to": 500, "from": -500, "val": self.cget("label_font").cget("size"), "callback": lambda val: self.save(lambda val: self.cget("label_font").configure(size=int(val)), "font_size", int(val), int(val))})
        #self.properties.add_option(self.properties.STYLES, "Font Weight", "COMBO", "font_weight", {"vals": ["bold", "normal"], "default": self.cget("label_font").cget("weight"), "callback": lambda val: self.save(lambda val: self.cget("label_font").configure(weight=val), "font_weight", val, val)})
        #self.properties.add_option(self.properties.STYLES, "Font Slant", "COMBO", "font_slant", {"vals": ["italic", "roman"], "default": self.cget("label_font").cget("slant"), "callback": lambda val: self.save(lambda val: self.cget("label_font").configure(slant=val), "font_slant", val, val)})
        #self.properties.add_option(self.properties.STYLES, "Font Underline", "COMBO", "font_underline", {"vals": ["True", "False"], "default": str(bool(self.cget("label_font").cget("underline"))), "callback": lambda val: self.save(lambda val: self.cget("label_font").configure(underline=val), "font_underline", self._bool_change(val), self._bool_change(val))})
        #self.properties.add_option(self.properties.STYLES, "Font Overstrike", "COMBO", "font_overstrike", {"vals": ["True", "False"], "default": str(bool(self.cget("label_font").cget("overstrike"))), "callback": lambda val: self.save(lambda val: self.cget("label_font").configure(overstrike=val), "font_overstrike", self._bool_change(val), self._bool_change(val))})

        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Corner Radius", "SPINBOX", "Corner Radius", {"to": 100, "from": 0, "val": self.cget("corner_radius"), "callback": lambda val: self.save(lambda val: self.self_configure(corner_radius=val), "corner_radius", int(val), int(val))})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Border Width", "SPINBOX", "Border Width", {"to": 100, "from": 0, "val": self.cget("border_width"), "callback": lambda val: self.save(lambda val: self.self_configure(border_width=val), "border_width", int(val), int(val))})
        self.properties.add_option(self.properties.STYLES, "FG Color", "COLOR_COMBO", "fg_color", {"color": self.cget("fg_color"), "key": "fg_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.self_configure(fg_color=val), "fg_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "BG Color", "COLOR_COMBO", "bg_color", {"color": self.cget("bg_color"), "key": "bg_color", "transparent": True, "callback": lambda val: self.save(lambda val: self.self_configure(bg_color=val), "bg_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Border Color", "COLOR_COMBO", "border_color", {"color": self.cget("border_color"), "key": "border_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.self_configure(border_color=val), "border_color", val, val)})
        #self.properties.add_option(self.properties.STYLES, "Scrollbar FG Color", "COLOR_COMBO", "scrollbar_fg_color", {"color": self.cget("scrollbar_fg_color"), "key": "scrollbar_fg_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.self_configure(scrollbar_fg_color=val), "scrollbar_fg_color", val, val)})
        # self.properties.add_option(self.properties.STYLES, "Scrollbar Button Color", "COLOR_COMBO", "scrollbar_button_color", {"color": self.cget("scrollbar_button_color"), "key": "scrollbar_button_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(scrollbar_button_color=val), "scrollbar_button_color", val, val)})
        # self.properties.add_option(self.properties.STYLES, "Scrollbar Button Hover Color", "COLOR_COMBO", "scrollbar_button_hover_color", {"color": self.cget("scrollbar_button_hover_color"), "key": "scrollbar_button_hover_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(scrollbar_button_hover_color=val), "scrollbar_button_hover_color", val, val)})
        #self.properties.add_option(self.properties.STYLES, "Label FG Color", "COLOR_COMBO", "label_fg_color", {"color": self.cget("label_fg_color"), "key": "label_fg_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.self_configure(label_fg_color=val), "label_fg_color", val, val)})
        # self.properties.add_option(self.properties.STYLES, "Label Text Color", "COLOR_COMBO", "label_text_color", {"color": self.cget("label_text_color"), "key": "label_text_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(label_text_color=val), "label_text_color", val, val)})
        # self.properties.add_option(self.properties.ARRANGEMENT, "Orientation", "COMBO", "orientation", {"vals": ["vertical", "horizontal"], "default": self.cget("orientation"), "callback": lambda val: self.save(lambda val: self.configure(orientation=val), "orientation", val, val)})

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