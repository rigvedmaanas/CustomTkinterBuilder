from tkinter.colorchooser import askcolor
from customtkinter import *
from typing import Union, Callable

class Spinbox(CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: Union[int] = 1,
                 command: Callable = None,
                 positive=False,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command
        self.long_press = False
        self.timeperiod = 0
        self.positive = positive
        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = CTkButton(self, text="-", width=height-6, height=height-6,
                                                       command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)
        self.subtract_button.bind("<Button-1>", lambda e: self.set_long_press(True, "SUB"))
        self.subtract_button.bind("<ButtonRelease>", lambda e: self.set_long_press(False, "SUB"))

        self.entry = CTkEntry(self, width=width-(2*height), height=height-6, border_width=0, justify="center")
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = CTkButton(self, text="+", width=height-6, height=height-6,
                                                  command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)
        self.add_button.bind("<Button-1>", lambda e: self.set_long_press(True, "ADD"))
        self.add_button.bind("<ButtonRelease>", lambda e: self.set_long_press(False, "ADD"))
        # default value
        self.entry.insert(0, "0")

    def do_checks(self, add_or_sub):
        if self.long_press:
            if add_or_sub == "ADD":
                self.add_button_callback()
            elif add_or_sub == "SUB":
                self.subtract_button_callback()
            self.winfo_toplevel().after(30, lambda: self.do_checks(add_or_sub))


    def set_long_press(self, state, add_or_sub):
        self.long_press = state

        if self.long_press:

            self.winfo_toplevel().after(750, lambda: self.do_checks(add_or_sub))


    def add_button_callback(self):

        try:
            value = int(float(self.entry.get())) + self.step_size
            if value < 0 and self.positive:
                value = int(float(self.entry.get()))
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError as e:
            print(e)
            return
        if self.command is not None:
            self.command(self.get())

    def subtract_button_callback(self):

        try:
            value = int(self.entry.get()) - self.step_size
            if value < 0 and self.positive:
                value = int(float(self.entry.get()))
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return
        if self.command is not None:
            self.command(self.get())

    def get(self) -> Union[int, None]:
        try:
            return self.entry.get()
        except ValueError:
            return None

    def set(self, value: int):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(int(value)))




