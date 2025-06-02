import pathlib
import shutil
import uuid
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename
import icecream
from icecream import ic
from tkinterdnd2 import TkinterDnD, DND_ALL
import math
from customtkinter import *
from typing import Union, Callable
from tkinter import font, messagebox
from PIL import Image, ImageTk
import requests
from .get_path import resource_path, tempify


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
        self.after(20, self.lift)
        self.after(25, self.focus_get)
        self.wm_iconbitmap()
        self.iconpath = ImageTk.PhotoImage(file=resource_path('Logo.ico'))
        self.after(100, lambda: self.iconphoto(False, self.iconpath))

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

        #self.icon_color = CTkOptionMenu(self.color_fr, width=250,
        #                                  values=["Black", "White"])
        #self.icon_color.pack(pady=10, side="left", padx=20)

        self.icon_color = CTkButton(self.color_fr, width=250, border_width=2, border_color="#FFFFFF", fg_color="#FFFFFF", command=self.get_color, hover=False, text="")
        self.icon_color.pack(pady=10, side="left", padx=20)
        self.icon_color.color = (255, 255, 255)

        self.img_lbl = CTkLabel(self.fr, text="")
        self.img_lbl.grid(row=2, column=1, pady=20, padx=20)


        self.temp_fr = CTkFrame(self.tab.tab("Icon"))
        self.temp_fr.pack(fill="x")

        self.download_btn = CTkButton(self.temp_fr, text="Download", height=40, command=lambda : self.get_icon(self.icon_name.get(), self.icon_type.get(), self.icon_size.get(), self.icon_density.get(), self.img_lbl))
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

    def get_color(self):
        color = askcolor(initialcolor=self.icon_color.color)
        if color != (None, None):
            new_color = (math.floor(color[0][0]), math.floor(color[0][1]), math.floor(color[0][2]))
            self.icon_color.color = new_color
            self.icon_color.configure(fg_color=color[1])


    def kill(self):
        self.callback(self.image)
        self.destroy()

    def choose_file(self):
        file = askopenfilename(filetypes=[(".png", "png"), (".jpg", "jpg"), (".PNG", "PNG"), (".JPG", "JPG"), (".jpeg", "jpeg"), (".JPEG", "JPEG")])
        if file != "":
            shutil.copy2(file, tempify("temp"))

            self.image = tempify(os.path.join("temp", os.path.basename(file)))
            #self.image.save(f"{tempify(os.path.join('temp', f'{n}_{name}_{self.image.color_type}_{size}_{density}.png'))}")
            self.callback(self.image)
            #print(self.image)
            self.destroy()
    def open_file(self, event):
        if event.data.endswith(".png") or event.data.endswith(".PNG") or event.data.endswith(".jpg") or event.data.endswith(".JPG") or event.data.endswith(".JPEG") or event.data.endswith(".jpeg"):
            #print(event.data)
            shutil.copy2(event.data, tempify("temp"))

            self.image = tempify(os.path.join("temp", os.path.basename(event.data)))

            #self.image = event.data
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

        new_color = self.icon_color.color
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
                if alpha != 0:
                    red_new = new_color[0]
                    green_new = new_color[1]
                    blue_new = new_color[2]

                    new_img.putpixel((x, y), (red_new, green_new, blue_new, alpha))
        # Save the grayscale image
        return new_img, str(new_color)

    def get_icon(self, name, type_, size, density, display):


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
        #print(url)

        response = requests.get(url, stream=True)
        response.raw.decode_content = True

        if response.ok:
            image = Image.open(response.raw)
            if image.mode == "LA":
                image = image.convert("RGBA")
            image, color = self.change_color_to_white(image)

            self.image = image
            self.image.color_type = color
            self.image.url = url
            self.image.save(f"{tempify(os.path.join('temp', f'{n}_{name}_{self.image.color_type}_{size}_{density}.png'))}")
            self.image = f"{tempify(os.path.join('temp', f'{n}_{name}_{self.image.color_type}_{size}_{density}.png'))}"
            print(self.image)

            display.configure(image=CTkImage(light_image=image, dark_image=image, size=(image.size[0], image.size[1])))

            self.use_btn.configure(state="normal")

        else:
            messagebox.showinfo("Error", f"'{name}' icon doesn't exist")



        


