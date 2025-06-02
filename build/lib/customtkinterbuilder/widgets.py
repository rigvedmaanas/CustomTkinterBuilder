import uuid

# Need to put all those default stuff of all widgets here
class BaseWidgetClass:
    def __init__(self, **kwargs):
        self._inner_id = str(uuid.uuid4())
        #self.configure(bg_color="transparent")
        if "master" in kwargs:
            self.parent = kwargs["master"]
        else:
            self.parent = self.master

    def bind_mouse(self, properties):
        self.bind("<MouseWheel>", properties.main.on_vert_mouse)
        self.bind("<Shift-MouseWheel>", properties.main.on_horiz_mouse)