class PropertiesManager(CTkScrollableFrame):
    def __init__(self, *args, main, **kwargs):
        super().__init__(*args, **kwargs)
        self.options = {}
        self.main = main

    def add_seperator(self, head):
        frame = CTkFrame(self, height=75, fg_color="transparent")
        frame.pack(padx=10, pady=(10, 0), fill="x")

        txt = CTkLabel(frame, text=head)
        txt.pack(fill="x")


    def add_option(self, header, TYPE, key, vals):
        if TYPE == "SLIDER":
            frame = CTkFrame(self, height=75)
            frame.pack(padx=10, pady=(10, 0), fill="x")

            num_spinbox = Spinbox(frame, width=150, command=lambda val: (vals["callback"](val), slider.set(int(float(num_spinbox.get())))))
            num_spinbox.pack(side="right", padx=(10, 10), pady=10)
            slider = CTkSlider(frame, to=vals["to"], from_=vals["from"], command=lambda val: (vals["callback"](val), num_spinbox.set(int(val))), width=150)
            #slider.pack(padx=10, pady=10, fill="x")
            slider.set(vals["val"])
            head = CTkLabel(frame, text=header)
            head.pack(side="right", padx=(10, 0), pady=10)

            self.options[key] = [head, slider, num_spinbox]

        if TYPE == "TEXT":
            frame = CTkFrame(self, height=75)
            frame.pack(padx=10, pady=(10, 0), fill="x")


            sv = StringVar()
            sv.trace("w", lambda name, index, mode, sv=sv: vals["callback"](sv.get()))

            entry = CTkEntry(frame, width=150, textvariable=sv)
            entry.pack(side="right", padx=10, pady=10)
            head = CTkLabel(frame, text=header)
            head.pack(side="right", padx=(10, 0), pady=10)

            print(vals)
            #entry.bind("<Key>", lambda e: self._manage_text(e, entry, vals["callback"]))
            sv.set(vals["val"])
            self.options[key] = [head, entry]

        if TYPE == "TUPLE":
            frame = CTkFrame(self, height=75)
            frame.pack(padx=10, pady=(10, 0), fill="x")

            temp = CTkFrame(frame, height=75, fg_color="transparent")
            temp.pack(side="right", fill="x")

            num_spinbox_1 = Spinbox(temp, width=150, positive=True, command=lambda val: (
            vals["callback"](int(val), num_spinbox_2.get())))
            num_spinbox_1.pack(padx=(10, 10), pady=10)
            num_spinbox_1.set(vals["val1"])

            num_spinbox_2 = Spinbox(temp, width=150, positive=True, command=lambda val: (
            vals["callback"](num_spinbox_1.get(), int(val))))
            num_spinbox_2.pack(padx=(10, 10), pady=10)

            num_spinbox_2.set(vals["val2"])

            head = CTkLabel(frame, text=header)
            head.pack(side="right", padx=(10, 0), pady=10)

            self.options[key] = [head, num_spinbox_1, num_spinbox_2]

        if TYPE == "COMBO":
            frame = CTkFrame(self, height=75)
            frame.pack(padx=10, pady=(10, 0), fill="x")



            combo = CTkOptionMenu(frame, width=150, values=vals["vals"], command=vals["callback"])
            combo.set(vals["default"])
            combo.pack(side="right", padx=10, pady=10)
            head = CTkLabel(frame, text=header)
            head.pack(side="right", padx=(10, 0), pady=10)
            self.options[key] = [head, combo]

        if TYPE == "COLOR_COMBO":
            frame = CTkFrame(self, height=75)
            frame.pack(padx=10, pady=(10, 0), fill="x")

            temp = CTkFrame(frame, height=75, fg_color="transparent")
            temp.pack(side="right", fill="x")

            clr_1 = CTkButton(temp, width=150//2-2, hover=False, text="", border_width=2)
            clr_1.pack(padx=(0, 2), pady=10, side="left", fill="x")
            clr_1.configure(command=lambda: self._color_chooser_btn1(clr_1, clr_2, vals["callback"]))

            clr_2 = CTkButton(temp, width=150//2-1, hover=False, text="", border_width=2)
            clr_2.pack(padx=(2, 10), pady=10, side="left", fill="x")
            clr_2.configure(command=lambda: self._color_chooser_btn2(clr_1, clr_2, vals["callback"]))


            if vals["transparent"]:
                head = CTkCheckBox(frame, text=header)
                head.pack(side="right", padx=(10, 0), pady=10)
                head.configure(command=lambda: (
                    (clr_1.configure(state="normal"), clr_2.configure(state="normal"), vals["callback"]((clr_1.cget("fg_color"))), clr_2.configure(fg_color=clr_1.cget("fg_color")))
                    if head.get() == 1
                    else (clr_1.configure(state="disabled"), clr_2.configure(state="disabled"), vals["callback"]("transparent"))
                ))
            else:
                head = CTkLabel(frame, text=header)
                head.pack(side="right", padx=(10, 10), pady=10)

            if vals["color"] != "transparent":
                clr_1.configure(fg_color=vals["color"][0])
                clr_2.configure(fg_color=vals["color"][1])
                if type(head) == CTkCheckBox:
                    head.select()
            else:
                if type(head) == CTkCheckBox:
                    head.deselect()

                clr_1.configure(state="disabled")
                clr_2.configure(state="disabled")


            self.options[key] = [head, clr_1, clr_1]

    def _color_chooser_btn1(self, btn, btn2, callback):
        clr = askcolor()[1]

        if clr is not None:
            btn.configure(fg_color=clr)

            callback((clr, btn2.cget("fg_color")))

    def _color_chooser_btn2(self, btn, btn2, callback):
        clr = askcolor()[1]

        if clr is not None:
            btn2.configure(fg_color=clr)

            callback((btn.cget("fg_color"), clr))


    def _manage(self, e, slider, num_entry, callback):
        try:
            if e.char.isdigit():
                slider.set(int(float(num_entry.get()+e.char)))
                callback(slider.get())
            else:
                slider.set(int(float(num_entry.get())))
                callback(slider.get())
        except Exception as e:
            pass
    def _manage_text(self, e, entry, callback):
        try:
            if e.char in list("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/?"):
                callback(entry.get()+e.char)
            else:
                callback(entry.get())
        except Exception as e:
            pass

    def update_options(self, key, type, vals):
        if type == "SLIDER":
            option = self.options[key]
            option[1].set(vals["val"])
            option[2].set(vals["val"])




    def destroy_children(self):
        for widget in self.winfo_children():
            widget.destroy()