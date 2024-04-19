import uuid

# Need to put all those default stuff of all widgets here
class BaseWidgetClass:
    def __init__(self):
        self._inner_id = str(uuid.uuid4())