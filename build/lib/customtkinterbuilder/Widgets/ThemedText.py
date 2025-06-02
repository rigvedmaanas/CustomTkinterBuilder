from customtkinterbuilder.Widgets.Label import Label


class Heading_1(Label):
    def __init__(self, *args, properties, **kwargs):
        super().__init__(*args, properties=properties, **kwargs)
    def pack(self, **kwargs):
        super().pack(**kwargs)
        self.save(lambda val: self.configure(text=val), "text", "Heading 1", "Heading 1")
        self.save(lambda val: self.cget("font").configure(size=val), "font_size", int(45), int(45))
        self.save(lambda val: self.cget("font").configure(weight=val), "font_weight", "bold", "bold")


class Heading_2(Label):
    def __init__(self, *args, properties, **kwargs):
        super().__init__(*args, properties=properties, **kwargs)
    def pack(self, **kwargs):
        super().pack(**kwargs)
        self.save(lambda val: self.configure(text=val), "text", "Heading 2", "Heading 2")
        self.save(lambda val: self.cget("font").configure(size=val), "font_size", int(45), int(45))
        self.save(lambda val: self.cget("font").configure(weight=val), "font_weight", "normal", "normal")


class SubHeading(Label):
    def __init__(self, *args, properties, **kwargs):
        super().__init__(*args, properties=properties, **kwargs)
    def pack(self, **kwargs):
        super().pack(**kwargs)
        self.save(lambda val: self.configure(text=val), "text", "Sub Heading", "Sub Heading")
        self.save(lambda val: self.cget("font").configure(size=val), "font_size", int(30), int(30))
        self.save(lambda val: self.cget("font").configure(weight=val), "font_weight", "normal", "normal")

class Paragraph_1(Label):
    def __init__(self, *args, properties, **kwargs):
        super().__init__(*args, properties=properties, **kwargs)
    def pack(self, **kwargs):
        super().pack(**kwargs)
        self.save(lambda val: self.configure(text=val), "text", "I am Paragraph 1", "I am Paragraph 1")
        self.save(lambda val: self.cget("font").configure(size=val), "font_size", int(15), int(15))
        self.save(lambda val: self.cget("font").configure(weight=val), "font_weight", "normal", "normal")

class WrappedParagraph(Label):
    def __init__(self, *args, properties, **kwargs):
        super().__init__(*args, properties=properties, **kwargs)
        #self.save(lambda val: self.bind('<Configure>', lambda e: self.configure(wraplength=val)), "wraplength", self.winfo_width(), self.winfo_width())

        self.save(lambda val: self.configure(wraplength=val), "wraplength", int(200), int(200))
    def pack(self, **kwargs):
        super().pack(**kwargs)
        self.save(lambda val: self.configure(text=val), "text", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
        self.save(lambda val: self.cget("font").configure(size=val), "font_size", int(15), int(15))
        self.save(lambda val: self.cget("font").configure(weight=val), "font_weight", "normal", "normal")
