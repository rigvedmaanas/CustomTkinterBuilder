import pathlib
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename
from tkinterdnd2 import TkinterDnD, DND_ALL
import math
from customtkinter import *
from typing import Union, Callable
from tkinter import font
from PIL import Image
import requests



class Toplevel(CTkToplevel, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

class ImageChooser(Toplevel):
    def __init__(self, *args, callback, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback = callback
        self.geometry("700x550+600+200")
        self.protocol("WM_DELETE_WINDOW", self.kill)
        #self.attributes('-topmost', True)
        self.title("Choose Image or Icon")
        self.image = ""

        self.tab = CTkTabview(self)
        self.tab.pack(fill="both", expand=True, padx=20, pady=20)

        self.tab.add("Icon")
        self.tab.add("Image")

        self.fr = CTkFrame(self.tab.tab("Icon"), fg_color="transparent")
        self.fr.pack(expand=True, fill="both", padx=20, pady=20)

        self.name_fr = CTkFrame(self.fr)
        self.name_fr.grid(row=0, column=0)

        self.instruct_lbl = CTkLabel(self.name_fr, text="Name", font=CTkFont(size=20), anchor="w")
        self.instruct_lbl.pack(padx=20, pady=(10, 0), fill="x")

        self.icon_name = CTkEntry(self.name_fr, width=250, placeholder_text="Name of the Icon")
        self.icon_name.pack(pady=10, side="left", padx=20)


        self.type_fr = CTkFrame(self.fr)
        self.type_fr.grid(row=1, column=0)

        self.instruct_lbl2 = CTkLabel(self.type_fr, text="Type", font=CTkFont(size=20), anchor="w")
        self.instruct_lbl2.pack(padx=20, pady=(10, 0), fill="x")

        self.icon_type = CTkOptionMenu(self.type_fr, width=250, values=["Filled", "Outlined", "Round", "Sharp", "Two Tone"])
        self.icon_type.pack(pady=10, side="left", padx=20)

        self.size_fr = CTkFrame(self.fr)
        self.size_fr.grid(row=0, column=1)

        self.instruct_lbl3 = CTkLabel(self.size_fr, text="Size", font=CTkFont(size=20), anchor="w")
        self.instruct_lbl3.pack(padx=20, pady=(10, 0), fill="x")

        self.icon_size = CTkOptionMenu(self.size_fr, width=250,
                                       values=["18dp", "24dp", "36dp", "48dp"])
        self.icon_size.pack(pady=10, side="left", padx=20)

        self.density_fr = CTkFrame(self.fr)
        self.density_fr.grid(row=1, column=1)

        self.instruct_lbl4 = CTkLabel(self.density_fr, text="Density", font=CTkFont(size=20), anchor="w")
        self.instruct_lbl4.pack(padx=20, pady=(10, 0), fill="x")

        self.icon_density = CTkOptionMenu(self.density_fr, width=250,
                                       values=["1x", "2x"])
        self.icon_density.pack(pady=10, side="left", padx=20)

        self.color_fr = CTkFrame(self.fr)
        self.color_fr.grid(row=2, column=0)

        self.instruct_lbl5 = CTkLabel(self.color_fr, text="Color", font=CTkFont(size=20), anchor="w")
        self.instruct_lbl5.pack(padx=20, pady=(10, 0), fill="x")

        self.icon_color = CTkOptionMenu(self.color_fr, width=250,
                                          values=["Black", "White"])
        self.icon_color.pack(pady=10, side="left", padx=20)

        self.img_lbl = CTkLabel(self.fr, text="")
        self.img_lbl.grid(row=2, column=1, pady=20, padx=20)


        self.temp_fr = CTkFrame(self.tab.tab("Icon"))
        self.temp_fr.pack(fill="x")

        self.download_btn = CTkButton(self.temp_fr, text="Download", height=40, command=lambda : self.get_icon(self.icon_name.get(), self.icon_type.get(), self.icon_size.get(), self.icon_density.get(), self.icon_color.get(), self.img_lbl))
        self.download_btn.pack(pady=20, padx=40, side="left")

        self.use_btn = CTkButton(self.temp_fr, text="Use", height=40, state="disabled", command=lambda : (self.callback(self.image), self.destroy()))
        self.use_btn.pack(pady=20, padx=40, side="right")

        self.frame = CTkFrame(self.tab.tab("Image"))
        self.frame.pack(padx=20, pady=20, expand=True, fill="both")

        self.text = CTkLabel(self.frame, text="Drag and Drop the Image or Choose the File", font=CTkFont(size=20))
        self.text.pack(pady=20)

        self.dnd_frame = CTkFrame(self.frame)
        self.dnd_frame.pack(padx=30, pady=(10, 30), expand=True, fill="both")

        self.dnd_frame.drop_target_register(DND_ALL)
        self.dnd_frame.dnd_bind("<<Drop>>", self.open_file)

        self.lbl = CTkButton(self.dnd_frame, text="Click to choose the file or Drag and Drop the File", font=CTkFont(size=13),
                        hover=False, fg_color="transparent", command=self.choose_file)
        self.lbl.pack(expand=True, fill="both")

    def kill(self):
        self.callback(self.image)
        self.destroy()

    def choose_file(self):
        file = askopenfilename(filetypes=[(".png", "png"), (".jpg", "jpg"), (".PNG", "PNG"), (".JPG", "JPG"), (".jpeg", "jpeg"), (".JPEG", "JPEG")])
        if file != "":
            self.image = file
            self.callback(self.image)
            print(self.image)
            self.destroy()
    def open_file(self, event):
        if event.data.endswith(".png") or event.data.endswith(".PNG") or event.data.endswith(".jpg") or event.data.endswith(".JPG") or event.data.endswith(".JPEG") or event.data.endswith(".jpeg"):
            print(event.data)
            self.image = event.data
            self.callback(self.image)
            self.destroy()



    def map_range(self, value, start1, stop1, start2, stop2):
        """
        Map a value from one range to another range.

        Parameters:
            value (float): The value to be mapped.
            start1 (float): Lower bound of the input range.
            stop1 (float): Upper bound of the input range.
            start2 (float): Lower bound of the output range.
            stop2 (float): Upper bound of the output range.

        Returns:
            float: The mapped value.
        """
        return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1))

    def change_color_to_white(self, img):



        width, height = img.size
        new_img = img.copy()


        # Loop through each pixel
        for x in range(width):
            for y in range(height):
                # Get the pixel value (R, G, B) tuple
                pixel = img.getpixel((x, y))

                # Access individual color channels (modify as needed)
                red = pixel[0]
                green = pixel[1]
                blue = pixel[2]
                alpha = pixel[3]
                red_new = math.floor(self.map_range(red, 0, 255, 255, 0))
                green_new = math.floor(self.map_range(green, 0, 255, 255, 0))
                blue_new = math.floor(self.map_range(blue, 0, 255, 255, 0))

                new_img.putpixel((x, y), (red_new, green_new, blue_new, alpha))
        # Save the grayscale image
        return new_img

    def get_icon(self, name, type_, size, density, color, display):


        if type_ == "Filled":
            type_ = "materialicons"
            n = "baseline"
        elif type_ == "Outlined":
            type_ = "materialiconsoutlined"
            n = "outline"
        elif type_ == "Round":
            type_ = "materialiconsround"
            n = "round"
        elif type_ == "Sharp":
            type_ = "materialiconssharp"
            n = "sharp"
        elif type_ == "Two Tone":
            type_ = "materialiconstwotone"
            n = "twotone"

        name = name.lower().replace(" ", "_")

        url = f"https://raw.githubusercontent.com/rigvedmaanas/material-design-icons/main/icons/{name}/{type_}/{size}/{density}/{n}_{name}_black_{size}.png"
        print(url)

        response = requests.get(url, stream=True)
        response.raw.decode_content = True

        if response.ok:
            image = Image.open(response.raw)
            if image.mode == "LA":
                image = image.convert("RGBA")
            if color == "White":
                image = self.change_color_to_white(image)

            self.image = image
            if color == "White":
                self.image.color_type = "white"
            else:
                self.image.color_type = "black"
            self.image.url = url
            self.image.save(f"temp/{n}_{name}_{self.image.color_type}_{size}_{density}.png")
            self.image = f"temp/{n}_{name}_{self.image.color_type}_{size}_{density}.png"
            display.configure(image=CTkImage(light_image=image, dark_image=image, size=(image.size[0], image.size[1])))

            self.use_btn.configure(state="normal")

        else:
            print("Invalid Name of Icon")



        


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

    def set_command(self, command):
        self.command = command

