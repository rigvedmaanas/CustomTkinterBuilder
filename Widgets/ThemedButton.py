import os.path
import shutil
from get_path import resource_path, tempify
from theme_colors import get_ui_color
from Widgets.Button import Button


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
        self.save(lambda val: self.configure(fg_color=val), "fg_color", get_ui_color("themed_button_1_fg"), get_ui_color("themed_button_1_fg"))
        self.save(lambda val: self.configure(hover_color=val), "hover_color", get_ui_color("themed_button_1_hover"), get_ui_color("themed_button_1_hover"))
        self.save(lambda val: self.configure(border_color=val), "border_color", get_ui_color("themed_button_1_border"), get_ui_color("themed_button_1_border"))
        self.save(lambda val: self.configure(border_width=val), "border_width", 1, 1)


class Button_2(Button):
    def __init__(self, *args, properties, **kwargs):
        super().__init__(*args, properties=properties, **kwargs)

    def pack(self, **kwargs):
        super().pack(**kwargs)
        shutil.copy2(resource_path(os.path.join("ThemeAssets", "ThemedButton", "Button_2", "baseline_arrow_forward_white_18dp_1x.png")), tempify("temp"))

        #self.set_image(os.path.join("ThemeAssets", "ThemedButton", "Button_2", "baseline_arrow_forward_white_18dp_1x.png"), size=(18, 18))
        self.set_image(tempify(os.path.join("temp", "baseline_arrow_forward_white_18dp_1x.png")), size=(18, 18))

        self.save(lambda val: self.configure(width=val), "width", 140, 140)
        self.save(lambda val: self.configure(height=val), "height", 38, 38)
        self.save(lambda val: self.configure(compound=val), "compound", "right", "right")

        self.save(lambda val: self.configure(text=val), "text", "Next", "Next")
        self.save(lambda val: self.configure(corner_radius=val), "corner_radius", 30, 30)
        self.save(lambda val: self.configure(fg_color=val), "fg_color", get_ui_color("themed_button_2_fg"), get_ui_color("themed_button_2_fg"))
        self.save(lambda val: self.configure(text_color=val), "text_color", get_ui_color("themed_button_2_text"), get_ui_color("themed_button_2_text"))
        self.save(lambda val: self.configure(hover_color=val), "hover_color", get_ui_color("themed_button_2_hover"), get_ui_color("themed_button_2_hover"))
        self.save(lambda val: self.configure(border_color=val), "border_color", get_ui_color("themed_button_2_border"), get_ui_color("themed_button_2_border"))
        self.save(lambda val: self.configure(border_width=val), "border_width", 0, 0)
        self.save(lambda val: self.configure(text_color_disabled=val), "text_color_disabled", ["gray78", "gray68"], ["gray78", "gray68"])


        self.save(lambda val: self.cget("font").configure(size=val), "font_size", int(15), int(15))
        self.save(lambda val: self.cget("font").configure(weight=val), "font_weight", "normal", "normal")

class Button_3(Button):
    def __init__(self, *args, properties, **kwargs):
        super().__init__(*args, properties=properties, **kwargs)

    def pack(self, **kwargs):
        super().pack(**kwargs)

        self.save(lambda val: self.configure(width=val), "width", 140, 140)
        self.save(lambda val: self.configure(height=val), "height", 38, 38)

        self.save(lambda val: self.configure(text=val), "text", "Purchase", "Purchase")
        self.save(lambda val: self.configure(corner_radius=val), "corner_radius", 3, 3)
        self.save(lambda val: self.configure(fg_color=val), "fg_color", get_ui_color("themed_button_3_fg"), get_ui_color("themed_button_3_fg"))
        self.save(lambda val: self.configure(text_color=val), "text_color", get_ui_color("themed_button_3_text"), get_ui_color("themed_button_3_text"))
        self.save(lambda val: self.configure(hover_color=val), "hover_color", get_ui_color("themed_button_3_hover"), get_ui_color("themed_button_3_hover"))
        self.save(lambda val: self.configure(border_color=val), "border_color", get_ui_color("themed_button_3_border"), get_ui_color("themed_button_3_border"))
        self.save(lambda val: self.configure(border_width=val), "border_width", 1, 1)
        self.save(lambda val: self.configure(text_color_disabled=val), "text_color_disabled", ["gray78", "gray68"], ["gray78", "gray68"])

        self.save(lambda val: self.cget("font").configure(size=val), "font_size", int(15), int(15))
        self.save(lambda val: self.cget("font").configure(weight=val), "font_weight", "bold", "bold")

