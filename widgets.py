import uuid

# Need to put all those default stuff of all widgets here
class BaseWidgetClass:
    def __init__(self):
        self._inner_id = str(uuid.uuid4())

    def bind_mouse(self, properties):
        self.bind("<MouseWheel>", properties.main.on_vert_mouse)
        self.bind("<Shift-MouseWheel>", properties.main.on_horiz_mouse)
