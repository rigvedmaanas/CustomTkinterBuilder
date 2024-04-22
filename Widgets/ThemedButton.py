from icecream import ic

from Widgets.Button import Button
from customtkinter import CTkButton, CTkImage, CTkFont
import tkinter
from PackArgs import PackArgs
from widgets import BaseWidgetClass
from PIL import Image, ImageTk
from typing import Union, Tuple, Callable, Optional, Any
from customtkinter.windows.widgets.theme.theme_manager import ThemeManager
class Button_1(Button):
    def __init__(self, *args, properties, **kwargs):
        super().__init__(*args, properties=properties, **kwargs)

    def pack(self, **kwargs):
        super().pack(**kwargs)
        self.save(lambda val: self.configure(text=val), "text", "Button 1", "Button 1")
        self.save(lambda val: self.cget("font").configure(size=val), "font_size", int(15), int(15))
        self.save(lambda val: self.cget("font").configure(weight=val), "font_weight", "normal", "normal")
        # 140x38
        self.save(lambda val: self.configure(width=val), "width", 140, 140)
        self.save(lambda val: self.configure(height=val), "height", 38, 38)
        self.save(lambda val: self.configure(corner_radius=val), "corner_radius", 3, 3)
        self.save(lambda val: self.configure(fg_color=val), "fg_color", ["#797979", "#000000"], ["#797979", "#000000"])
        self.save(lambda val: self.configure(hover_color=val), "hover_color", ["#4e4e4e", "#434343"], ["#4e4e4e", "#434343"])
        self.save(lambda val: self.configure(border_color=val), "border_color", ["#000000", "#a2a2a2"], ["#000000", "#a2a2a2"])
        self.save(lambda val: self.configure(border_width=val), "border_width", 1, 1)