class TextExtension(CTkFrame):
    """Extends Frame.  Intended as a container for a Text field.  Better related data handling
    and has Y scrollbar."""


    def __init__(self, master, textvariable=None, *args, **kwargs):

        super(TextExtension, self).__init__(master)
        # Init GUI



        self._text_widget = CTkTextbox(self, *args, **kwargs)
        self._text_widget.pack(side=LEFT, fill=BOTH, expand=1)

        if textvariable is not None:
            if not (isinstance(textvariable, Variable)):
                raise TypeError("tkinter.Variable type expected, " + str(type(textvariable)) + " given.".format(type(textvariable)))
            self._text_variable = textvariable
            self.var_modified()
            self._text_trace = self._text_widget.bind('<<Modified>>', self.text_modified)
            self._var_trace = textvariable.trace("w", self.var_modified)

    def text_modified(self, *args):
            if self._text_variable is not None:
                self._text_variable.trace_vdelete("w", self._var_trace)
                self._text_variable.set(self._text_widget.get(1.0, 'end-1c'))
                self._var_trace = self._text_variable.trace("w", self.var_modified)
                self._text_widget.edit_modified(False)

    def var_modified(self, *args):
        self.set_text(self._text_variable.get())
        self._text_widget.edit_modified(False)

    def unhook(self):
        if self._text_variable is not None:
            self._text_variable.trace_vdelete("w", self._var_trace)


    def clear(self):
        self._text_widget.delete(1.0, END)

    def set_text(self, _value):
        self.clear()
        if (_value is not None):
            self._text_widget.insert(END, _value)