class Button_Icon_white(Button):
    def __init__(self, *args, properties, **kwargs):
        super().__init__(*args, properties=properties, **kwargs)

    def pack(self, **kwargs):
        super().pack(**kwargs)
        self.save(lambda val: self.configure(width=val), "width", 40, 40)
        self.save(lambda val: self.configure(height=val), "height", 40, 40)
        self.save(lambda val: self.configure(text=val), "text", "", "")
        self.save(lambda val: self.configure(corner_radius=val), "corner_radius", 3, 3)
        self.save(lambda val: self.configure(fg_color=val), "fg_color", get_ui_color("themed_icon_white_fg"), get_ui_color("themed_icon_white_fg"))
        self.save(lambda val: self.configure(text_color=val), "text_color", get_ui_color("themed_icon_white_text"), get_ui_color("themed_icon_white_text"))
        self.save(lambda val: self.configure(hover_color=val), "hover_color", get_ui_color("themed_icon_white_hover"), get_ui_color("themed_icon_white_hover"))
        self.save(lambda val: self.configure(border_color=val), "border_color", get_ui_color("themed_icon_white_border"), get_ui_color("themed_icon_white_border"))
        self.save(lambda val: self.configure(border_width=val), "border_width", 0, 0)
        self.save(lambda val: self.configure(text_color_disabled=val), "text_color_disabled", ["gray78", "gray68"], ["gray78", "gray68"])
        shutil.copy2(resource_path(os.path.join("ThemeAssets", "ThemedButton", "Icon_White", "baseline_people_white_18dp_1x.png")), tempify("temp"))
        #self.set_image(resource_path(os.path.join("ThemeAssets", "ThemedButton", "Icon_White", "baseline_people_white_18dp_1x.png")), size=(18, 18))
        self.set_image(tempify(os.path.join("temp", "baseline_people_white_18dp_1x.png")), size=(18, 18))


class Button_Icon_black(Button):
    def __init__(self, *args, properties, **kwargs):
        super().__init__(*args, properties=properties, **kwargs)

    def pack(self, **kwargs):
        super().pack(**kwargs)
        self.save(lambda val: self.configure(width=val), "width", 40, 40)
        self.save(lambda val: self.configure(height=val), "height", 40, 40)
        self.save(lambda val: self.configure(text=val), "text", "", "")
        self.save(lambda val: self.configure(corner_radius=val), "corner_radius", 3, 3)
        self.save(lambda val: self.configure(fg_color=val), "fg_color", get_ui_color("themed_icon_black_fg"), get_ui_color("themed_icon_black_fg"))
        self.save(lambda val: self.configure(text_color=val), "text_color", get_ui_color("themed_icon_black_text"), get_ui_color("themed_icon_black_text"))
        self.save(lambda val: self.configure(hover_color=val), "hover_color", get_ui_color("themed_icon_black_hover"), get_ui_color("themed_icon_black_hover"))
        self.save(lambda val: self.configure(border_color=val), "border_color", get_ui_color("themed_icon_black_border"), get_ui_color("themed_icon_black_border"))
        self.save(lambda val: self.configure(border_width=val), "border_width", 0, 0)
        self.save(lambda val: self.configure(text_color_disabled=val), "text_color_disabled", ["gray78", "gray68"], ["gray78", "gray68"])
        shutil.copy2(resource_path(os.path.join("ThemeAssets", "ThemedButton", "Icon_Black", "baseline_people_black_18dp_1x.png")), tempify("temp"))
        #self.set_image(resource_path(os.path.join("ThemeAssets", "ThemedButton", "Icon_Black", "baseline_people_black_18dp_1x.png")), size=(18, 18))
        self.set_image(tempify(os.path.join("temp", "baseline_people_black_18dp_1x.png")), size=(18, 18))