class CTkAdvancedButton(CTkButton):
    def __init__(self,
                 master: Any,
                 width: int = 140,
                 height: int = 38,
                 corner_radius: Optional[int] = None,
                 hover_corner_radius: Optional[int] = None,
                 border_width: Optional[int] = None,
                 hover_border_width: Optional[int] = None,
                 border_spacing: int = 2,
                 hover_border_spacing: int = 2,

                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,

                 hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                 border_color: Optional[Union[str, Tuple[str, str]]] = None,
                 hover_border_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 hover_text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color_disabled: Optional[Union[str, Tuple[str, str]]] = None,

                 background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None,
                 round_width_to_even_numbers: bool = True,
                 round_height_to_even_numbers: bool = True,

                 text: str = "CTkAdvancedButton",
                 hover_text: str = "CTkAdvancedButton",
                 font: Optional[Union[tuple, CTkFont]] = None,
                 hover_font: Optional[Union[tuple, CTkFont]] = None,
                 textvariable: Union[tkinter.Variable, None] = None,
                 hover_image: Union[CTkImage, "ImageTk.PhotoImage", None] = None,
                 image: Union[CTkImage, "ImageTk.PhotoImage", None] = None,
                 state: str = "normal",
                 hover: bool = True,
                 command: Union[Callable[[], Any], None] = None,
                 compound: str = "left",
                 anchor: str = "center",
                 **kwargs):


        super().__init__(master, width, height, corner_radius, border_width, border_spacing, bg_color, fg_color,
                         hover_color, border_color, text_color, text_color_disabled, background_corner_colors,
                         round_width_to_even_numbers, round_height_to_even_numbers, text, font, textvariable, image,
                         state, hover, command, compound, anchor, **kwargs)


        self._hover_corner_radius: int = ThemeManager.theme["CTkButton"][
            "corner_radius"] if hover_corner_radius is None else hover_corner_radius
        self._hover_corner_radius = min(self._hover_corner_radius, round(self._current_height / 2))


        self._hover_border_width: int = ThemeManager.theme["CTkButton"][
            "border_width"] if hover_border_width is None else hover_border_width
        self._hover_border_spacing: int = hover_border_spacing

        # color
        self._hover_border_color: Union[str, Tuple[str, str]] = ThemeManager.theme["CTkButton"][
            "border_color"] if hover_border_color is None else self._check_color_type(hover_border_color)
        self._hover_text_color: Union[str, Tuple[str, str]] = ThemeManager.theme["CTkButton"][
            "text_color"] if hover_text_color is None else self._check_color_type(hover_text_color)
        self._text_color_disabled: Union[str, Tuple[str, str]] = ThemeManager.theme["CTkButton"][
            "text_color_disabled"] if text_color_disabled is None else self._check_color_type(text_color_disabled)

        # text, font
        self._text = text
        self._hover_text = hover_text
        self._hover_font: Union[tuple, CTkFont] = CTkFont() if hover_font is None else self._check_font_type(hover_font)
        if isinstance(self._hover_font, CTkFont):
            self._hover_font.add_size_configure_callback(self._update_font)

        # image
        self._hover_image = self._check_image_type(hover_image)
        if isinstance(self._hover_image, CTkImage):
            self._hover_image.add_configure_callback(self._update_image)

        self._hover_options = {"hover_corner_radius": self._hover_corner_radius,
                               "hover_border_width": self._hover_border_width,
                               "hover_border_spacing": self._hover_border_spacing,
                               "hover_border_color": self._hover_border_color,
                               "hover_text_color": self._hover_text_color,
                               "hover_text": self._hover_text,
                               "hover_font": self._hover_font,
                               "hover_image": self._hover_image}

        self._normal_options = {"corner_radius": self._corner_radius,
                                    "border_width": self._border_width,
                                    "border_spacing": self._border_spacing,
                                    "border_color": self._border_color,
                                    "text_color": self._text_color,
                                    "text": self._text,
                                    "font": self._font,
                                    "image": self._image}


    def configure(self, require_redraw=False, stop_saving_hover=False, stop_saving_normal=False, **kwargs):

        if "hover_corner_radius" in kwargs:
            self._hover_corner_radius = kwargs.pop("hover_corner_radius")
            self._create_grid()
            require_redraw = True

        if "hover_border_width" in kwargs:
            self._hover_border_width = kwargs.pop("hover_border_width")
            self._create_grid()
            require_redraw = True

        if "hover_border_spacing" in kwargs:
            self._hover_border_spacing = kwargs.pop("hover_border_spacing")
            self._create_grid()
            require_redraw = True

        if "hover_border_color" in kwargs:
            self._hover_border_color = self._check_color_type(kwargs.pop("hover_border_color"))
            require_redraw = True


        if "hover_text" in kwargs:
            self._hover_text = kwargs.pop("hover_text")
            if self._text_label is None:
                require_redraw = True  # text_label will be created in .draw()


        if "hover_font" in kwargs:
            if isinstance(self._hover_font, CTkFont):
                self._hover_font.remove_size_configure_callback(self._update_font)
            self._hover_font = self._check_font_type(kwargs.pop("hover_font"))
            if isinstance(self._hover_font, CTkFont):
                self._hover_font.add_size_configure_callback(self._update_font)

            self._update_font()

        if "hover_image" in kwargs:
            if isinstance(self._hover_image, CTkImage):
                self._hover_image.remove_configure_callback(self._update_image)
            self._hover_image = self._check_image_type(kwargs.pop("hover_image"))
            if isinstance(self._hover_image, CTkImage):
                self._hover_image.add_configure_callback(self._update_image)
            self._update_image()

        if "hover_text_color" in kwargs:
            self._hover_text_color = self._check_color_type(kwargs.pop("hover_text_color"))
            require_redraw = True

        if not stop_saving_hover:
            self._hover_options = {"hover_corner_radius": self._hover_corner_radius,
                                   "hover_border_width": self._hover_border_width,
                                   "hover_border_spacing": self._hover_border_spacing,
                                   "hover_border_color": self._hover_border_color,
                                   "hover_text_color": self._hover_text_color,
                                   "hover_text": self._hover_text,
                                   "hover_font": self._hover_font,
                                   "hover_image": self._hover_image}

        super().configure(require_redraw=True, **kwargs)

        if not stop_saving_normal:
            self._normal_options = {"corner_radius": self._corner_radius,
                                    "border_width": self._border_width,
                                    "border_spacing": self._border_spacing,
                                    "border_color": self._border_color,
                                    "text_color": self._text_color,
                                    "text": self._text,
                                    "font": self._font,
                                    "image": self._image}
        if self._text_label != None:
            self._text_label.bind("<Enter>", self._on_enter)
            self._text_label.bind("<Leave>", self._on_enter)

        if self._image_label != None:
            self._image_label.bind("<Enter>", self._on_enter)
            self._image_label.bind("<Leave>", self._on_enter)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "hover_corner_radius":
            return self._hover_corner_radius
        elif attribute_name == "hover_border_width":
            return self._hover_border_width
        elif attribute_name == "hover_border_spacing":
            return self._hover_border_spacing

        elif attribute_name == "hover_border_color":
            return self._hover_border_color
        elif attribute_name == "hover_text_color":
            return self._hover_text_color

        elif attribute_name == "hover_text":
            return self._hover_text
        elif attribute_name == "hover_font":
            return self._hover_font

        elif attribute_name == "hover_image":
            return self._hover_image
        else:
            return super().cget(attribute_name)

    def _on_enter(self, event=None):
        h = dict(self._hover_options)
        for key in list(h.keys()):
            k = key.replace("hover_", "")

            if h[key] != self._normal_options[k]:
                self.configure(**{k: self._hover_options[key]}, stop_saving_normal=True, stop_saving_hover=False)
        super()._on_enter(event=event)

    def _on_leave(self, event=None):
        h = dict(self._normal_options)
        for key in list(h.keys()):
            self.configure(**{key: h[key]}, stop_saving_normal=False, stop_saving_hover=True)
        super()._on_leave(event=event)