class Spinbox(CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: Union[int] = 1,
                 command: Callable = None,
                 positive=True,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command
        self.long_press = False
        self.timeperiod = 0
        self.positive = positive
        #self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = CTkButton(self, text="-", width=height-6, height=height-6,
                                                       command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)
        self.subtract_button.bind("<Button-1>", lambda e: self.set_long_press(True, "SUB"))
        self.subtract_button.bind("<ButtonRelease>", lambda e: self.set_long_press(False, "SUB"))

        self.entry = CTkEntry(self, width=width-(2*height), height=height-6, border_width=0, justify="center", state="disabled")
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")
        self.entry.bind("<Button-1>", self.double)


        self.add_button = CTkButton(self, text="+", width=height-6, height=height-6,
                                                  command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)
        self.add_button.bind("<Button-1>", lambda e: self.set_long_press(True, "ADD"))
        self.add_button.bind("<ButtonRelease>", lambda e: self.set_long_press(False, "ADD"))
        # default value
        self.entry.configure(state="normal")
        self.entry.insert(0, "0")
        self.entry.configure(state="disabled")
        self.entry.bind("<FocusOut>", lambda e: (self.command(self.entry.get()), self.entry.configure(state="disabled"), self.main.r.winfo_toplevel().update_idletasks(),self.main.draw_box(self.main.hierarchy.widget)))

    def return_set(self, e):

        self.command(self.get())
        self.entry.configure(state="disabled")
        self.entry.unbind("<Return>")
        self.main.r.winfo_toplevel().update_idletasks()
        self.main.draw_box(self.main.hierarchy.widget)


    def double(self, e):
        self.entry.configure(state="normal")
        self.entry.bind("<Return>", self.return_set)

    def do_checks(self, add_or_sub, id):
        if self.long_press and self.id == id:
            if add_or_sub == "ADD":
                self.add_button_callback()
            elif add_or_sub == "SUB":
                self.subtract_button_callback()
            self.winfo_toplevel().after(30, lambda: self.do_checks(add_or_sub, id))


    def set_long_press(self, state, add_or_sub):
        self.long_press = state

        if self.long_press:
            self.id = str(uuid.uuid4())
            self.winfo_toplevel().after(750, lambda: self.do_checks(add_or_sub, id=self.id))




    def add_button_callback(self):

        try:
            value = int(float(self.entry.get())) + self.step_size
            if value < 0 and self.positive:
                value = int(float(self.entry.get()))
            self.entry.configure(state="normal")
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
            self.entry.configure(state="disabled")

        except ValueError as e:
            #print(e)
            return
        if self.command is not None:
            self.command(self.get())
            self.main.draw_box(self.main.hierarchy.widget)

    def subtract_button_callback(self):

        try:
            value = int(self.entry.get()) - self.step_size
            if value < 0 and self.positive:
                value = int(float(self.entry.get()))
            self.entry.configure(state="normal")
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
            self.entry.configure(state="disabled")

        except ValueError:
            return
        if self.command is not None:
            self.command(self.get())
            self.main.draw_box(self.main.hierarchy.widget)

    def get(self) -> Union[int, None]:
        try:
            return self.entry.get()
        except ValueError:
            return None

    def set(self, value: int):
        self.entry.configure(state="normal")

        self.entry.delete(0, "end")
        self.entry.insert(0, str(int(value)))

        self.entry.configure(state="disabled")

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