class PropertiesManager(CTkTabview):
    def __init__(self, *args, main, **kwargs):
        super().__init__(*args, **kwargs)
        self.options = {}
        self.main = main
        self.images = []  # To prevent garbage collection
        self.add("Geometry & Content")
        self.add("Styles")
        self.add("Arrangement")
        self.add("Layout")


        self.scr_geometry_content = CTkScrollableFrame(self.tab("Geometry & Content"), fg_color="transparent")
        self.scr_geometry_content.pack(fill="both", expand=True, pady=10)

        self.GEOMETRY_CONTENT = self.scr_geometry_content

        self.scr_style = CTkScrollableFrame(self.tab("Styles"), fg_color="transparent")
        self.scr_style.pack(fill="both", expand=True, pady=10)

        self.STYLES = self.scr_style

        self.scr_arrangement = CTkScrollableFrame(self.tab("Arrangement"), fg_color="transparent")
        self.scr_arrangement.pack(fill="both", expand=True, pady=10)

        self.ARRANGEMENT = self.scr_arrangement

        self.scr_layout = CTkScrollableFrame(self.tab("Layout"), fg_color="transparent")
        self.scr_layout.pack(fill="both", expand=True, pady=10)

        self.LAYOUT = self.scr_layout





    def add_seperator(self, head):
        frame = CTkFrame(self, height=75, fg_color="transparent")
        frame.pack(padx=10, pady=(10, 0), fill="x")

        txt = CTkLabel(frame, text=head)
        txt.pack(fill="x")


    def add_option(self, category, header, TYPE, key, vals):
        self.ctab = category

        if TYPE == "SPINBOX":
            frame = CTkFrame(self.ctab, height=75)
            frame.pack(padx=10, pady=(10, 0), fill="x")

            num_spinbox = Spinbox(frame, width=150, command=lambda val: vals["callback"](val))
            num_spinbox.pack(side="right", padx=(10, 10), pady=10)
            num_spinbox.set(vals["val"])


            head = CTkLabel(frame, text=header)
            head.pack(side="right", padx=(10, 0), pady=10)

            self.options[key] = [head, num_spinbox]

        elif TYPE == "TEXT":
            frame = CTkFrame(self.ctab, height=75)
            frame.pack(padx=10, pady=(10, 0), fill="x")


            sv = StringVar()
            sv.trace_add("write", lambda e1, e2, e3: vals["callback"](sv.get()))
            entry = TextExtension(frame, width=150, height=100, textvariable=sv)
            entry.pack(side="right", padx=10, pady=10)
            head = CTkLabel(frame, text=header)
            head.pack(side="right", padx=(10, 0), pady=10)

            sv.set(vals["val"])
            self.options[key] = [head, entry]

        elif TYPE == "SINGLELINE_TEXT":
            frame = CTkFrame(self.ctab, height=75)
            frame.pack(padx=10, pady=(10, 0), fill="x")


            sv = StringVar()
            sv.trace_add("write", lambda e1, e2, e3: vals["callback"](sv.get()))
            entry = CTkEntry(frame, width=150, textvariable=sv)
            entry.pack(side="right", padx=10, pady=10)
            head = CTkLabel(frame, text=header)
            head.pack(side="right", padx=(10, 0), pady=10)

            sv.set(vals["val"])
            self.options[key] = [head, entry]

        elif TYPE == "TUPLE":
            frame = CTkFrame(self.ctab, height=75)
            frame.pack(padx=10, pady=(10, 0), fill="x")

            temp = CTkFrame(frame, height=60, fg_color="transparent")
            temp.pack(side="right", fill="x", pady=10)

            num_spinbox_1 = Spinbox(temp, width=150, positive=True, command=lambda val: (
            vals["callback"](int(val), num_spinbox_2.get())))
            num_spinbox_1.pack(padx=(10, 10))
            num_spinbox_1.set(vals["val1"])

            num_spinbox_2 = Spinbox(temp, width=150, positive=True, command=lambda val: (
            vals["callback"](num_spinbox_1.get(), int(val))))
            num_spinbox_2.pack(padx=(10, 10), pady=(10, 0))

            num_spinbox_2.set(vals["val2"])

            head = CTkLabel(frame, text=header)
            head.pack(side="right", padx=(10, 0), pady=10)



            self.options[key] = [head, num_spinbox_1, num_spinbox_2]

        elif TYPE == "COMBO":
            frame = CTkFrame(self.ctab, height=75)
            frame.pack(padx=10, pady=(10, 0), fill="x")



            combo = CTkOptionMenu(frame, width=150, values=vals["vals"], command=vals["callback"])
            combo.set(vals["default"])
            combo.pack(side="right", padx=10, pady=10)
            head = CTkLabel(frame, text=header)
            head.pack(side="right", padx=(10, 0), pady=10)
            self.options[key] = [head, combo]

        elif TYPE == "COLOR_COMBO":
            frame = CTkFrame(self.ctab, height=75)
            frame.pack(padx=10, pady=(10, 0), fill="x")

            temp = CTkFrame(frame, height=60, fg_color="transparent")
            temp.pack(side="right", fill="x", pady=10)

            clr_1 = CTkButton(temp, width=150//2-2, hover=False, text="", border_width=2)
            clr_1.pack(padx=(0, 2), side="left", fill="x")
            clr_1.configure(command=lambda: self._color_chooser_btn1(clr_1, clr_2, vals["callback"]))

            clr_2 = CTkButton(temp, width=150//2-1, hover=False, text="", border_width=2)
            clr_2.pack(padx=(2, 10), side="left", fill="x")
            clr_2.configure(command=lambda: self._color_chooser_btn2(clr_1, clr_2, vals["callback"]))


            if vals["transparent"]:
                head = CTkCheckBox(frame, text=header)
                head.pack(side="right", padx=(10, 0), pady=10)
                head.configure(command=lambda: self.update_color_and_call_callback(head, clr_1, clr_2, vals))
            else:
                head = CTkLabel(frame, text=header)
                head.pack(side="right", padx=(10, 10), pady=10)

            if vals["color"] != "transparent":
                print(vals["color"])
                if type(vals["color"]) == str:
                    clr_1.configure(fg_color=vals["color"])
                    clr_2.configure(fg_color=vals["color"])
                else:
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

        elif TYPE == "FONT_FAMILY":
            frame = CTkFrame(self.ctab, height=75)
            frame.pack(padx=10, pady=(10, 0), fill="x")
            fonts = list(font.families())
            fonts.sort()
            combo = CTkOptionMenu(frame, width=150, values=fonts, dynamic_resizing=False)
            combo.set(vals["default"])
            combo.pack(side="right", padx=10, pady=10)
            combo.configure(command=vals["callback"])
            head = CTkLabel(frame, text=header)
            head.pack(side="right", padx=(10, 0), pady=10)
            frame.after(100, lambda: vals["callback"](vals["default"])) # Added this because sometimes the font family changes randomly. Probably a bug in customtkinter.

            self.options[key] = [head, combo]

        elif TYPE == "LISTBOX":
            frame = CTkFrame(self.ctab, height=250)
            frame.pack(padx=10, pady=(10, 0), fill="x")

            scrl_box = CTkScrollableFrame(frame, label_text=header)
            scrl_box.pack(padx=5, pady=5, fill="x")

            for l in vals["default_vals"]:
                self.add_value(scrl_box, l, vals["callback"])


            temp = CTkFrame(frame, height=35, fg_color="transparent")
            temp.pack(padx=5, pady=(0, 5), fill="x")
            temp.pack_propagate(False)

            entry = CTkEntry(temp, placeholder_text="Enter value")
            entry.pack(side="left", fill="x", expand="True")

            btn = CTkButton(temp, text="Add", width=50, command=lambda: (self.add_value_and_call_callback(scrl_box, entry.get(), vals["callback"]), entry.delete(0, "end")))
            btn.pack(side="right", padx=(3, 0))

        elif TYPE == "IMAGE":
            frame = CTkFrame(self.ctab, height=75)
            frame.pack(padx=10, pady=(10, 0), fill="x")

            temp = CTkFrame(frame, height=60, fg_color="transparent")
            temp.pack(padx=10, fill="x", pady=(15, 5))

            discard_btn = CTkButton(temp, text="X", width=10)
            discard_btn.pack(side="right", padx=(5, 0))

            image_btn = CTkButton(temp, text="None", width=120)
            image_btn.pack(side="right", padx=(10, 0))


            head = CTkLabel(temp, text=header)
            head.pack(side="right", padx=(10, 0))

            img_lbl = CTkLabel(frame, width=150, text="", font=CTkFont(size=1), height=1)
            img_lbl.pack(fill="x", padx=10, pady=(0, 10))

            frame1 = CTkFrame(frame, height=75, fg_color="transparent")
            frame1.pack(padx=10, pady=(0, 10), fill="x")

            num_spinbox = Spinbox(frame1, width=150)
            num_spinbox.pack(side="right", padx=(10, 0), pady=10)

            frame1.pack_forget()

            head = CTkLabel(frame1, text="Width")
            head.pack(side="right", padx=(10, 0), pady=10)

            frame2 = CTkFrame(frame, height=75, fg_color="transparent")
            frame2.pack(padx=10, pady=(0, 10), fill="x")

            num_spinbox2 = Spinbox(frame2, width=150)
            num_spinbox2.pack(side="right", padx=(10, 0), pady=10)

            frame2.pack_forget()

            head2 = CTkLabel(frame2, text="Height")
            head2.pack(side="right", padx=(10, 0), pady=10)

            image_btn.configure(command=lambda: self._choose_image(vals["callback"], image_btn, img_lbl, frame, num_spinbox, frame2, num_spinbox2))
            discard_btn.configure(command=lambda: self._discard(vals, img_lbl, image_btn, frame, num_spinbox, frame2, num_spinbox2))
            frame = frame1 # I am toooooo Lazy. I should rename it properly
            if vals["image"] is not None:
                n = 15
                if os.path.basename(os.path.dirname(vals["image"])) == "Assets":
                    vals["image"] = os.path.join(os.path.join(str(pathlib.PurePath(vals["image"]).parent.parent), "temp"), str(pathlib.PurePath(vals["image"]).name))

                if type(vals["image"]) == str:
                    if len(vals["image"]) > n:
                        txt = "..." + vals["image"][len(vals["image"]) - (n - 3)::]
                    else:
                        txt = vals["image"]
                else:
                    txt = "Icon"
                # txt = textwrap.shorten(file, width=10, placeholder="...")
                num_spinbox.set_command(command=lambda val: (vals["callback"](vals["image"], (val, num_spinbox2.get()))))
                num_spinbox2.set_command(command=lambda val: (vals["callback"](vals["image"], (num_spinbox.get(), val))))


                image_btn.configure(text=txt, width=120)
                img = Image.open(vals["image"])
                img.thumbnail((200, 200))
                frame.pack(padx=10, pady=(0, 10), fill="x")
                frame2.pack(padx=10, pady=(0, 10), fill="x")
                num_spinbox.set(img.size[0])
                num_spinbox2.set(img.size[1])
                vals["callback"](vals["image"], (int(num_spinbox.get()), int(num_spinbox2.get())))

                img = CTkImage(img, size=img.size)
                img_lbl.configure(image=img)
            self.options[key] = [head, image_btn]

    def get_vals(self, scrl):
        l = []
        for widgets in scrl.winfo_children():
            for widget in widgets.winfo_children():
                print(widget)
                if type(widget) == CTkLabel:
                    l.append(widget.cget("text"))
        return l

    def add_value(self, scrl, val, callback):

        temp = CTkFrame(scrl, height=40)
        temp.pack(fill="x", pady=(5, 0))
        temp.pack_propagate(False)

        delete_btn = CTkButton(temp, text="X", width=20, height=20,
                               command=lambda: (temp.destroy(), callback(self.get_vals(scrl))))
        delete_btn.pack(side="left", padx=(10, 6))

        lbl = CTkLabel(temp, text=val, anchor="w")
        lbl.pack(side="left")



    def add_value_and_call_callback(self, scrl, val, callback):

        temp = CTkFrame(scrl, height=40)
        temp.pack(fill="x", pady=(5, 0))
        temp.pack_propagate(False)

        delete_btn = CTkButton(temp, text="X", width=20, height=20, command=lambda : (temp.destroy(), callback(self.get_vals(scrl))))
        delete_btn.pack(side="left", padx=(10, 6))

        lbl = CTkLabel(temp, text=val, anchor="w")
        lbl.pack(side="left")

        callback(self.get_vals(scrl))




    def update_color_and_call_callback(self, head, clr_1, clr_2, vals):

        if head.get() == 1:
            clr_1.configure(state="normal")
            clr_2.configure(state="normal")
            if (type(clr_1.cget("fg_color")) == list):
                vals["callback"]((clr_1.cget("fg_color")[0], clr_1.cget("fg_color")[0]))
                color = clr_1.cget("fg_color")[0]

            else:
                vals["callback"]((clr_1.cget("fg_color"), clr_1.cget("fg_color")))
                color = clr_1.cget("fg_color")

            print(color)
            clr_1.configure(fg_color=color)
            clr_2.configure(fg_color=color)
        else:
            clr_1.configure(state="disabled")
            clr_2.configure(state="disabled")
            vals["callback"]("transparent")
    def _discard(self, vals, img_lbl, image_btn, frame, num_spinbox, frame2, num_spinbox2):

        vals["callback"](None, (0, 0))
        img_lbl.configure(image="", height=1)
        image_btn.configure(text="None")
        num_spinbox.set_command(command=None)
        frame.pack_forget()

        num_spinbox2.set_command(command=None)
        frame2.pack_forget()

    def choose(self, callback, btn, lbl, frame, num_spinbox, frame2, num_spinbox2, file):
        if file != "":
            n = 15
            if type(file) == str:
                if len(file) > n:
                    txt = "..." + file[len(file)-(n-3)::]
                else:
                    txt = file
            else:
                txt = "Icon"
            #txt = textwrap.shorten(file, width=10, placeholder="...")
            btn.configure(text=txt, width=120)
            if type(file) == str:
                img = Image.open(file)
                img.thumbnail((200, 200))
            else:
                img = file.thumbnail((200, 200))
            frame.pack(padx=10, pady=(0, 10), fill="x")
            num_spinbox.set(img.size[0])
            num_spinbox.set_command(command=lambda val: callback(file, (int(val), int(num_spinbox2.get()))))

            frame2.pack(padx=10, pady=(0, 10), fill="x")
            num_spinbox2.set(img.size[1])
            num_spinbox2.set_command(command=lambda val: callback(file, (int(num_spinbox.get()), int(val))))

            img = CTkImage(img, size=img.size)
            lbl.configure(image=img)
            #print("       ", (int(num_spinbox.get()), int(num_spinbox2.get())))
            callback(file, (int(num_spinbox.get()), int(num_spinbox2.get())))

    def _choose_image(self, callback, btn, lbl, frame, num_spinbox, frame2, num_spinbox2):
        #file = askopenfilename(filetypes=[(".png", "png"), (".jpg", "jpg"), (".jpeg", "jpeg"), (".JPEG", "JPEG"), (".PNG", "PNG")])
        file = ImageChooser(callback=lambda file: self.choose(callback, btn, lbl, frame, num_spinbox, frame2, num_spinbox2, file))




    def _color_chooser_btn1(self, btn, btn2, callback):
        clr = askcolor(initialcolor=btn.cget("fg_color"))[1]

        if clr is not None:
            btn.configure(fg_color=clr)

            callback((clr, btn2.cget("fg_color")))



    def _color_chooser_btn2(self, btn, btn2, callback):
        clr = askcolor(initialcolor=btn2.cget("fg_color"))[1]

        if clr is not None:
            print((btn.cget("fg_color"), clr))
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
        # Just make sure it works
        if type == "SPINBOX":
            option = self.options[key]
            option[1].set(vals["val"])
            option[2].set(vals["val"])




    def destroy_children(self):
        for frame in [self.GEOMETRY_CONTENT, self.ARRANGEMENT, self.STYLES, self.LAYOUT]:
            for widget in frame.winfo_children():
                widget.destroy()