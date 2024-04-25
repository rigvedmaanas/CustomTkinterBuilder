from customtkinter import CTkScrollableFrame, CTkLabel, CTkFrame, CTkScrollbar, CTkFont, CTkCanvas
from icecream import ic

from PackArgs import PackArgs
from tkinter import Canvas, Frame
from tkinter.ttk import Scrollbar

from widgets import BaseWidgetClass

from typing import Union, Tuple, Optional, Any
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
import tkinter
import sys

from customtkinter.windows.widgets.appearance_mode.appearance_mode_base_class import CTkAppearanceModeBaseClass
from customtkinter.windows.widgets.scaling.scaling_base_class import CTkScalingBaseClass
from customtkinter.windows.widgets.core_widget_classes import CTkBaseClass
from customtkinter.windows.widgets.theme.theme_manager import ThemeManager

"""
class CTkScrollableFrameCustomMade(CTkFrame, CTkAppearanceModeBaseClass, CTkScalingBaseClass):
    def __init__(self,
                 master: Any,
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

        self._orientation = orientation

        # dimensions independent of scaling
        self._desired_width = width  # _desired_width and _desired_height, represent desired size set by width and height
        self._desired_height = height
        CTkFrame.__init__(self, master=master, width=0, height=0, corner_radius=corner_radius,
                                      border_width=border_width, bg_color=bg_color, fg_color=fg_color, border_color=border_color)

        self._parent_canvas = tkinter.Canvas(master=self, highlightthickness=0)
        self._parent_frame = tkinter.Frame(master=self._parent_canvas, highlightthickness=0)

        self._set_scroll_increments()

        if self._orientation == "horizontal":
            self._scrollbar = CTkScrollbar(master=self, orientation="horizontal", command=self._parent_canvas.xview,
                                           fg_color=scrollbar_fg_color, button_color=scrollbar_button_color, button_hover_color=scrollbar_button_hover_color, bg_color="white")
            self._parent_canvas.configure(xscrollcommand=self._scrollbar.set)
        elif self._orientation == "vertical":
            self._scrollbar = CTkScrollbar(master=self, orientation="vertical", command=self._parent_canvas.yview,
                                           fg_color=scrollbar_fg_color, button_color=scrollbar_button_color, button_hover_color=scrollbar_button_hover_color, bg_color="white")
            self._parent_canvas.configure(yscrollcommand=self._scrollbar.set)

        self._label_text = label_text
        self._label = CTkLabel(self, text=label_text, anchor=label_anchor, font=label_font,
                               corner_radius=self.cget("corner_radius"), text_color=label_text_color,
                               fg_color=ThemeManager.theme["CTkScrollableFrame"]["label_fg_color"] if label_fg_color is None else label_fg_color)

        #tkinter.Frame.__init__(self, master=self._parent_canvas, highlightthickness=0)
        CTkAppearanceModeBaseClass.__init__(self)
        CTkScalingBaseClass.__init__(self, scaling_type="widget")

        self._create_grid()

        self._parent_canvas.configure(width=self._apply_widget_scaling(self._desired_width),
                                      height=self._apply_widget_scaling(self._desired_height))

        self._parent_frame.bind("<Configure>", lambda e: self._parent_canvas.configure(scrollregion=self._parent_canvas.bbox("all")))
        self._parent_canvas.bind("<Configure>", self._fit_frame_dimensions_to_canvas)
        self._parent_frame.bind_all("<MouseWheel>", self._mouse_wheel_all, add="+")
        self._parent_frame.bind_all("<KeyPress-Shift_L>", self._keyboard_shift_press_all, add="+")
        self._parent_frame.bind_all("<KeyPress-Shift_R>", self._keyboard_shift_press_all, add="+")
        self._parent_frame.bind_all("<KeyRelease-Shift_L>", self._keyboard_shift_release_all, add="+")
        self._parent_frame.bind_all("<KeyRelease-Shift_R>", self._keyboard_shift_release_all, add="+")
        self._create_window_id = self._parent_canvas.create_window(0, 0, window=self, anchor="nw")

        if self.cget("fg_color") == "transparent":
            CTkFrame.configure(self, bg_color=self._apply_appearance_mode(self.cget("bg_color")))
            self._parent_canvas.configure(bg=self._apply_appearance_mode(self.cget("bg_color")))
        else:
            CTkFrame.configure(self, bg_color=self._apply_appearance_mode(self.cget("fg_color")))
            self._parent_canvas.configure(bg=self._apply_appearance_mode(self.cget("fg_color")))

        self._shift_pressed = False

    def destroy(self):
        CTkFrame.destroy(self)
        CTkAppearanceModeBaseClass.destroy(self)
        CTkScalingBaseClass.destroy(self)

    def _create_grid(self):
        border_spacing = self._apply_widget_scaling(self.cget("corner_radius") + self.cget("border_width"))

        if self._orientation == "horizontal":
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(1, weight=1)
            self._parent_canvas.grid(row=1, column=0, sticky="nsew", padx=border_spacing, pady=(border_spacing, 0))
            self._scrollbar.grid(row=2, column=0, sticky="nsew", padx=border_spacing)

            if self._label_text is not None and self._label_text != "":
                self._label.grid(row=0, column=0, sticky="ew", padx=border_spacing, pady=border_spacing)
            else:
                self._label.grid_forget()

        elif self._orientation == "vertical":
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(1, weight=1)
            self._parent_canvas.grid(row=1, column=0, sticky="nsew", padx=(border_spacing, 0), pady=border_spacing)
            self._scrollbar.grid(row=1, column=1, sticky="nsew", pady=border_spacing)

            if self._label_text is not None and self._label_text != "":
                self._label.grid(row=0, column=0, columnspan=2, sticky="ew", padx=border_spacing, pady=border_spacing)
            else:
                self._label.grid_forget()

    def _set_appearance_mode(self, mode_string):
        super()._set_appearance_mode(mode_string)

        if self.cget("fg_color") == "transparent":
            CTkFrame.configure(self, bg_color=self._apply_appearance_mode(self.cget("bg_color")))
            self.configure(bg_color=self._apply_appearance_mode(self.cget("bg_color")))
        else:
            CTkFrame.configure(self, bg_color=self._apply_appearance_mode(self.cget("fg_color")))
            self.configure(bg_color=self._apply_appearance_mode(self.cget("fg_color")))

    def _set_scaling(self, new_widget_scaling, new_window_scaling):
        super()._set_scaling(new_widget_scaling, new_window_scaling)

        self._parent_canvas.configure(width=self._apply_widget_scaling(self._desired_width),
                                      height=self._apply_widget_scaling(self._desired_height))

    def _set_dimensions(self, width=None, height=None):
        if width is not None:
            self._desired_width = width
        if height is not None:
            self._desired_height = height

        self._parent_canvas.configure(width=self._apply_widget_scaling(self._desired_width),
                                      height=self._apply_widget_scaling(self._desired_height))

    def parent_frame_configure(self, **kwargs):
        if "width" in kwargs:
            self._set_dimensions(width=kwargs.pop("width"))

        if "height" in kwargs:
            self._set_dimensions(height=kwargs.pop("height"))

        if "corner_radius" in kwargs:
            new_corner_radius = kwargs.pop("corner_radius")
            self.configure(corner_radius=new_corner_radius)
            if self._label is not None:
                self._label.configure(corner_radius=new_corner_radius)
            self._create_grid()

        if "border_width" in kwargs:
            self.configure(border_width=kwargs.pop("border_width"))
            self._create_grid()

        if "fg_color" in kwargs:
            self.configure(fg_color=kwargs.pop("fg_color"))

            if self.cget("fg_color") == "transparent":
                CTkFrame.configure(self, bg=self._apply_appearance_mode(self.cget("bg_color")))
                self._parent_canvas.configure(bg=self._apply_appearance_mode(self.cget("bg_color")))
            else:
                CTkFrame.configure(self, bg=self._apply_appearance_mode(self.cget("fg_color")))
                self._parent_canvas.configure(bg=self._apply_appearance_mode(self.cget("fg_color")))

            for child in self.winfo_children():
                if isinstance(child, CTkBaseClass):
                    child.configure(bg_color=self.cget("fg_color"))

        if "scrollbar_fg_color" in kwargs:
            self._scrollbar.configure(fg_color=kwargs.pop("scrollbar_fg_color"))

        if "scrollbar_button_color" in kwargs:
            self._scrollbar.configure(button_color=kwargs.pop("scrollbar_button_color"))

        if "scrollbar_button_hover_color" in kwargs:
            self._scrollbar.configure(button_hover_color=kwargs.pop("scrollbar_button_hover_color"))

        if "label_text" in kwargs:
            self._label_text = kwargs.pop("label_text")
            self._label.configure(text=self._label_text)
            self._create_grid()

        if "label_font" in kwargs:
            self._label.configure(font=kwargs.pop("label_font"))

        if "label_text_color" in kwargs:
            self._label.configure(text_color=kwargs.pop("label_text_color"))

        if "label_fg_color" in kwargs:
            self._label.configure(fg_color=kwargs.pop("label_fg_color"))

        if "label_anchor" in kwargs:
            self._label.configure(anchor=kwargs.pop("label_anchor"))

        self.configure(**kwargs)

    def parent_frame_cget(self, attribute_name: str):
        if attribute_name == "width":
            return self._desired_width
        elif attribute_name == "height":
            return self._desired_height

        elif attribute_name == "label_text":
            return self._label_text
        elif attribute_name == "label_font":
            return self._label.cget("font")
        elif attribute_name == "label_text_color":
            return self._label.cget("_text_color")
        elif attribute_name == "label_fg_color":
            return self._label.cget("fg_color")
        elif attribute_name == "label_anchor":
            return self._label.cget("anchor")

        elif attribute_name.startswith("scrollbar_fg_color"):
            return self._scrollbar.cget("fg_color")
        elif attribute_name.startswith("scrollbar_button_color"):
            return self._scrollbar.cget("button_color")
        elif attribute_name.startswith("scrollbar_button_hover_color"):
            return self._scrollbar.cget("button_hover_color")

        else:
            return self.cget(attribute_name)



    def _fit_frame_dimensions_to_canvas(self, event):
        if self._orientation == "horizontal":
            self._parent_canvas.itemconfigure(self._create_window_id, height=self._parent_canvas.winfo_height())
        elif self._orientation == "vertical":
            self._parent_canvas.itemconfigure(self._create_window_id, width=self._parent_canvas.winfo_width())

    def _set_scroll_increments(self):
        if sys.platform.startswith("win"):
            self._parent_canvas.configure(xscrollincrement=1, yscrollincrement=1)
        elif sys.platform == "darwin":
            self._parent_canvas.configure(xscrollincrement=4, yscrollincrement=8)

    def _mouse_wheel_all(self, event):
        if self.check_if_master_is_canvas(event.widget):
            if sys.platform.startswith("win"):
                if self._shift_pressed:
                    if self._parent_canvas.xview() != (0.0, 1.0):
                        self._parent_canvas.xview("scroll", -int(event.delta / 6), "units")
                else:
                    if self._parent_canvas.yview() != (0.0, 1.0):
                        self._parent_canvas.yview("scroll", -int(event.delta / 6), "units")
            elif sys.platform == "darwin":
                if self._shift_pressed:
                    if self._parent_canvas.xview() != (0.0, 1.0):
                        self._parent_canvas.xview("scroll", -event.delta, "units")
                else:
                    if self._parent_canvas.yview() != (0.0, 1.0):
                        self._parent_canvas.yview("scroll", -event.delta, "units")
            else:
                if self._shift_pressed:
                    if self._parent_canvas.xview() != (0.0, 1.0):
                        self._parent_canvas.xview("scroll", -event.delta, "units")
                else:
                    if self._parent_canvas.yview() != (0.0, 1.0):
                        self._parent_canvas.yview("scroll", -event.delta, "units")

    def _keyboard_shift_press_all(self, event):
        self._shift_pressed = True

    def _keyboard_shift_release_all(self, event):
        self._shift_pressed = False

    def check_if_master_is_canvas(self, widget):
        if widget == self._parent_canvas:
            return True
        elif widget.master is not None:
            return self.check_if_master_is_canvas(widget.master)
        else:
            return False

    def pack(self, **kwargs):
        self._parent_frame.pack(**kwargs)

    def place(self, **kwargs):
        self.place(**kwargs)

    def grid(self, **kwargs):
        self.grid(**kwargs)

    def pack_forget(self):
        self.pack_forget()

    def place_forget(self, **kwargs):
        self.place_forget()

    def grid_forget(self, **kwargs):
        self.grid_forget()

    def grid_remove(self, **kwargs):
        self.grid_remove()

    def grid_propagate(self, **kwargs):
        self.grid_propagate()

    def grid_info(self, **kwargs):
        return self.grid_info()

    def lift(self, aboveThis=None):
        self.lift(aboveThis)

    def lower(self, belowThis=None):
        self.lower(belowThis)"""