class ColorManager:
    def __init__(self, main):
        self.colors = {}
        self.on_change_list = {}
        self.main = main

    def check_on_list(self, id, key, mode):
        for x in self.on_change_list.keys():
            vals = self.on_change_list[x]
            for val in vals:
                if id in val and key in val and mode in val:
                    return [x, self.on_change_list[x].index(val)]

    def get_all_changes(self, id):
        l = []
        for x in self.on_change_list.keys():
            vals = self.on_change_list[x]
            for val in vals:
                if id in val:
                     l.append([x, val])
        return l


    def add_color(self, name, color):
        if name not in list(self.colors.keys()):
            self.colors[name] = color
            self.on_change_list[name] = []

    def on_change(self, name, command):
        vals = self.on_change_list[name]
        vals.append(command)
        self.on_change_list[name] = vals

    def edit(self, name, val):
        ic(name)
        if len(self.on_change_list[name]) > 0:
            for x in self.on_change_list[name]:
                try:
                    widget = self.main.id_mapped_widgets[x[0]]
                    if x[2] == "dark":
                        d = {x[1]: [widget.cget(x[1])[0], val]}
                    else:
                        d = {x[1]: [val, widget.cget(x[1])[1]]}
                    widget.save(lambda v: widget.configure(**d), x[1], d[x[1]], d[x[1]])
                    ic(widget._inner_id, d, [widget.cget("fg_color"), val])
                except Exception as e:
                    ic("Error", e)
        self.colors[name] = val

    def get_color(self, name):
        return self.colors[name]

    def delete_color(self, name):
        self.colors.pop(name)
        self.on_change_list.pop(name)



