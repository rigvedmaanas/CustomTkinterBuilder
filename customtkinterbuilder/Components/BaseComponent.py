import shutil

class BaseComponent:
    def __init__(self):
        self.component = True

    @classmethod
    def as_str(cls):
        return "Base Component"

    def copy(self, file):
        shutil.copy2(file, "./customtkinterbuilder/temp")

    def add_widgets(self, func, properties, widget):
        pass



    def get_combined_properties(self, properties1, properties2):
        new_properties = {}
        print(properties1)
        for key, value in properties2.items():
            new_properties[key] = value
        for key, value in properties1.items():  # Added second because these values will replace default
            new_properties[key] = value
        return new_properties