class ScrollFrame(CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        outerFrame = self
        canv = CTkCanvas(outerFrame, highlightthickness=0)
        vsb = CTkScrollbar(outerFrame, orientation="vertical", command=canv.yview)
        vsb.pack(side="right", fill="y")
        canv.pack(fill="both", expand=1, anchor="nw")
        kwargs.pop("master")
        frame = CTkFrame(canv, **kwargs)
        wrapFrameId = canv.create_window((0,0), window=frame, anchor="nw")
        canv.config(yscrollcommand=vsb.set)
        canv.bind("<Configure>", lambda event: self.onFrameConfigure())
        canv.bind("<Enter>", lambda event: canv.bind_all("<MouseWheel>", self.on_mouse_wheel)) # on mouse enter
        canv.bind("<Leave>", lambda event: canv.unbind_all("<MouseWheel>")) # on mouse leave
        frame.bind('<Configure>', lambda event: self.onFrameConfigure())
        frame.bind('<Enter>', lambda event: canv.bind_all("<MouseWheel>", self.on_mouse_wheel))
        frame.bind('<Leave>', lambda event: canv.unbind_all("<MouseWheel>"))
        self.outerFrame, self.canv, self.vsb, self.scrollwindow, self.wrapFrameId = outerFrame, canv, vsb, frame, wrapFrameId
    def onFrameConfigure(self):
        canv = self.canv
        '''Reset the scroll region to encompass the inner frame'''
        canv.configure(scrollregion=canv.bbox("all"))
        canv.itemconfigure(self.wrapFrameId, width=canv.winfo_width())
    def on_mouse_wheel(self, event, scale=3):
        canv = self.canv
        #only care event.delta is - or +, scroll down or up
        if event.delta<0:
            canv.yview_scroll(scale, "units")
        else:
            canv.yview_scroll(-scale, "units")

    def _bound_to_mousewheel(self, event):
        self.canv.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canv.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canv.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def get_me(self):
        return self.scrollwindow


    def _set_appearance_mode(self, mode):
        pass

    def configure(self, **kwargs):
        if "label_fg_color" in kwargs:
            kwargs.pop("label_fg_color")

        if "bg_color" in kwargs:
            kwargs.pop("bg_color")

        if "label_text" in kwargs:
            kwargs.pop("label_text")
        CTkFrame.configure(self, **kwargs)

    def cget(self, attribute_name):
        if attribute_name in ["label_text"]:
            pass
        else:
            return CTkFrame.cget(self, attribute_name)
    def winfo_children(self):
        return self.scrollwindow.winfo_children()


class ScrolledWindow(CTkFrame):
    """
    1. Master widget gets scrollbars and a canvas. Scrollbars are connected
    to canvas scrollregion.

    2. self.scrollwindow is created and inserted into canvas

    Usage Guideline:
    Assign any widgets as children of <ScrolledWindow instance>.scrollwindow
    to get them inserted into canvas

    __init__(self, parent, canv_w = 400, canv_h = 400, *args, **kwargs)
    docstring:
    Parent = master of scrolled window
    canv_w - width of canvas
    canv_h - height of canvas

    """


    def __init__(self, parent, canv_w = 400, canv_h = 400, *args, **kwargs):
        """Parent = master of scrolled window
        canv_w - width of canvas
        canv_h - height of canvas

       """
        super().__init__(parent, *args, **kwargs)

        self.parent = self
        self.pack_propagate(False)
        # creating a scrollbars
        self.xscrlbr = CTkScrollbar(self.parent, orientation='horizontal')
        self.xscrlbr.grid(column=0, row=1, sticky='ew', columnspan=2)
        self.yscrlbr = CTkScrollbar(self.parent, orientation='vertical')
        self.yscrlbr.grid(column=1, row=0, sticky='ns')
        # creating a canvas
        self.canv = CTkCanvas(self.parent, bg="yellow")
        self.canv.configure(relief='flat',
                         width=10,
                         height=10, bd=2)
        # placing a canvas into frame
        self.canv.grid(column=0, row=0, sticky='nsew')
        # accociating scrollbar comands to canvas scroling
        self.xscrlbr.configure(command = self.canv.xview)
        self.yscrlbr.configure(command = self.canv.yview)

        # creating a frame to inserto to canvas
        self.scrollwindow = CTkFrame(self.parent)

        self.canv.create_window(0, 0, window = self.scrollwindow, anchor = 'nw')

        self.canv.config(xscrollcommand = self.xscrlbr.set,
                         yscrollcommand = self.yscrlbr.set,
                         scrollregion = (0, 0, 100, 100))

        self.yscrlbr.lift(self.scrollwindow)
        self.xscrlbr.lift(self.scrollwindow)
        self.scrollwindow.bind('<Configure>', self._configure_window)
        self.scrollwindow.bind('<Enter>', self._bound_to_mousewheel)
        self.scrollwindow.bind('<Leave>', self._unbound_to_mousewheel)
        self.canv.pack_propagate(False)
        self.canv.grid_propagate(False)

        return
    def get_me(self):
        return self.scrollwindow

    def _bound_to_mousewheel(self, event):
        self.canv.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canv.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canv.yview_scroll(int(-1*(event.delta/120)), "units")

    def _configure_window(self, event):
        # update the scrollbars to match the size of the inner frame
        size = (self.scrollwindow.winfo_reqwidth(), self.scrollwindow.winfo_reqheight())
        ic(size)
        self.canv.configure(scrollregion=(0, 0, size[0], size[1]))
        if self.scrollwindow.winfo_reqwidth() != self.canv.winfo_width():
            # update the canvas's width to fit the inner frame
            self.canv.configure(width = self.scrollwindow.winfo_reqwidth())
        if self.scrollwindow.winfo_reqheight() != self.canv.winfo_height():
            # update the canvas's width to fit the inner frame
            self.canv.configure(height = self.scrollwindow.winfo_reqheight())

    def _set_appearance_mode(self, mode):
        pass

    def configure(self, **kwargs):
        if "label_fg_color" in kwargs:
            kwargs.pop("label_fg_color")

        if "bg_color" in kwargs:
            kwargs.pop("bg_color")

        if "label_text" in kwargs:
            kwargs.pop("label_text")
        CTkFrame.configure(self, **kwargs)

    def cget(self, attribute_name):
        if attribute_name in ["label_text"]:
            pass
        else:
            return CTkFrame.cget(self, attribute_name)
    def winfo_children(self):
        return self.scrollwindow.winfo_children()



class ScrollableFrame(ScrollFrame, PackArgs, BaseWidgetClass):
    def __init__(self, *args, properties, **kwargs):
        super().__init__(*args, **kwargs)
        BaseWidgetClass.__init__(self)
        self.type = "SCROLLABLEFRAME"
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
        return "CTkScrollableFrame"

    def get_name(self):
        return self.name.replace(" ", "_")

    def save(self, func, key, val, arg):
        self.props[key] = val
        func(arg)

    def self_configure(self, require_redraw=False, **kwargs):
        #print(kwargs)
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
        self.properties.add_option(self.properties.STYLES, "FG Color", "COLOR_COMBO", "fg_color", {"color": self.cget("fg_color"), "key": "fg_color", "transparent": True, "callback": lambda val: self.save(lambda val: self.self_configure(fg_color=val), "fg_color", val, val)})
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