class ColorPicker(CTkToplevel):
    def __init__(self, *args, color=(255, 255, 255), color_manager, command=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x500")
        self.title("Color Picker")
        self.color = color
        self.command = command
        self.current_selection = [None, None]
        self.clickables = []
        self.color_manager = color_manager
        self.scrl = CTkScrollableFrame(self)
        self.scrl.pack(fill="both", expand=True, padx=10, pady=(10, 0))
        self.fr = CTkFrame(self)
        self.fr.pack(padx=10, pady=10, fill="x")
        self.after(20, self.lift)
        self.after(25, self.focus_get)
        self.wm_iconbitmap()
        self.iconpath = ImageTk.PhotoImage(file=resource_path('Logo.ico'))
        self.after(100, lambda: self.iconphoto(False, self.iconpath))


        self.c = CTkButton(self.fr, width=100, height=100, text="", fg_color=self.color, hover=False, command=self.get_color)
        self.c.pack(side="left")

        self.hex = CTkLabel(self.fr, text=f"HEX: {self.color}", anchor="w")
        self.hex.pack(fill="x", padx=10, pady=10, expand=True)


        self.rgb = CTkLabel(self.fr, text=f"RGB: {self.hex_to_rgb(self.color)}", anchor="w")
        self.rgb.pack(fill="x", padx=10, pady=(0, 10), expand=True)

        self.use_btn = CTkButton(self.fr, text=f"Use", command=self.use)
        self.use_btn.pack(fill="x", padx=10, pady=(0, 10), expand=True)

        for x in list(self.color_manager.colors.keys()):
            self.add_color_option(x, self.color_manager.get_color(x))

    def hex_to_rgb(self, value):
        try:
            value = value.lstrip('#')
            lv = len(value)
            return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
        except:
            return ""
    def select(self, name, val):
        self.current_selection = [name, val]
        self.c.configure(fg_color=self.color_manager.get_color(name))
        self.hex.configure(text=f"HEX: {self.color_manager.get_color(name)}")
        self.rgb.configure(text=f"RGB: {self.hex_to_rgb(self.color_manager.get_color(name))}")

    def add_color_option(self, name, val):
        c = CTkFrame(self.scrl, height=100)
        c.pack(fill="x", pady=10)

        clr = CTkFrame(c, width=75, height=75, fg_color=val)
        clr.pack(side="left", padx=10)

        fr = CTkFrame(c)
        fr.pack(side="left", fill="both", expand=True)

        lbl = CTkLabel(fr, text=name, anchor="w", font=CTkFont(size=17))
        lbl.pack(fill="x", expand=True, padx=10, pady=10)

        lbl2 = CTkLabel(fr, text=val, anchor="w")
        lbl2.pack(fill="x", expand=True, padx=10, pady=(0, 10))

        for x in [c, clr, fr, lbl, lbl2]:
            x.bind("<Button-1>", lambda e, name=name, val=val: (self.select(name, val), self.change_selection([fr, c])))
        self.clickables.append([fr, c])
    def get_color(self):
        c = askcolor(initialcolor=self.c.cget("fg_color"))
        if c != (None, None):
            self.c.configure(fg_color=c[1])
            for x in self.clickables:
                for y in x:
                    y.configure(fg_color="transparent")

            self.current_selection = [None, None]

    def use(self):
        if self.command != None:
            self.command(self.c.cget("fg_color"), self.current_selection)
            self.destroy()


    def change_selection(self, clr):
        for x in self.clickables:
            for y in x:
                y.configure(fg_color="transparent")
        for x in clr:
            x.configure(fg_color="#1F6AA5")

    def rgb2hex(self, c):
        return '#%02x%02x%02x' % c

class CustomCTkComboBox(CTkComboBox):
    def __init__(self, *args, **kwargs):
        super(CustomCTkComboBox, self).__init__(*args, **kwargs)
        self.main = None

    def _dropdown_callback(self, value: str):
        super()._dropdown_callback(value=value)
        self.update_idletasks()
        self.main.draw_box(self.main.hierarchy.widget)

    def _create_grid(self):
        self._canvas.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nsew")

        left_section_width = self._current_width - self._current_height
        self._entry.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="ew",
                         padx=(max(self._apply_widget_scaling(8), self._apply_widget_scaling(3)),
                               max(self._apply_widget_scaling(self._current_width - left_section_width + 3),
                                   self._apply_widget_scaling(3))),
                         pady=self._apply_widget_scaling(self._border_width))
        self._entry.bind("<Button-1>", self._clicked)
        if sys.platform == "darwin":
            self._entry.configure(cursor="pointinghand")
            self._canvas.configure(cursor="pointinghand")
        elif sys.platform.startswith("win"):
            self._entry.configure(cursor="hand2")
            self._canvas.configure(cursor="hand2")






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
        self.color_manager = ColorManager(main=self.main)

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





    def add_seperator(self, s, head):
        frame = CTkFrame(s, height=75)
        frame.pack(padx=10, pady=(10, 0), fill="x")

        txt = CTkLabel(frame, text=head)
        txt.pack(fill="x")


    def add_option(self, category, header, TYPE, key, vals):
        self.ctab = category

        if TYPE == "SPINBOX":
            frame = CTkFrame(self.ctab, height=75, fg_color=self.master.master.cget("fg_color"))
            frame.pack(padx=10, pady=(10, 0), fill="x")

            num_spinbox = Spinbox(frame, width=150, command=lambda val: vals["callback"](val))
            num_spinbox.pack(side="right", padx=(10, 10), pady=10)
            num_spinbox.set(vals["val"])
            num_spinbox.main = self.main


            head = CTkLabel(frame, text=header)
            head.pack(side="right", padx=(10, 0), pady=10)

            self.options[key] = [head, num_spinbox]

        elif TYPE == "TEXT":
            frame = CTkFrame(self.ctab, height=75, fg_color=self.master.master.cget("fg_color"))
            frame.pack(padx=10, pady=(10, 0), fill="x")


            sv = StringVar()
            sv.trace_add("write", lambda e1, e2, e3: (vals["callback"](sv.get()), self.main.r.winfo_toplevel().update_idletasks(), self.main.draw_box(self.main.hierarchy.widget)))
            entry = TextExtension(frame, width=150, height=100, textvariable=sv)
            entry.pack(side="right", padx=10, pady=10)
            head = CTkLabel(frame, text=header)
            head.pack(side="right", padx=(10, 0), pady=10)

            sv.set(vals["val"])
            self.options[key] = [head, entry]


        elif TYPE == "SINGLELINE_TEXT":
            frame = CTkFrame(self.ctab, height=75, fg_color=self.master.master.cget("fg_color"))
            frame.pack(padx=10, pady=(10, 0), fill="x")


            sv = StringVar()
            sv.trace_add("write", lambda e1, e2, e3: vals["callback"](sv.get()))
            entry = CTkEntry(frame, width=150, textvariable=sv, border_width=1)
            entry.pack(side="right", padx=10, pady=10)
            head = CTkLabel(frame, text=header)
            head.pack(side="right", padx=(10, 0), pady=10)

            sv.set(vals["val"])
            self.options[key] = [head, entry]

        elif TYPE == "TUPLE":
            frame = CTkFrame(self.ctab, height=75, fg_color=self.master.master.cget("fg_color"))
            frame.pack(padx=10, pady=(10, 0), fill="x")

            temp = CTkFrame(frame, height=60, fg_color=frame.cget("fg_color"))
            temp.pack(side="right", fill="x", pady=10)

            num_spinbox_1 = Spinbox(temp, width=150, positive=True, command=lambda val: (
            vals["callback"](int(val), int(num_spinbox_2.get()))))
            num_spinbox_1.pack(padx=(10, 10))
            num_spinbox_1.set(vals["val1"])
            num_spinbox_1.main = self.main


            num_spinbox_2 = Spinbox(temp, width=150, positive=True, command=lambda val: (
            vals["callback"](int(num_spinbox_1.get()), int(val))))
            num_spinbox_2.pack(padx=(10, 10), pady=(10, 0))

            num_spinbox_2.set(vals["val2"])
            num_spinbox_2.main = self.main


            head = CTkLabel(frame, text=header)
            head.pack(side="right", padx=(10, 0), pady=10)



            self.options[key] = [head, num_spinbox_1, num_spinbox_2]

        elif TYPE == "COMBO":
            frame = CTkFrame(self.ctab, height=75, fg_color=self.master.master.cget("fg_color"))
            frame.pack(padx=10, pady=(10, 0), fill="x")

            combo = CustomCTkComboBox(frame, width=150, values=vals["vals"], command=vals["callback"], state="readonly")
            combo.set(vals["default"])
            combo.main = self.main
            combo.pack(side="right", padx=10, pady=10)
            head = CTkLabel(frame, text=header)
            head.pack(side="right", padx=(10, 0), pady=10)
            self.options[key] = [head, combo]

        elif TYPE == "COLOR_COMBO":
            frame = CTkFrame(self.ctab, height=75, fg_color=self.master.master.cget("fg_color"))
            frame.pack(padx=10, pady=(10, 0), fill="x")

            temp = CTkFrame(frame, height=60, fg_color="transparent")
            temp.pack(side="right", fill="x", pady=10)

            clr_1 = CTkButton(temp, width=150//2-2, hover=False, text="", border_width=2)
            clr_1.pack(padx=(0, 2), side="left", fill="x")
            clr_1.configure(command=lambda: self._color_chooser_btn1(clr_1, clr_2, vals["callback"], key=vals["key"]))

            clr_2 = CTkButton(temp, width=150//2-1, hover=False, text="", border_width=2)
            clr_2.pack(padx=(2, 10), side="left", fill="x")
            clr_2.configure(command=lambda: self._color_chooser_btn2(clr_1, clr_2, vals["callback"], key=vals["key"]))


            if vals["transparent"]:
                head = CTkCheckBox(frame, text=header)
                head.pack(side="right", padx=(10, 0), pady=10)
                head.configure(command=lambda: self.update_color_and_call_callback(head, clr_1, clr_2, vals))
            else:
                head = CTkLabel(frame, text=header)
                head.pack(side="right", padx=(10, 10), pady=10)

            if vals["color"] != "transparent":
                #print(vals["color"])
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
            frame = CTkFrame(self.ctab, height=75, fg_color=self.master.master.cget("fg_color"))
            frame.pack(padx=10, pady=(10, 0), fill="x")
            fonts = list(font.families())
            fonts.sort()
            combo = CustomCTkComboBox(frame, width=150, values=fonts, state="readonly", command=vals["callback"])
            combo.set(vals["default"])
            combo.pack(side="right", padx=10, pady=10)
            combo.main = self.main

            #combo.configure()
            head = CTkLabel(frame, text=header)
            head.pack(side="right", padx=(10, 0), pady=10)
            # Added this because sometimes the font family changes randomly. Probably a bug in customtkinter.
            frame.after(200, lambda: (vals["callback"](vals["default"]), combo.set(vals["default"])))

            self.options[key] = [head, combo]

        elif TYPE == "LISTBOX":
            frame = CTkFrame(self.ctab, height=250, fg_color=self.master.master.cget("fg_color"))
            frame.pack(padx=10, pady=(10, 0), fill="x")

            scrl_box = CTkScrollableFrame(frame, label_text=header, label_fg_color="transparent")
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
            frame = CTkFrame(self.ctab, height=75, fg_color=self.master.master.cget("fg_color"))
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
            num_spinbox.main = self.main

            frame1.pack_forget()

            head = CTkLabel(frame1, text="Width")
            head.pack(side="right", padx=(10, 0), pady=10)

            frame2 = CTkFrame(frame, height=75, fg_color="transparent")
            frame2.pack(padx=10, pady=(0, 10), fill="x")

            num_spinbox2 = Spinbox(frame2, width=150)
            num_spinbox2.pack(side="right", padx=(10, 0), pady=10)
            num_spinbox2.main = self.main

            frame2.pack_forget()

            head2 = CTkLabel(frame2, text="Height")
            head2.pack(side="right", padx=(10, 0), pady=10)

            image_btn.configure(command=lambda: self._choose_image(vals["callback"], image_btn, img_lbl, frame, num_spinbox, frame2, num_spinbox2))
            discard_btn.configure(command=lambda: self._discard(vals, img_lbl, image_btn, frame, num_spinbox, frame2, num_spinbox2))
            frame = frame1 # I am toooooo Lazy. I should rename it properly
            if vals["image"] is not None:
                n = 15
                if os.path.basename(os.path.dirname(vals["image"])) == "Assets":
                    vals["image"] = os.path.join(os.path.join(str(pathlib.PurePath(vals["image"]).parent.parent), tempify(
                        "temp")), str(pathlib.PurePath(vals["image"]).name))

                if type(vals["image"]) == str:
                    if len(vals["image"]) > n:
                        txt = "..." + vals["image"][len(vals["image"]) - (n - 3)::]
                    else:
                        txt = vals["image"]
                else:
                    txt = "Icon"
                # txt = textwrap.shorten(file, width=10, placeholder="...")
                num_spinbox.set_command(command=lambda val: (vals["callback"](vals["image"], (int(val), int(num_spinbox2.get())))))
                num_spinbox2.set_command(command=lambda val: (vals["callback"](vals["image"], (int(num_spinbox.get()), int(val)))))


                image_btn.configure(text=txt, width=120)
                try:
                    img = Image.open(vals["image"])
                except FileNotFoundError as e:
                    img = Image.open(tempify(vals["image"]))
                    vals["image"] = tempify(vals["image"])

                frame.pack(padx=10, pady=(0, 10), fill="x")
                frame2.pack(padx=10, pady=(0, 10), fill="x")
                if vals["size"]() is not None:
                    num_spinbox.set(vals["size"]()[0])
                    num_spinbox2.set(vals["size"]()[1])
                else:
                    num_spinbox.set(img.size[0])
                    num_spinbox2.set(img.size[1])

                vals["callback"](vals["image"], (int(num_spinbox.get()), int(num_spinbox2.get())))
                img.thumbnail((200, 200))

                img = CTkImage(img, size=img.size)
                img_lbl.configure(image=img)
            self.options[key] = [head, image_btn]

    def get_vals(self, scrl):
        l = []
        for widgets in scrl.winfo_children():
            for widget in widgets.winfo_children():
                #print(widget)
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
        key = vals["key"]
        if head.get() == 1:
            clr_1.configure(state="normal")
            clr_2.configure(state="normal")
            for mode in ["light", "dark"]:
                ic(self.color_manager.check_on_list(self.main.hierarchy.widget._inner_id, key, mode))

                val = self.color_manager.check_on_list(self.main.hierarchy.widget._inner_id, key, mode)
                if val is not None:
                    arr = self.color_manager.on_change_list[val[0]]
                    arr.pop(val[1])
                    self.color_manager.on_change_list[val[0]] = arr
                ic(self.color_manager.check_on_list(self.main.hierarchy.widget._inner_id, key, mode))
                ic(self.color_manager.on_change_list, self.main.hierarchy.widget._inner_id, key)
            if (type(clr_1.cget("fg_color")) == list):
                vals["callback"]((clr_1.cget("fg_color")[0], clr_1.cget("fg_color")[0]))
                color = clr_1.cget("fg_color")[0]

            else:
                vals["callback"]((clr_1.cget("fg_color"), clr_1.cget("fg_color")))
                color = clr_1.cget("fg_color")

            #print(color)
            clr_1.configure(fg_color=color)
            clr_2.configure(fg_color=color)
        else:
            for mode in ["light", "dark"]:
                ic(self.color_manager.check_on_list(self.main.hierarchy.widget._inner_id, key, mode))

                val = self.color_manager.check_on_list(self.main.hierarchy.widget._inner_id, key, mode)
                if val is not None:
                    arr = self.color_manager.on_change_list[val[0]]
                    arr.pop(val[1])
                    self.color_manager.on_change_list[val[0]] = arr
                ic(self.color_manager.check_on_list(self.main.hierarchy.widget._inner_id, key, mode))
                ic(self.color_manager.on_change_list, self.main.hierarchy.widget._inner_id, key)
            clr_1.configure(state="disabled")
            clr_2.configure(state="disabled")
            vals["callback"]("transparent")
    def _discard(self, vals, img_lbl, image_btn, frame, num_spinbox, frame2, num_spinbox2):

        vals["callback"]("", (0, 0))
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
            ##print("       ", (int(num_spinbox.get()), int(num_spinbox2.get())))
            callback(file, (int(num_spinbox.get()), int(num_spinbox2.get())))

    def _choose_image(self, callback, btn, lbl, frame, num_spinbox, frame2, num_spinbox2):
        #file = askopenfilename(filetypes=[(".png", "png"), (".jpg", "jpg"), (".jpeg", "jpeg"), (".JPEG", "JPEG"), (".PNG", "PNG")])
        file = ImageChooser(callback=lambda file: self.choose(callback, btn, lbl, frame, num_spinbox, frame2, num_spinbox2, file))

    def btn1_color_command(self, color, c, btn, btn2, callback, key):
        btn.configure(fg_color=color)

        callback((color, btn2.cget("fg_color")))

        val = self.color_manager.check_on_list(self.main.hierarchy.widget._inner_id, key, "light")
        if val is not None:
            arr = self.color_manager.on_change_list[val[0]]
            arr.pop(val[1])
            self.color_manager.on_change_list[val[0]] = arr
        ic(self.color_manager.check_on_list(self.main.hierarchy.widget._inner_id, key, "light"))

        if c != [None, None]:
            #self.color_manager.on_change(c[0], lambda val, btn2=btn2: callback((val, btn2.cget("fg_color"))))
            #print([self.main.hierarchy.widget._inner_id, key, "light"])

            self.color_manager.on_change(c[0], [self.main.hierarchy.widget._inner_id, key, "light"])

        ic(self.color_manager.on_change_list)


    def _color_chooser_btn1(self, btn, btn2, callback, key):
        #clr = askcolor(initialcolor=btn.cget("fg_color"))[1]
        clr = ColorPicker(color=btn.cget("fg_color"),  color_manager=self.color_manager,command=lambda e, p: self.btn1_color_command(e, p, btn, btn2, callback, key))

    def btn2_color_command(self, color, c, btn, btn2, callback, key):

        btn2.configure(fg_color=color)

        callback((btn.cget("fg_color"), color))
        val = self.color_manager.check_on_list(self.main.hierarchy.widget._inner_id, key, "dark")
        if val is not None:
            arr = self.color_manager.on_change_list[val[0]]
            arr.pop(val[1])
            self.color_manager.on_change_list[val[0]] = arr
        ic(self.color_manager.check_on_list(self.main.hierarchy.widget._inner_id, key, "dark"))

        if c != [None, None]:
            #print([self.main.hierarchy.widget._inner_id, key, "dark"])
            self.color_manager.on_change(c[0], [self.main.hierarchy.widget._inner_id, key, "dark"])
        ic(self.color_manager.on_change_list)


    def _color_chooser_btn2(self, btn, btn2, callback, key):
        #clr = askcolor(initialcolor=btn2.cget("fg_color"))[1]
        clr = ColorPicker(color=btn2.cget("fg_color"), color_manager=self.color_manager,
                          command=lambda e, p: self.btn2_color_command(e, p, btn, btn2, callback, key))




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
