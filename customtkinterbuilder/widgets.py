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

    def save_properties(self, properties):
        print(properties)
        for key, value in properties.items():
            if key.startswith("font_"):
                prop = {key.replace("font_", ""): value}
                self.save(lambda val: self.cget("font").configure(**prop), key, value, value)
            else:
                self.save(lambda val: self.configure(**{key: value}), key, value, value)

    def bind_mouse(self, properties):
        self.bind("<MouseWheel>", properties.main.on_vert_mouse)
        self.bind("<Shift-MouseWheel>", properties.main.on_horiz_mouse)
