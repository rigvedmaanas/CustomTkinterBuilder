from .BaseComponent import BaseComponent
from customtkinterbuilder.Widgets import *

class LabelEntry(Frame, BaseComponent):
    def __init__(self, *args, properties, **kwargs):
        BaseComponent.__init__(self)
        Frame.__init__(self, *args, properties=properties, **kwargs)

    def __str__(self):
        return "Label Entry"

    def add_widgets(self, func, properties, widget):
        # func(WidgetClass, x=0, y=0, properties=properties, widget=widget, part_of_component=True, return_widget=True)

        self.properties = properties
        properties["orientation"] = "vertical"
        scrl = func(ScrollableFrame, x=0, y=0, properties=properties, widget=widget, part_of_component=True, return_widget=True)
        properties.pop("orientation")

        for a in range(10):
            func(Button_1, x=0, y=0, properties=properties, widget=scrl.get_me(), part_of_component=True,
                 return_widget=True)