class AdvancedButton(CTkAdvancedButton, PackArgs, BaseWidgetClass):
    def __init__(self, *args, properties, **kwargs):
        super().__init__(*args, **kwargs)
        BaseWidgetClass.__init__(self)
        self.type = "ADVANCEDBUTTON"
        self.properties = properties
        self.image = None
        self.img = None
        self.size = None

        self.hover_image = None
        self.hover_img = None
        self.hover_size = None

        self.pack_options = {}
        self.pack_propagate(False)
        #self.configure(bg_color=self.master.cget("fg_color"))
        self.order = 0
        self.num = None
        self.name = None

        #self.bind("<B1-Motion>", self.on_drag_motion)
        self.props = {}
        self.hover_options = {}

        print(self._inner_id)
        self.bind_mouse(properties)




    def __repr__(self):

        return f"{self.type}_{str(self.order)}"

    def get_class(self):
        return "CTkAdvancedButton"

    def get_name(self):
        return self.name.replace(" ", "_")

    def save(self, func, key, val, arg):
        self.props[key] = val
        func(arg)

    def save_hover(self, func, key, val, arg):
        self.hover_options[key] = val
        func(arg)

    def configure(self, require_redraw=False, **kwargs):

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
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Text", "TEXT", "text", {"val": self.cget("text"), "callback": lambda val: self.save(lambda val: self.configure(text=val), "text", val, val)})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Image", "IMAGE", "image", {"image": self.image, "key": "image", "callback": self.set_image})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Corner Radius", "SPINBOX", "Corner Radius", {"to": 100, "from": 0, "val": self.cget("corner_radius"), "callback": lambda val: self.save(lambda val: self.configure(corner_radius=val), "corner_radius", int(val), int(val))})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Border Width", "SPINBOX", "Border Width", {"to": 100, "from": 0, "val": self.cget("border_width"), "callback": lambda val: self.save(lambda val: self.configure(border_width=val), "border_width", int(val), int(val))})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Border Spacing", "SPINBOX", "border_spacing", {"to": 100, "from": 0, "val": self.cget("border_spacing"), "callback": lambda val: self.save(lambda val: self.configure(border_spacing=val), "border_spacing", int(val), int(val))})
        self.properties.add_seperator(self.properties.GEOMETRY_CONTENT, "Hover Changes")
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Hover Text", "TEXT", "hover_text", {"val": self.cget("hover_text"), "callback": lambda val: self.save(lambda val: self.configure(hover_text=val), "hover_text", val, val)})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Hover Image", "IMAGE", "hover_image", {"image": self.hover_image, "key": "image", "callback": self.hover_set_image})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Hover Corner Radius", "SPINBOX", "hover_corner_radius", {"to": 100, "from": 0, "val": self.cget("hover_corner_radius"), "callback": lambda val: self.save(lambda val: self.configure(hover_corner_radius=val), "hover_corner_radius", int(val), int(val))})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Hover Border Width", "SPINBOX", "hover_border_width", {"to": 100, "from": 0, "val": self.cget("hover_border_width"), "callback": lambda val: self.save(lambda val: self.configure(hover_border_width=val), "hover_border_width", int(val), int(val))})
        self.properties.add_option(self.properties.GEOMETRY_CONTENT, "Hover Border Spacing", "SPINBOX", "hover_border_spacing", {"to": 100, "from": 0, "val": self.cget("hover_border_spacing"), "callback": lambda val: self.save(lambda val: self.configure(hover_border_spacing=val), "hover_border_spacing", int(val), int(val))})
        # Had to reset the image for compound option to take effect
        self.properties.add_option(self.properties.ARRANGEMENT, "Compound", "COMBO", "compound", {"vals": ["top", "bottom", "left", "right"], "default": self.cget("compound"), "callback": lambda val: self.save(lambda val: (self.configure(compound=val, image=None), self.set_compound(self.image)), "compound", val, val)})
        self.properties.add_option(self.properties.ARRANGEMENT, "Anchor", "COMBO", "anchor", {"vals": ["n", "ne", "e", "se", "s", "sw", "w", "nw", "center"], "default": self.cget("anchor"), "callback": lambda val: self.save(lambda val: self.configure(anchor=val, image=None), "anchor", val, val)})


        self.properties.add_option(self.properties.STYLES, "Font Family", "FONT_FAMILY", "font_family", {"key": "font_family", "default": self.cget("font").cget("family"), "callback": lambda val: self.save(lambda val: self.cget("font").configure(family=val), "font_family", val, val)})
        self.properties.add_option(self.properties.STYLES, "Font Size", "SPINBOX", "font_size", {"to": 500, "from": -500, "val": self.cget("font").cget("size"), "callback": lambda val: self.save(lambda val: self.cget("font").configure(size=int(val)), "font_size", int(val), int(val))})
        self.properties.add_option(self.properties.STYLES, "Font Weight", "COMBO", "font_weight", {"vals": ["bold", "normal"], "default": self.cget("font").cget("weight"), "callback": lambda val: self.save(lambda val: self.cget("font").configure(weight=val), "font_weight", val, val)})
        self.properties.add_option(self.properties.STYLES, "Font Slant", "COMBO", "font_slant", {"vals": ["italic", "roman"], "default": self.cget("font").cget("slant"), "callback": lambda val: self.save(lambda val: self.cget("font").configure(slant=val), "font_slant", val, val)})
        self.properties.add_option(self.properties.STYLES, "Font Underline", "COMBO", "font_underline", {"vals": ["True", "False"], "default": str(bool(self.cget("font").cget("underline"))), "callback": lambda val: self.save(lambda val: self.cget("font").configure(underline=val), "font_underline", self._bool_change(val), self._bool_change(val))})
        self.properties.add_option(self.properties.STYLES, "Font Overstrike", "COMBO", "font_overstrike", {"vals": ["True", "False"], "default": str(bool(self.cget("font").cget("overstrike"))), "callback": lambda val: self.save(lambda val: self.cget("font").configure(overstrike=val), "font_overstrike", self._bool_change(val), self._bool_change(val))})
        self.properties.add_seperator(self.properties.STYLES, "Hover Changes")
        self.properties.add_option(self.properties.STYLES, "Hover Font Family", "FONT_FAMILY", "hover_font_family", {"key": "hover_font_family", "default": self.cget("hover_font").cget("family"), "callback": lambda val: self.save(lambda val: self.cget("hover_font").configure(family=val), "hover_font_family", val, val)})
        self.properties.add_option(self.properties.STYLES, "Hover Font Size", "SPINBOX", "hover_font_size", {"to": 500, "from": -500, "val": self.cget("hover_font").cget("size"), "callback": lambda val: self.save(lambda val: self.cget("hover_font").configure(size=int(val)), "hover_font_size", int(val), int(val))})
        self.properties.add_option(self.properties.STYLES, "Hover Font Weight", "COMBO", "hover_font_weight", {"vals": ["bold", "normal"], "default": self.cget("hover_font").cget("weight"), "callback": lambda val: self.save(lambda val: self.cget("hover_font").configure(weight=val), "hover_font_weight", val, val)})
        self.properties.add_option(self.properties.STYLES, "Hover Font Slant", "COMBO", "hover_font_slant", {"vals": ["italic", "roman"], "default": self.cget("hover_font").cget("slant"), "callback": lambda val: self.save(lambda val: self.cget("hover_font").configure(slant=val), "hover_font_slant", val, val)})
        self.properties.add_option(self.properties.STYLES, "Hover Font Underline", "COMBO", "hover_font_underline", {"vals": ["True", "False"], "default": str(bool(self.cget("hover_font").cget("underline"))), "callback": lambda val: self.save(lambda val: self.cget("hover_font").configure(underline=val), "hover_font_underline", self._bool_change(val), self._bool_change(val))})
        self.properties.add_option(self.properties.STYLES, "Hover Font Overstrike", "COMBO", "hover_font_overstrike", {"vals": ["True", "False"], "default": str(bool(self.cget("hover_font").cget("overstrike"))), "callback": lambda val: self.save(lambda val: self.cget("hover_font").configure(overstrike=val), "hover_font_overstrike", self._bool_change(val), self._bool_change(val))})
        self.properties.add_seperator(self.properties.STYLES, "Normal Changes")

        self.properties.add_option(self.properties.STYLES, "Hover", "COMBO", "hover", {"vals": ["True", "False"], "default": str(bool(self.cget("hover"))), "callback": lambda val: self.save(lambda val: self.configure(hover=val), "hover", self._bool_change(val), self._bool_change(val))})
        self.properties.add_option(self.properties.STYLES, "State", "COMBO", "state", {"vals": ["normal", "disabled"], "default": self.cget("state"), "callback": lambda val: self.save(lambda val: self.configure(state=val), "state", val, val)})

        self.properties.add_option(self.properties.STYLES, "FG Color", "COLOR_COMBO", "fg_color", {"color": self.cget("fg_color"), "key": "fg_color", "transparent": True, "callback": lambda val: self.save(lambda val: self.configure(fg_color=val), "fg_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "BG Color", "COLOR_COMBO", "bg_color", {"color": self.cget("bg_color"), "key": "bg_color", "transparent": True, "callback": lambda val: self.save(lambda val: self.configure(bg_color=val), "bg_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Border Color", "COLOR_COMBO", "border_color", {"color": self.cget("border_color"), "key": "border_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(border_color=val), "border_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Text Color", "COLOR_COMBO", "text_color", {"color": self.cget("text_color"), "key": "text_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(text_color=val), "text_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Text Disabled Color", "COLOR_COMBO", "text_color_disabled", {"color": self.cget("text_color_disabled"), "key": "text_color_disabled", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(text_color_disabled=val), "text_color_disabled", val, val)})
        self.properties.add_seperator(self.properties.STYLES, "Hover Changes")
        self.properties.add_option(self.properties.STYLES, "Hover Border Color", "COLOR_COMBO", "hover_border_color", {"color": self.cget("hover_border_color"), "key": "hover_border_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(hover_border_color=val), "hover_border_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Hover Color", "COLOR_COMBO", "hover_color", {"color": self.cget("hover_color"), "key": "hover_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(hover_color=val), "hover_color", val, val)})
        self.properties.add_option(self.properties.STYLES, "Hover Text Color", "COLOR_COMBO", "hover_text_color", {"color": self.cget("hover_text_color"), "key": "hover_text_color", "transparent": False, "callback": lambda val: self.save(lambda val: self.configure(hover_text_color=val), "hover_text_color", val, val)})



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


    def hover_set_image(self, hover_img, hover_size):
        if hover_img is not None:
            self.hover_image = hover_img
            hover_img = Image.open(hover_img)
            hover_img = CTkImage(light_image=hover_img, dark_image=hover_img, size=hover_size)

            # Image is not updating. Changing the width is the workaround I found. Need to change this if possible
            self.configure(hover_image=hover_img, width=int(self.cget("width"))+1)
            self.configure(width=int(self.cget("width"))-1)
            self.hover_img = hover_img
            self.hover_size = hover_size
            self.props["hover_image"] = hover_img

        else:
            self.hover_image = None
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
            self.configure(hover_image=None, width=with_img_width, height=with_img_height)
            self.update()
            self.configure(width=real_width, height=real_height)
            self.hover_size = None

            #self.properties.main.redraw(self.properties.main.widgets[self.properties.main.r])

            #self.properties.main.r.update()



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


