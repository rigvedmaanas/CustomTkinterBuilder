import os.path
import shutil
from customtkinterbuilder.get_path import resource_path, tempify
from customtkinterbuilder.Widgets.Button import Button
from customtkinterbuilder.Widgets.Frame import Frame
from customtkinterbuilder.Widgets.ScrollableFrame import ScrollableFrame

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


class Button_2(Frame):
    def __init__(self, *args, properties, **kwargs):
        super().__init__(*args, properties=properties, **kwargs)
        self.component = True


    def add_widgets(self, func, properties, widget):

        # func(Button_1, x=0, y=0, properties=properties, widget=widget, part_of_component=True)
        properties["orientation"] = "vertical"
        scrl = func(ScrollableFrame, x=0, y=0, properties=properties, widget=widget, part_of_component=True, return_widget=True)
        properties.pop("orientation")

        for a in range(10):
            func(Button_1, x=0, y=0, properties=properties, widget=scrl.get_me(), part_of_component=True,
                 return_widget=True)


class Button_3(Button):
    def __init__(self, *args, properties, **kwargs):
        super().__init__(*args, properties=properties, **kwargs)

    def pack(self, **kwargs):
        super().pack(**kwargs)

        self.save(lambda val: self.configure(width=val), "width", 140, 140)
        self.save(lambda val: self.configure(height=val), "height", 38, 38)

        self.save(lambda val: self.configure(text=val), "text", "Purchase", "Purchase")
        self.save(lambda val: self.configure(corner_radius=val), "corner_radius", 3, 3)
        self.save(lambda val: self.configure(fg_color=val), "fg_color", ["#993500", "#282525"], ["#993500", "#282525"])
        self.save(lambda val: self.configure(text_color=val), "text_color", ["gray98", "#ffffff"], ["gray98", "#ffffff"])
        self.save(lambda val: self.configure(hover_color=val), "hover_color", ["#2d2929", "#993500"], ["#2d2929", "#993500"])
        self.save(lambda val: self.configure(border_color=val), "border_color", ["#5f5f5f", "#ffffff"], ["#5f5f5f", "#ffffff"])
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
        self.save(lambda val: self.configure(fg_color=val), "fg_color", ["#3965FF", "#3965FF"], ["#3965FF", "#3965FF"])
        self.save(lambda val: self.configure(text_color=val), "text_color", ["#ffffff", "#ffffff"], ["#ffffff", "#ffffff"])
        self.save(lambda val: self.configure(hover_color=val), "hover_color", ["#2B4DC6", "#2B4DC6"], ["#2B4DC6", "#2B4DC6"])
        self.save(lambda val: self.configure(border_color=val), "border_color", ["#3E454A", "#949A9F"], ["#3E454A", "#949A9F"])
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
        self.save(lambda val: self.configure(fg_color=val), "fg_color", ["#40B6FF", "#40B6FF"], ["#40B6FF", "#40B6FF"])
        self.save(lambda val: self.configure(text_color=val), "text_color", ["#ffffff", "#ffffff"], ["#ffffff", "#ffffff"])
        self.save(lambda val: self.configure(hover_color=val), "hover_color", ["#00D9FF", "#00D9FF"], ["#00D9FF", "#00D9FF"])
        self.save(lambda val: self.configure(border_color=val), "border_color", ["#3E454A", "#949A9F"], ["#3E454A", "#949A9F"])
        self.save(lambda val: self.configure(border_width=val), "border_width", 0, 0)
        self.save(lambda val: self.configure(text_color_disabled=val), "text_color_disabled", ["gray78", "gray68"], ["gray78", "gray68"])
        shutil.copy2(resource_path(os.path.join("ThemeAssets", "ThemedButton", "Icon_Black", "baseline_people_black_18dp_1x.png")), tempify("temp"))
        #self.set_image(resource_path(os.path.join("ThemeAssets", "ThemedButton", "Icon_Black", "baseline_people_black_18dp_1x.png")), size=(18, 18))
        self.set_image(tempify(os.path.join("temp", "baseline_people_black_18dp_1x.png")), size=(18, 18))


