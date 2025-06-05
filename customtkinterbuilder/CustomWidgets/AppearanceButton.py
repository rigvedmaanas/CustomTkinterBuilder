from customtkinter import *

class AppearanceButton(CTkSegmentedButton):
    def __init__(self, master):
        super().__init__(master, values=["Light Mode", "Dark Mode"], command=self.change)
        self.value = 0
        self.call_command = None
        self.set("Light Mode")

    def change(self, value):
        if value == "Dark Mode":
            self.value = 1
        else:
            self.value = 0
        if self.call_command is not None:
            self.call_command()
    def configure(self, **kwargs):
        command = kwargs.pop("command")
        if command:
            self.call_command = command

    def toggle(self):
        if self.value == 0:
            self.value = 1
            self.set("Dark Mode")

        else:
            self.value = 0
            self.set("Light Mode")


    def get(self):
        return self.value
