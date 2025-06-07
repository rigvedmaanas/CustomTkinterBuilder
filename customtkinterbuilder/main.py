import json
import platform
import threading
import tkinter.messagebox
import uuid
from pathlib import Path
from tkinter import messagebox
from tkinter.colorchooser import askcolor
import pyperclip
from jinja2 import Environment, FileSystemLoader
import darkdetect
import userpaths
from icecream import ic
from .Widgets import *
from .properties import PropertiesManager
from tkinter.filedialog import asksaveasfilename, askdirectory
from customtkinter import *
from .dragndrop import DragManager
from .CodeGenerator import CodeGenerator
from CustomtkinterCodeViewer import CTkCodeViewer
from PIL import Image, ImageTk
from .get_path import resource_path, tempify, joinpath
import autopep8
from customtkinterthemes import theme_manager
from .CustomWidgets.ToolBar import ToolBar
from .CustomWidgets.AppearanceButton import AppearanceButton
from .CustomWidgets.MessageBox import MessageBox
from .Components import *
from re import sub

#ic.disable()
def blockPrint():
    sys.stdout = open(os.devnull, 'w')
#blockPrint()
class ThemeUtl:
    def __init__(self, theme_dir, theme_name: str):
        path = theme_manager.get(theme_name)
        with open(path, "r") as f:
            self.theme = json.load(f)
        self.path = path
        self.name = theme_name

    def change_theme(self, theme_name):
        path = theme_manager.get(theme_name)
        with open(path, "r") as f:
            self.theme = json.load(f)
        self.path = path
        self.name = theme_name

    def get_theme_by_name(self):
        return self.theme

class SaveFileDialog(CTkToplevel):
    def __init__(self, *args, callback, theme=False, **kwargs):
        super().__init__(*args, **kwargs)
        #self.pack_propagate(False)
        self.callback = callback
        self.after(20, self.lift)
        self.after(25, self.focus_get)
        self.wm_iconbitmap()
        self.iconpath = ImageTk.PhotoImage(file=resource_path('Logo.ico'))
        self.after(100, lambda: self.iconphoto(False, self.iconpath))

        if theme:
            self.geometry("500x380+600+200")
            self.title("New Project")

        else:
            self.geometry("500x280+600+200")
            self.title("Save as project")


        self.project_name_lbl = CTkLabel(self, text="Project Name", anchor="w", padx=5, font=CTkFont(size=20))
        self.project_name_lbl.pack(pady=(20, 0), padx=20, fill="x")

        self.project_name_entry = CTkEntry(self, placeholder_text="Enter Project Name")
        self.project_name_entry.pack(padx=20, pady=10, fill="x")
        self.project_name_entry.insert(0, "Untitled")

        self.fr = CTkFrame(self, fg_color="transparent")
        self.fr.pack(fill="x")

        self.dir_lbl = CTkLabel(self.fr, text="Location", anchor="w", padx=5, font=CTkFont(size=20))
        self.dir_lbl.pack(pady=(20, 10), padx=20, fill="x")

        self.dir_entry = CTkEntry(self.fr)
        self.dir_entry.pack(padx=(20, 5), pady=(0, 20), fill="x", side="left", expand=True)
        self.dir_entry.insert(0, userpaths.get_my_documents())
        self.dir_entry.configure(state="disabled")

        self.select_dir = CTkButton(self.fr, text="...", width=20, command=self.choose_dir)
        self.select_dir.pack(side="right", padx=(0, 20), pady=(0, 20))

        if theme:
            self.f = CTkFrame(self, fg_color="transparent")
            self.f.pack(fill="x")

            self.theme_lbl = CTkLabel(self.f, text="Theme", anchor="w", padx=5, font=CTkFont(size=20))
            self.theme_lbl.pack(pady=(20, 10), padx=20, fill="x")

            self.theme_entry = CTkOptionMenu(self.f, values=theme_manager.get_all_themes())
            self.theme_entry.pack(padx=20, pady=(0, 20), fill="x", side="left", expand=True)
            self.theme_entry.set("blue")

            self.save_btn = CTkButton(self, text="Save", height=35, command=lambda: (
            self.callback(dir_=self.dir_entry.get(), name=self.project_name_entry.get(), theme=self.theme_entry.get()), self.destroy()))
            self.save_btn.pack(fill="x", padx=20, pady=20)

        else:
            self.save_btn = CTkButton(self, text="Save", height=35, command=lambda: (self.callback(dir_=self.dir_entry.get(), name=self.project_name_entry.get()), self.destroy()))
            self.save_btn.pack(fill="x", padx=20, pady=20)

    def choose_dir(self):
        dir = askdirectory()
        if dir != "":
            self.dir_entry.configure(state="normal")
            self.dir_entry.delete(0, "end")
            self.dir_entry.insert(0, dir)
            self.dir_entry.configure(state="disabled")



class MainWindow:
    def __init__(self, root, theme_name):
        self.type = "ROOT"
        self.widgets = {}
        self.id_mapped_widgets = {}
        self.hierarchy = None
        self.r = root
        self.widgets[root] = {}
        self.drag_manager = None
        self.properties = None
        self._parents = []
        self.temp_widgets = {}
        self.file = ""
        self.total_num = 0
        self.files_to_copy = []
        self.title = "Window"
        self.theme_manager = ThemeUtl(theme_dir=f"Themes", theme_name=theme_name)
        self.horiz_max_offset = 100
        self.vert_max_offset = 100
        self.current_selected_widget = None
        self.theme = self.theme_manager.get_theme_by_name()
        self.template_env = Environment(loader=FileSystemLoader(os.path.dirname(os.path.abspath(__file__))))
        self.scale = 1
        self.class_map = {
            "CTkButton": "Button",
            "CTkCheckBox": "CheckBox",
            "CTkComboBox": "ComboBox",
            "CTkEntry": "Entry",
            "CTkFrame": "Frame",
            "CTkLabel": "Label",
            "CTkOptionMenu": "OptionMenu",
            "CTkProgressBar": "ProgressBar",
            "CTkRadioButton": "RadioButton",
            "CTkScrollableFrame": "ScrollableFrame",
            "CTkScrollbar": "Scrollbar",
            "CTkSegmentedButton": "SegmentedButton",
            "CTkSlider": "Slider",
            "CTkSwitch": "Switch",
            "CTkTextbox": "TextBox"
        }
        self.windows_open = []

        self.widget_colors = {
            "CTk": ["fg_color"],
            "CTkToplevel": ["fg_color"],
            "CTkFrame": ["fg_color", "border_color"],
            "CTkButton": ["fg_color", "hover_color", "border_color", "text_color", "text_color_disabled"],
            "CTkLabel": ["fg_color", "text_color"],
            "CTkEntry": ["fg_color", "border_color", "text_color", "placeholder_text_color"],
            "CTkCheckBox": ["fg_color", "border_color", "hover_color", "checkmark_color", "text_color", "text_color_disabled"],
            "CTkSwitch": ["fg_color", "progress_color", "button_color", "button_hover_color", "text_color", "text_color_disabled"],
            "CTkRadioButton": ["fg_color", "border_color", "hover_color", "text_color", "text_color_disabled"],
            "CTkProgressBar": ["fg_color", "progress_color", "border_color"],
            "CTkSlider": ["fg_color", "progress_color", "button_color", "button_hover_color"],
            "CTkOptionMenu": ["fg_color", "button_color", "button_hover_color", "text_color", "text_color_disabled"],
            "CTkComboBox": ["fg_color", "border_color", "button_color", "button_hover_color", "text_color", "text_color_disabled"],
            "CTkScrollbar": ["fg_color", "button_color", "button_hover_color"],
            "CTkSegmentedButton": ["fg_color", "selected_color", "selected_hover_color", "unselected_color", "unselected_hover_color", "text_color", "text_color_disabled"],
            "CTkTextbox": ["fg_color", "border_color", "text_color", "scrollbar_button_color", "scrollbar_button_hover_color"],
            "CTkScrollableFrame": ["label_fg_color"],
            "DropdownMenu": ["fg_color", "hover_color", "text_color"]
        }

    def to_camelcase(self, s):
        s = sub(r"(_|-)+", " ", s).title().replace(" ", "").replace("*", "")
        return ''.join([s[0].lower(), s[1:]])

    def generate_component_code(self, class_name):
        component = {self.current_selected_widget: self.traverse_widgets_till_found(self.current_selected_widget, self.widgets)}
        print(component)

        oop_code = CodeGenerator(indentation="    ")

        if self.current_selected_widget.type not in ["FRAME", "SCROLLABLEFRAME", "SLIDER", "SCROLLBAR"]:
            oop_code.add_line(f"""
from .BaseComponent import BaseComponent
from customtkinterbuilder.Widgets import *
from customtkinter import CTkImage
from PIL import Image

class {self.to_camelcase(class_name)}({self.class_map[self.current_selected_widget.get_class()]}, BaseComponent):
    def __init__(self, *args, properties, **kwargs):
        BaseComponent.__init__(self)
        {self.class_map[self.current_selected_widget.get_class()]}.__init__(self, *args, properties=properties, **kwargs)""")
            parameters = self.current_selected_widget.props
            print(parameters)
            if "image" in parameters:
                dst = f"./customtkinterbuilder/ComponentAssets/{class_name}"
                src = parameters["image"].cget("dark_image").filename
                parameters["image"] = "ahifhyhmacpopgbbjajsrwjrvfnmzsikrymjfgjakcjyjtdtfxcxqiowpbrheqlhbvgkhckncvdqjxhisnnvzuayoqpdhuiqlolhblocdokaoaroqwfkqbmtfcnoajnqszlgefvvmzhanfeqmtzkrlivydjigeodcezyahakdilbxlkcbyuchwnotsokqbisednbxethehnmepprylstzkakkmpdnwedvjnrzsvwktiyejzrshqklqnhoimdszccokywzuoboruzpcdqkblxdegiljcyyertfvynbgqdzsvjfqvgxtcqozgzuvcbtgbkdcorikwfqkqlsefoqdcxkkagjunbkhvlpulj" # Just a work around
                parameters = str(parameters)
                parameters = parameters.replace("'ahifhyhmacpopgbbjajsrwjrvfnmzsikrymjfgjakcjyjtdtfxcxqiowpbrheqlhbvgkhckncvdqjxhisnnvzuayoqpdhuiqlolhblocdokaoaroqwfkqbmtfcnoajnqszlgefvvmzhanfeqmtzkrlivydjigeodcezyahakdilbxlkcbyuchwnotsokqbisednbxethehnmepprylstzkakkmpdnwedvjnrzsvwktiyejzrshqklqnhoimdszccokywzuoboruzpcdqkblxdegiljcyyertfvynbgqdzsvjfqvgxtcqozgzuvcbtgbkdcorikwfqkqlsefoqdcxkkagjunbkhvlpulj'", f"CTkImage(light_image=Image.open(os.path.join(tempify('temp'), '{os.path.basename(src)}')), dark_image=Image.open(os.path.join(tempify('temp'), '{os.path.basename(src)}')))")
                self.copy_file_to_nested_dir(src, dst)
                # print(parameters["image"], parameters["image"].dark_image)
                oop_code.add_line(f"        self.copy('{os.path.join(dst, os.path.basename(src))}')")
            oop_code.add_line(f"        {self.class_map[self.current_selected_widget.get_class()]}.save_properties(self, properties={parameters})")
            oop_code.add_line(f"""
    @classmethod
    def as_str(cls):
        return "{class_name}"

    def add_widgets(self, func, properties, widget):
        pass""")
        elif self.current_selected_widget.type in ["SCROLLABLEFRAME", "SLIDER", "SCROLLBAR"]:
            string_ = '{"properties": properties, "orientation": "' + self.current_selected_widget.props.pop("orientation") + '"}'


            oop_code.add_line(f"""
from .BaseComponent import BaseComponent
from customtkinterbuilder.Widgets import *
from customtkinter import CTkImage
from PIL import Image

class {self.to_camelcase(class_name)}({self.class_map[self.current_selected_widget.get_class()]}, BaseComponent):
    def __init__(self, *args, properties, **kwargs):
        BaseComponent.__init__(self)
        prop = {string_}
        {self.class_map[self.current_selected_widget.get_class()]}.__init__(self, *args, **prop, **kwargs)
        {self.class_map[self.current_selected_widget.get_class()]}.save_properties(self, properties={self.current_selected_widget.props})

    @classmethod
    def as_str(cls):
        return "{class_name}"

    def add_widgets(self, func, properties, widget):
        """)
        else:
            oop_code.add_line(f"""
from .BaseComponent import BaseComponent
from customtkinterbuilder.Widgets import *
from customtkinter import CTkImage
from PIL import Image

class {self.to_camelcase(class_name)}(Frame, BaseComponent):
    def __init__(self, *args, properties, **kwargs):
        BaseComponent.__init__(self)
        Frame.__init__(self, *args, properties=properties, **kwargs)
    
    @classmethod
    def as_str(cls):
        return "{class_name}"
    
    def add_widgets(self, func, properties, widget):""")
        oop_code.indent()
        oop_code.indent()
        self.loop_generate_component(d=component[self.current_selected_widget], p="self", code=oop_code, class_name=class_name)
        oop_code.add_line("pass") # If there are no widgets in frame or Scrollable Frame
        return oop_code.get_code()

    def create_component_code(self, class_name):

        if self.current_selected_widget.type == "MAIN":
            self.r.winfo_toplevel().message_box.show(f"{self.current_selected_widget.get_name()} isn't supported in a component")
            return
        if class_name.strip() == "":
            class_name = "Default Component"

        code = self.generate_component_code(class_name)

        file = Path(f"./customtkinterbuilder/Components/{self.to_camelcase(class_name)}.py")
        if file.is_file():
            reply = messagebox.askyesno("Warning", f"{self.to_camelcase(class_name)}.py exists. Do you want to replace the file?")
            if not reply:
                return None
        with open(file, "w") as f:
            f.write(code)


    def create_component(self):

        self.clear_toplevels()
        root = CTkToplevel()

        root.geometry("400x150+500+100")
        root.title("Create Component")
        root.after(20, root.lift)
        root.after(25, root.focus_get)
        self.windows_open.append(root)
        root.wm_iconbitmap()
        root.iconpath = ImageTk.PhotoImage(file=resource_path('Logo.ico'))
        root.after(100, lambda: root.iconphoto(False, root.iconpath))


        FRAME28 = CTkFrame(master=root, fg_color="transparent")
        FRAME28.pack(fill="both", padx=10, pady=10)
        LABEL29 = CTkLabel(master=FRAME28, text="Component Name (Should be a valid python file name)", anchor="w", padx=10, pady=0,
                           font=CTkFont(weight="bold", size=17))
        LABEL29.pack(fill="x")
        ENTRY30 = CTkEntry(master=FRAME28, placeholder_text="Component Name")
        ENTRY30.pack(pady=(10, 0), fill="x", padx=10)
        BUTTON32 = CTkButton(master=FRAME28, text="Create New Component", fg_color=("#008fff", "#008fff"), hover=False, command=lambda: (self.create_component_code(ENTRY30.get()), root.destroy()))
        BUTTON32.pack(pady=(10, 10), padx=10, side="right")


    def traverse_widgets_till_found(self, widget, widget_list):
        for key, value in widget_list.items():
            if widget == key:
                return value
            else:
                result = self.traverse_widgets_till_found(widget, value)
                if result is not None:
                    return result
        return None


    def loop_generate_component(self, d, p, code, class_name):
        try:
            widget_code = self.template_env.get_template("component.py.j2")

        except Exception as e:
            print(f"Error loading Jinja2 template 'ctk_widget.py.j2': {e}")

            return
        for parent, children in d.items():
            #ic(parent, children, type(parent))
            widget_type = parent.type
            widget_id = parent.get_name()
            parameters = parent.props
            pack_options = parent.pack_options
            ic(parameters)
            if parent.type == "Frame":
                pack_propagate = parent.propagate_on_pack
            else:
                pack_propagate = None
            children = {k: v for k, v in children.items() if
                        k not in ["TYPE", "parameters", "pack_options", "ID", "PACK_PROPAGATE"]}
            widget_class = parent.get_class()
            orientation = parameters.pop('orientation', None)
            prop = '{"properties": properties["properties"]'
            if orientation is not None:
                prop += f', "orientation": "{orientation}"'
            prop += "}"

            rendered_code = widget_code.render(
                widget_id=widget_id,
                widget_class=self.class_map[widget_class],
                parent=p,
                properties=prop,
                pack_options=pack_options,
                pack_propagate=pack_propagate,
                os=os,
                platform=platform,
                theme=self.theme,
                escape_special_chars=self.escape_chars,
                bool_change=self._bool_change,
                widget_type=widget_type,
                format_pack_options=self.format_pack_options,
            )
            code.add_line(rendered_code)

            if "image" in parameters:
                dst = f"./customtkinterbuilder/ComponentAssets/{class_name}"
                src = parameters["image"].cget("dark_image").filename
                parameters["image"] = "ahifhyhmacpopgbbjajsrwjrvfnmzsikrymjfgjakcjyjtdtfxcxqiowpbrheqlhbvgkhckncvdqjxhisnnvzuayoqpdhuiqlolhblocdokaoaroqwfkqbmtfcnoajnqszlgefvvmzhanfeqmtzkrlivydjigeodcezyahakdilbxlkcbyuchwnotsokqbisednbxethehnmepprylstzkakkmpdnwedvjnrzsvwktiyejzrshqklqnhoimdszccokywzuoboruzpcdqkblxdegiljcyyertfvynbgqdzsvjfqvgxtcqozgzuvcbtgbkdcorikwfqkqlsefoqdcxkkagjunbkhvlpulj" # Just a work around
                parameters = str(parameters)
                parameters = parameters.replace("'ahifhyhmacpopgbbjajsrwjrvfnmzsikrymjfgjakcjyjtdtfxcxqiowpbrheqlhbvgkhckncvdqjxhisnnvzuayoqpdhuiqlolhblocdokaoaroqwfkqbmtfcnoajnqszlgefvvmzhanfeqmtzkrlivydjigeodcezyahakdilbxlkcbyuchwnotsokqbisednbxethehnmepprylstzkakkmpdnwedvjnrzsvwktiyejzrshqklqnhoimdszccokywzuoboruzpcdqkblxdegiljcyyertfvynbgqdzsvjfqvgxtcqozgzuvcbtgbkdcorikwfqkqlsefoqdcxkkagjunbkhvlpulj'", f"CTkImage(light_image=Image.open(os.path.join(tempify('temp'), '{os.path.basename(src)}')), dark_image=Image.open(os.path.join(tempify('temp'), '{os.path.basename(src)}')))")
                self.copy_file_to_nested_dir(src, dst)
                #print(parameters["image"], parameters["image"].dark_image)
                code.add_line(f"self.copy('{os.path.join('temp', os.path.basename(src))}')")

            code.add_line(f"self.{widget_id}.save_properties({parameters})")
            if children != {}:
                self.loop_generate_component(children, f"self.{parent.get_name()}", code, class_name)

    def copy_file_to_nested_dir(self, source_file_path, destination_dir_path):
        """
        Creates a nested directory and copies the file into it.

        Parameters:
        - source_file_path (str): The path to the file to copy.
        - destination_dir_path (str): The nested directory path where the file should be copied.

        Returns:
        - str: The full path to the copied file.
        """
        try:
            # Create nested directory if it doesn't exist
            os.makedirs(destination_dir_path, exist_ok=True)

            # Get the filename from the source path
            file_name = os.path.basename(source_file_path)

            # Full path for the destination file
            destination_file_path = os.path.join(destination_dir_path, file_name)

            # Copy the file
            shutil.copy2(source_file_path, destination_file_path)

            return destination_file_path

        except Exception as e:
            print(f"Error copying file: {e}")
            return None

    def change_appearance_mode(self, mode):
        wgts = list(self.id_mapped_widgets.values())

        if mode == 0:
            mode = "light"
        else:
            mode = "dark"

        self.r._set_appearance_mode(mode)
        self.r.winfo_toplevel().main_window_panel._set_appearance_mode(mode)
        self.r.winfo_toplevel().temp._set_appearance_mode(mode)
        self.r.winfo_toplevel().toolbar._set_appearance_mode(mode)
        self.loop_change_appearance(mode, self.widgets[self.r])
        #for widget in wgts:
        #    widget._set_appearance_mode(mode)


    def loop_change_appearance(self, mode, d):
        for x in list(d.keys()):

            if d[x] != {}:
                x._set_appearance_mode(mode)
                self.loop_change_appearance(mode, d[x])
            else:
                x._set_appearance_mode(mode)

    def loop_change_scale(self, scale, d):
        self.scale = scale
        for x in list(d.keys()):
            if d[x] != {}:
                x._set_scaling(scale, scale)

                self.loop_change_scale(scale, d[x])
            else:
                x._set_scaling(scale, scale)

    def change_scale(self, scale):
        wgts = list(self.id_mapped_widgets.values())
        self.loop_change_scale(scale, self.widgets)



    def apply_theme_to_widget(self, widget):
        if self.appearance.get() == 0:
            mode = "light"
        else:
            mode = "dark"

        widget._set_appearance_mode(mode)
        widget._set_scaling(self.scale, self.scale)
        if widget.get_class() == "CTkScrollableFrame":
            x = self.theme["CTkFrame"]

        else:
            x = self.theme[widget.get_class()]

        d = {}

        for key in list(x.keys()):
            if key == "top_fg_color":
                if widget.get_class() == "CTkFrame" or widget.get_class() == "CTkScrollableFrame":
                    try:
                        if widget.master.cget("fg_color") == x["fg_color"]:
                            d["fg_color"] = x["top_fg_color"]
                        else:
                            d["fg_color"] = x["fg_color"]
                    except tkinter.TclError as e:
                        # Parent widget is a Scrollable Frame
                        if widget.master.master.master.master._fg_color == x["fg_color"]:
                            d["fg_color"] = x["top_fg_color"]
                        else:
                            d["fg_color"] = x["fg_color"]
            else:
                d[key] = x[key]

        if widget.__class__ not in [Frame, ProgressBar, Scrollbar, Slider, Main, ScrollableFrame]:
            if widget.type not in ["FRAME", "PROGRESSBAR", "SCROLLBAR", "SLIDER", "MAIN", "SCROLLABLEFRAME"]:
                ic(widget.type)
                for y in list(self.theme["CTkFont"].keys()):
                    if sys.platform == "darwin":
                        d["font"] = CTkFont(family=self.theme["CTkFont"]["macOS"]["family"], size=self.theme["CTkFont"]["macOS"]["size"],
                                          weight=self.theme["CTkFont"]["macOS"]["weight"])
                    elif sys.platform.startswith("win"):
                        d["font"] = CTkFont(family=self.theme["CTkFont"]["Windows"]["family"], size=self.theme["CTkFont"]["Windows"]["size"],
                                          weight=self.theme["CTkFont"]["Windows"]["weight"])
                    else:
                        d["font"] = CTkFont(family=self.theme["CTkFont"]["Linux"]["family"], size=self.theme["CTkFont"]["Linux"]["size"],
                                          weight=self.theme["CTkFont"]["Linux"]["weight"])
        widget.configure(**d)

        if widget.get_class() == "CTkScrollableFrame":
            ic(self.theme["CTkScrollbar"]["fg_color"])
            widget.configure(scrollbar_fg_color=self.theme["CTkScrollbar"]["fg_color"])

        if widget.__class__ in [ComboBox, OptionMenu]:
            widget.set_nonvisible_disable()

    def change(self, **kwargs):
        for key in list(kwargs.keys()):
            if key == "title":
                self.title = kwargs[key]

    def clear_toplevels(self):
        for x in self.windows_open:
            x.destroy()

    def run_code(self):
        self.clear_toplevels()


        code = CodeGenerator(indentation="\t")
        code.add_line(f"""
root = CTkToplevel()
root.title("{self.escape_special_chars(self.title)}")
root.geometry("{self.r.cget('width')}x{self.r.cget('height')}")
root.protocol("WM_DELETE_WINDOW", lambda root=root: (set_default_color_theme("{resource_path(os.path.join('Themes', 'ctktheme.json'))}"), root.destroy()))
root.configure(fg_color="{self.r.cget("fg_color")[self.appearance.get()]}")
set_default_color_theme(theme_manager.get("{self.theme_manager.name}"))
root.after(20, root.lift)
self.windows_open.append(root)
""")


        self.loop_generate(d=self.widgets[self.r], parent="root", code=code, run=True)
        #print(code.get_code())
        # I know this is not that safe. Do create an issue if there are any safer ways to do this
        exec(code.get_code())

    def export(self, code):
        filename = asksaveasfilename(filetypes=[(".py", "py")])
        if filename != "":
            with open(filename, "w", encoding="utf-8") as f:
                f.write(code)


    def export_code(self):
        code = CodeGenerator(indentation="    ")
        code.add_line(f"""
from customtkinter import *
from PIL import Image
from customtkinterthemes import theme_manager

set_default_color_theme(theme_manager.get("{self.theme_manager.name}"))

root = CTk()
root.title("{self.escape_special_chars(self.title)}")
root.geometry("{self.r.cget('width')}x{self.r.cget('height')}")
root.configure(fg_color={self.r.cget("fg_color")})
""")
        self.loop_generate(d=self.widgets[self.r], parent="root", code=code)
        code.add_line("root.mainloop()")

        oop_code = CodeGenerator(indentation="    ")
        oop_code.add_line("""
from customtkinter import *
from PIL import Image
from customtkinterthemes import theme_manager

class App(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
""")
        oop_code.indent()
        oop_code.indent()
        self.loop_generate_oop(d=self.widgets[self.r], p="self", code=oop_code)
        oop_code.add_line(f"""
set_default_color_theme(theme_manager.get("{self.theme_manager.name}"))
root = App()
root.geometry("{self.r.cget("width")}x{self.r.cget("height")}")
root.title("{self.escape_special_chars(self.title)}")
root.configure(fg_color={self.r.cget("fg_color")})
root.mainloop()
            """)
        self.clear_toplevels()
        top = CTkToplevel()
        top.geometry("1000x800+500+100")
        top.title("Export Code")
        top.configure(fg_color=["gray95", "gray10"])
        top.after(20, top.lift)
        top.after(25, top.focus_get)
        self.windows_open.append(top)
        top.wm_iconbitmap()
        top.iconpath = ImageTk.PhotoImage(file=resource_path('Logo.ico'))
        top.after(100, lambda: top.iconphoto(False, top.iconpath))


        self.codeviewer = CTkCodeViewer.CTkCodeViewer(top, code=oop_code.get_code(), language="python", theme="monokai", font=CTkFont(size=15))
        self.codeviewer.configure(wrap="none")
        self.codeviewer.pack(expand=True, fill="both", padx=20, pady=20)

        self.oop_code_switch = CTkSwitch(top, text="OOP Code", command=self.change_oop)
        self.oop_code_switch.pack(side="left", padx=20, pady=(0, 20))
        self.oop_code_switch.select()

        self.pep8_switch = CTkSwitch(top, text="PEP8 Refactor", command=self.use_pep8)
        self.pep8_switch.pack(side="left", padx=20, pady=(0, 20))
        self.pep8_switch.select()

        self.current = oop_code

        exp_btn = CTkButton(top, text="Export Code", command=lambda: self.export(self.codeviewer.get(1.0, "end")))
        exp_btn.pack(side="right", padx=(20, 20), pady=(0, 20))

        copy_btn = CTkButton(top, text="Copy Code", command=lambda: pyperclip.copy(self.codeviewer.get(1.0, "end")))
        copy_btn.pack(side="right", padx=(20, 0), pady=(0, 20))

        export_with_assets = CTkButton(top, text="Export code with Assets", command=self.export_with_assets)
        export_with_assets.pack(side="right", padx=(20, 0), pady=(0, 20))


        self.oop_code = oop_code
        self.non_oop_code = code

    def export_with_assets(self):
        res = messagebox.askyesno("Note", "This saves the project before exporting. Do you want to continue?")
        if res:
            self.save_file(suppress_dialog=True)


            filename = asksaveasfilename(filetypes=[(".py", "py")])
            source_dir = os.path.join(self.file[0], self.file[1], "Assets")
            dest_dir = os.path.join(os.path.dirname(filename), "Assets")
            ic(filename, source_dir, dest_dir)
            if filename != "":
                self.copy_files(source_dir, dest_dir)
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(self.codeviewer.get(1.0, "end"))

    def copy_files(self, source_dir, dest_dir):
        # Ensure source directory exists
        if not os.path.isdir(source_dir):
            raise ValueError(f"Source directory does not exist: {source_dir}")

        # Create destination directory if it doesn't exist
        os.makedirs(dest_dir, exist_ok=True)

        for filename in os.listdir(source_dir):
            source_file = os.path.join(source_dir, filename)
            dest_file = os.path.join(dest_dir, filename)

            # Only copy files (not directories) and skip if file already exists
            if os.path.isfile(source_file) and not os.path.exists(dest_file):
                shutil.copy2(source_file, dest_file)
                ic(f"Copied: {filename}")
            elif os.path.exists(dest_file):
                ic(f"Skipped (already exists): {filename}")

    def change_oop(self):
        if self.oop_code_switch.get() == 0:
            self.current = self.non_oop_code

        else:
            self.current = self.oop_code
        self.codeviewer.delete(1.0, "end")
        self.codeviewer._add_code(self.current.get_code(), "python")

    def use_pep8(self):
        if self.pep8_switch.get() == 0:
            self.codeviewer.delete(1.0, "end")
            self.codeviewer._add_code(self.current.get_code(), "python")

        else:
            self.codeviewer.delete(1.0, "end")
            self.codeviewer._add_code(autopep8.fix_code(self.current.get_code()), "python")



    def escape_special_chars(self, text):
        escape_table = {
            "\n": "\\n",
            "\t": "\\t",
            "\"": "\\\"",
            "'": "\\'"
        }
        formatted_text = text
        for char, escape_seq in escape_table.items():
            formatted_text = formatted_text.replace(char, escape_seq)
        return formatted_text

    def loop_generate(self, d, parent, code, run=False):
        for x in list(d.keys()):
            if x.props == {}:
                code.add_line(f"{x.get_name()} = {x.get_class()}(master={parent})")
                if x.type == "FRAME" and not x._bool_change(x.propagate_on_pack):
                    code.add_line(f"{x.get_name()}.pack_propagate({x._bool_change(x.propagate_on_pack)})")
            else:
                p = ""
                font = "font=CTkFont("
                f2 = "hover_font=CTkFont("
                for key in list(x.props.keys()):
                    if key == "image" and x.props["image"] != None:
                        if not run:
                            ic("Assets", os.path.basename(x.props["image"].cget("dark_image").filename))
                            ic(joinpath("Assets", os.path.basename(x.props["image"].cget("dark_image").filename)))
                            p += f'image=CTkImage(Image.open(r"{joinpath("Assets", os.path.basename(x.props["image"].cget("dark_image").filename))}"), size=({x.props["image"].cget("size")[0]}, {x.props["image"].cget("size")[1]})), '
                        else:
                            val = x.props["image"].cget("dark_image").filename

                            ic(val)
                            ic(fr'image=CTkImage(Image.open(r"{val}"), size=({x.props["image"].cget("size")[0]}, {x.props["image"].cget("size")[1]})), ')
                            p += fr'image=CTkImage(Image.open(r"{val}"), size=({x.props["image"].cget("size")[0]}, {x.props["image"].cget("size")[1]})), '
                    elif key == "hover_image":
                        if not run:
                            p += f'hover_image=CTkImage(Image.open("{joinpath("Assets", os.path.basename(x.props["hover_image"].cget("dark_image").filename))}"), size=({x.props["hover_image"].cget("size")[0]}, {x.props["hover_image"].cget("size")[1]})), '
                        else:
                            p += f'hover_image=CTkImage(Image.open("{x.props["hover_image"].cget("dark_image").filename}"), size=({x.props["hover_image"].cget("size")[0]}, {x.props["hover_image"].cget("size")[1]})), '
                    elif key in ["font_family", "font_size", "font_weight", "font_slant", "font_underline",
                               "font_overstrike"]:
                        if key == "font_family":
                            current_os = platform.system()
                            if current_os == "Darwin":
                                current_os = "macOS"
                            elif current_os == "Windows":
                                current_os = "Windows"
                            elif current_os == "Linux":
                                current_os = "Linux"
                            if x.props[key] == self.theme["CTkFont"][current_os]["family"]:
                                pass
                            else:
                                if type(x.props[key]) == str:

                                    font += f'{key[5::]}="{x.props[key]}", '
                                else:
                                    font += f'{key[5::]}={x.props[key]}, '
                        else:
                            if type(x.props[key]) == str:

                                font += f'{key[5::]}="{x.props[key]}", '
                            else:
                                font += f'{key[5::]}={x.props[key]}, '
                    elif key in ["hover_font_family", "hover_font_size", "hover_font_weight", "hover_font_slant", "hover_font_underline",
                               "hover_font_overstrike"]:
                        ic(key, x.props[key])
                        if type(x.props[key]) == str:

                            f2 += f'{key[11::]}="{x.props[key]}", '
                        else:
                            f2 += f'{key[11::]}={x.props[key]}, '
                    else:
                        if type(x.props[key]) == str:
                            k = self.escape_special_chars(x.props[key])
                            p += f'{key}="{k}", '
                        elif type(x.props[key]) == tuple or type(x.props[key]) == list and len(x.props[key]) == 2:
                            if type(x.props[key][0]) == str and type(x.props[key][1]) == str:
                                p += f'{key}=("{x.props[key][0]}", "{x.props[key][1]}"), '
                            else:
                                p += f"{key}=({x.props[key][0]}, {x.props[key][1]}), "
                        else:
                            p += f"{key}={x.props[key]}, "

                font = font[0:-2] # Delete ', ' at last part
                f2 = f2[0:-2]
                f2 += ")"
                font += ")"

                if font != "font=CTkFon)": # Which means there is no change in font
                    p += font
                    p += ", "
                if f2 != "hover_font=CTkFon)": # Which means there is no change in font
                    p += f2
                    p += ", "


                p = p[0:-2]
                code.add_line(f"{x.get_name()} = {x.get_class()}(master={parent}, {p})")
                if x.type == "FRAME" and not x._bool_change(x.propagate_on_pack):
                    code.add_line(f"{x.get_name()}.pack_propagate({x._bool_change(x.propagate_on_pack)})")

                    #code.add_line(f"{x.get_name()}.pack_propagate(False)")
            if x.pack_options == {}:
                code.add_line(f"{x.get_name()}.pack()")

                if run:
                    if x.get_class() != "CTkSegmentedButton":
                        code.add_line(f"{x.get_name()}._set_appearance_mode('{'light' if self.appearance.get() == 0 else 'dark'}')")
                        if x.get_class() == "CTkScrollableFrame":
                            code.add_line(f"{x.get_name()}._parent_frame._set_appearance_mode('{'light' if self.appearance.get() == 0 else 'dark'}')")
                            code.add_line(f"{x.get_name()}._scrollbar._set_appearance_mode('{'light' if self.appearance.get() == 0 else 'dark'}')")
                            #code.add_line(f"{x.get_name()}._parent_frame.configure(fg_color={x.get_name()}.cget('fg_color')[{self.appearance.get()}], border_color={x.get_name()}.cget('fg_color')[{self.appearance.get()}])")
                    else:
                        code.add_line(f"""
for x in {x.get_name()}._buttons_dict.values():
    x._set_appearance_mode('{'light' if self.appearance.get() == 0 else 'dark'}')

""")


            else:
                p = ""
                default_pack_options = {"expand": False, "anchor": "center", "fill": "none", "padx": 0, "pady": 0, "side": "top", "ipadx": 0, "ipady": 0}
                modified_pack_options = x.pack_options
                for i in list(modified_pack_options.keys()):
                    if modified_pack_options[i] == default_pack_options[i]:
                        modified_pack_options.pop(i)

                for key in list(modified_pack_options.keys()):

                    if type(modified_pack_options[key]) == str:
                        p += f'{key}="{modified_pack_options[key]}", '
                    elif type(modified_pack_options[key]) == tuple or type(modified_pack_options[key]) == list:
                        """if type(x.pack_options[key][0]) == str and type(x.pack_options[key][1]) == str:
                            p += f'{key}=("{x.pack_options[key][0]}", "{x.pack_options[key][1]}"), '
                        else:"""
                        p += f"{key}=({int(modified_pack_options[key][0])}, {int(modified_pack_options[key][1])}), "
                    else:
                        p += f"{key}={modified_pack_options[key]}, "

                p = p[0:-2]  # Delete ', ' at last part
                code.add_line(f"{x.get_name()}.pack({p})")
                if run:
                    code.add_line(f"{x.get_name()}._set_appearance_mode('{'light' if self.appearance.get() == 0 else 'dark'}')")
                    if x.get_class() == "CTkScrollableFrame":
                        code.add_line(f"{x.get_name()}._parent_frame._set_appearance_mode('{'light' if self.appearance.get() == 0 else 'dark'}')")
                        code.add_line(f"{x.get_name()}._scrollbar._set_appearance_mode('{'light' if self.appearance.get() == 0 else 'dark'}')")

            if d[x] != {}:
                #btn = CTkButton(self, text=x.type, command=lambda x=x: x.on_drag_start(None))

                self.loop_generate(d=d[x], parent=x.get_name(), code=code, run=run)

    def open_file_without_asking(self):
        file = os.path.join(self.file[0], self.file[1])
        print(self.file, file)
        shutil.rmtree(tempify('temp'))
        shutil.copytree(os.path.join(file, "Assets"), tempify("temp"))

        with open(os.path.join(file, f"{os.path.basename(file)}.json"), 'r') as openfile:
            d = json.load(openfile)
        d = d["MAIN-1"]

        self.r.props = d["parameters"]
        self.r._inner_id = d["ID"]
        for key in list(d["parameters"].keys()):
            if key == "width":
                self.r.configure(width=d["parameters"]["width"])
            elif key == "height":
                self.r.configure(height=d["parameters"]["height"])
            elif key == "fg_color":
                self.r.configure(fg_color=d["parameters"]["fg_color"])
            elif key == "title":
                self.title = d["parameters"]["title"]
        d.pop("TYPE")
        d.pop("parameters")
        d.pop("pack_options")
        d.pop("ID")

        self.theme_manager = ThemeUtl(theme_dir=f"Themes", theme_name=d["theme"])
        self.theme = self.theme_manager.get_theme_by_name()
        self.properties.color_manager.colors = d["palette"]
        self.properties.color_manager.on_change_list = d["palette_on_change"]
        d.pop("theme")
        d.pop("palette")
        d.pop("palette_on_change")
        self.current_widget_count = IntVar(value=0)
        self.current_widget_count.trace("w", self.changed_value)
        self.widgetnumber = IntVar(value=1)
        self.get_number_of_widgets(json.loads(json.dumps(d)))

        t1 = self.launch_thread_with_message(target=self.loop_open, args=(d, self.r))

        #self.loop_open(d, self.r)
    def changed_value(self, a, b, c):
        try:
            if (self.widgetnumber.get()-1) == self.current_widget_count.get():
                self.edit_lbl.configure(text="Updating Hierarchy....")
            self.lbl2.configure(text=f"{self.current_widget_count.get()}/{self.widgetnumber.get()}")
            self.progressbar.step()
        except Exception:
            pass
    def center(self, toplevel):
        toplevel.update_idletasks()

        # Tkinter way to find the screen resolution
        screen_width = toplevel.winfo_screenwidth()
        screen_height = toplevel.winfo_screenheight()

        # PyQt way to find the screen resolution
        # app = QtGui.QApplication([])
        # screen_width = app.desktop().screenGeometry().width()
        # screen_height = app.desktop().screenGeometry().height()

        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = screen_width / 2 - size[0] / 2
        y = screen_height / 2 - size[1] / 2

        toplevel.geometry("+%d+%d" % (x, y))

    def show_loading(self):
        m = self.r.winfo_toplevel()
        self.loading_frame = CTkFrame(m)
        self.loading_frame.place(x=0, y=0, relwidth=1, relheight=1)
        frm = CTkFrame(self.loading_frame, fg_color="transparent", width=700, height=50)
        frm.pack_propagate(False)
        txt_frame = CTkFrame(frm, fg_color="transparent")
        txt_frame.pack(pady=1, fill="x", expand=True, padx=100)
        self.edit_lbl = CTkLabel(txt_frame, text="Creating Editable Widgets....", font=CTkFont(size=15))
        self.edit_lbl.pack(side="left")
        self.lbl2 = CTkLabel(txt_frame, text=f"0/{self.widgetnumber.get()}", font=CTkFont(size=15))
        self.lbl2.pack(side="right")
        stepval = ((1/self.widgetnumber.get())*50) # Looking at source code I found that the step val is from 1 --> 50. Not mentioned in the documentation.
        self.progressbar = CTkProgressBar(frm, height=15, orientation="horizontal", mode="determinate", determinate_speed=stepval)
        self.progressbar.set(0)
        self.progressbar.pack(fill="x", padx=100)
        #self.progressbar.start()
        frm.pack(expand=True)

    def destroy_loading(self):
        try:
            self.loading_frame.destroy()
        except Exception as e:
            pass

    def launch_thread_with_message(self, target, args=(), kwargs={}):
        def target_with_msg(*args, **kwargs):
            target(*args, **kwargs)
            #self.hierarchy.delete_children()
            self.hierarchy.update_list(self.widgets, 5)
            self.destroy_loading()

        """
        loading_window = CTkToplevel()
        loading_window.geometry(f"500x100")
        loading_window.title("Loading....")
        loading_window.overrideredirect(1)
        loading_window.overrideredirect(0)
        if sys.platform.startswith("win"):
            loading_window.overrideredirect(True)
        loading_window.after(20, loading_window.lift)
        loading_window.after(25, loading_window.focus_get)
        """
        self.show_loading()
        thread = threading.Thread(target=target_with_msg, args=args, kwargs=kwargs)
        thread.start()
        return thread


    def open_file(self):
        file = askdirectory()
        if file != "":
            self.file = [os.path.dirname(file), os.path.basename(file)]

            shutil.rmtree(tempify('temp'))
            shutil.copytree(os.path.join(file, "Assets"), tempify("temp"))

            with open(os.path.join(file, f"{os.path.basename(file)}.json"), 'r') as openfile:
                d = json.load(openfile)
            d = d["MAIN-1"]

            self.r.props = d["parameters"]
            self.r._inner_id = d["ID"]
            for key in list(d["parameters"].keys()):
                if key == "width":
                    self.r.configure(width=d["parameters"]["width"])
                elif key == "height":
                    self.r.configure(height=d["parameters"]["height"])
                elif key == "fg_color":
                    self.r.configure(fg_color=d["parameters"]["fg_color"])
                elif key == "title":
                    self.title = d["parameters"]["title"]
            d.pop("TYPE")
            d.pop("parameters")
            d.pop("pack_options")
            d.pop("ID")

            self.theme_manager = ThemeUtl(theme_dir=f"Themes", theme_name=d["theme"])
            self.theme = self.theme_manager.get_theme_by_name()
            self.properties.color_manager.colors = d["palette"]
            self.properties.color_manager.on_change_list = d["palette_on_change"]
            d.pop("theme")
            d.pop("palette")
            d.pop("palette_on_change")
            self.current_widget_count = IntVar(value=0)
            self.current_widget_count.trace("w", self.changed_value)
            self.widgetnumber = IntVar(value=1)
            self.get_number_of_widgets(json.loads(json.dumps(d)))

            t2 = self.launch_thread_with_message(target=self.loop_open, args=(d, self.r))

            #self.loop_open(d, self.r)

    def loop_open(self, d, parent, copy=False):
        for x in list(d.keys()):
            y = d[x]["TYPE"]
            if y == "FRAME":
                w = Frame
            elif y == "BUTTON":
                w = Button
            elif y == "LABEL":
                w = Label
            elif y == "SWITCH":
                w = Switch
            elif y == "SCROLLABLEFRAME":
                w = ScrollableFrame
            elif y == "ENTRY":
                w = Entry
            elif y == "MAIN":
                w = Main
            elif y == "TEXTBOX":
                w = TextBox
            elif y == "PROGRESSBAR":
                w = ProgressBar
            elif y == "SEGMENTEDBUTTON":
                w = SegmentedButton
            elif y == "SLIDER":
                w = Slider
            elif y == "OPTIONMENU":
                w = OptionMenu
            elif y == "CHECKBOX":
                w = CheckBox
            elif y == "RADIOBUTTON":
                w = RadioButton
            elif y == "SCROLLBAR":
                w = Scrollbar
            elif y == "COMBOBOX":
                w = ComboBox

            else:
                raise ModuleNotFoundError(f"The Widget is not available. Perhaps the file is edited. The unknown widget was {x}")
            f = CTkFont()

            i = None
            family = False
            d_copy = dict(d[x]["parameters"])
            img_path = None
            img_size = None
            for p in dict(d[x]["parameters"]):
                if p == "image":
                    path = d[x]["parameters"]["image"]["image"]
                    #file_name = os.path.basename(path)
                    file_name = path
                    img = tempify(os.path.join("temp", file_name))
                    img_path = img
                    img_size = d[x]["parameters"]["image"]["size"]
                    #print(img)
                    #i = CTkImage(light_image=Image.open(img), dark_image=Image.open(img), size=(d[x]["parameters"]["image"]["size"][0], d[x]["parameters"]["image"]["size"][1]))
                    #d[x]["parameters"]["image"] = img
                    d[x]["parameters"].pop("image")

                elif p == "font_family":
                    ##print(d[x], p)
                    f.configure(family=d[x]["parameters"][p])
                    family = True
                    d[x]["parameters"].pop("font_family")
                    if w != ScrollableFrame:
                        d[x]["parameters"]["font"] = f
                    else:
                        d[x]["parameters"]["label_font"] = f
                elif p == "font_size":
                    f.configure(size=d[x]["parameters"][p])
                    d[x]["parameters"].pop("font_size")
                    if w != ScrollableFrame:
                        d[x]["parameters"]["font"] = f
                    else:
                        d[x]["parameters"]["label_font"] = f
                elif p == "font_weight":
                    f.configure(weight=d[x]["parameters"][p])
                    d[x]["parameters"].pop("font_weight")
                    if w != ScrollableFrame:
                        d[x]["parameters"]["font"] = f
                    else:
                        d[x]["parameters"]["label_font"] = f
                elif p == "font_slant":
                    f.configure(slant=d[x]["parameters"][p])
                    d[x]["parameters"].pop("font_slant")
                    if w != ScrollableFrame:
                        d[x]["parameters"]["font"] = f
                    else:
                        d[x]["parameters"]["label_font"] = f
                elif p == "font_underline":
                    f.configure(underline=d[x]["parameters"][p])
                    d[x]["parameters"].pop("font_underline")
                    if w != ScrollableFrame:
                        d[x]["parameters"]["font"] = f
                    else:
                        d[x]["parameters"]["label_font"] = f
                elif p == "font_overstrike":
                    f.configure(overstrike=d[x]["parameters"][p])
                    d[x]["parameters"].pop("font_overstrike")
                    if w != ScrollableFrame:
                        d[x]["parameters"]["font"] = f
                    else:
                        d[x]["parameters"]["label_font"] = f


            ##print(w, parent.get_name(), d[x]["parameters"])
            if d[x]["parameters"] != {}:
                if "orientation" in list(d[x]["parameters"].keys()):

                    if parent.get_class() == "CTkScrollableFrame":
                        new_widget = w(master=parent.scrollwindow, orientation=d[x]["parameters"]["orientation"],
                                       properties=self.r.properties)
                    else:
                        new_widget = w(master=parent, orientation=d[x]["parameters"]["orientation"], properties=self.r.properties)
                    g = dict(d)
                    g[x]["parameters"].pop("orientation")

                    self.apply_theme_to_widget(new_widget)

                    new_widget.configure(**g[x]["parameters"])
                else:
                    if parent.get_class() == "CTkScrollableFrame":
                        new_widget = w(master=parent.scrollwindow, properties=self.r.properties)
                    else:
                        new_widget = w(master=parent, properties=self.r.properties)

                    self.apply_theme_to_widget(new_widget)

                    new_widget.configure(**d[x]["parameters"])

                try:
                    ##print(d_copy)
                    #img = tempify(os.path.join("temp", file_name))
                    #print(d_copy['image']['image'])
                    #new_widget.image = os.path.join("temp", d_copy["image"]["image"])
                    #img = d[x]["parameters"]["image"]
                    #print(img)
                    #new_widget.img = d[x]["parameters"]["image"]
                    #new_widget.size = (d[x]["parameters"]["image"].cget("size")[0], d[x]["parameters"]["image"].cget("size")[1])
                    #print(new_widget.img, new_widget.size)
                    if img_path != None and img_size != None:
                        new_widget.set_image(img_path, img_size)
                        d_copy["image"] = new_widget.img

                    ##print(d_copy)

                except KeyError as e:
                    pass

                new_widget.props = d_copy

            else:

                if parent.get_class() == "CTkScrollableFrame":
                    new_widget = w(master=parent.scrollwindow, properties=self.r.properties)
                else:
                    new_widget = w(master=parent, properties=self.r.properties)

                self.apply_theme_to_widget(new_widget)

            new_widget.num = self.total_num

            if not copy:
                new_widget.name = x
            else:

                new_widget.name = new_widget.type + str(new_widget.num + 1) + "_copy"
            self.total_num += 1
            self._parents = []

            self.get_parents(new_widget)
            #ic(self.widgets, self._parents, new_widget)
            if family:
                new_widget.family = new_widget.cget("font").cget("family")

            self.add_to_dict(self.widgets, self._parents, new_widget)

            self._parents = []


            new_widget.pack(**d[x]["pack_options"])
            new_widget.pack_options = d[x]["pack_options"]
            #new_widget.configure(bg_color=parent.cget("fg_color"))

            if new_widget.__class__ == SegmentedButton:
                new_widget.configure(command=lambda e, nw=new_widget: (nw.on_drag_start(None), self.hierarchy.set_current_selection(nw)))
            elif new_widget.__class__ == ScrollableFrame:
                new_widget.scrollwindow.bind("<Button-1>", lambda e, nw=new_widget: (nw.on_drag_start(None), self.hierarchy.set_current_selection(nw)))
                new_widget.canv.bind("<Button-1>", lambda e, nw=new_widget: (nw.on_drag_start(None), self.hierarchy.set_current_selection(nw)))
            else:
                new_widget.bind("<Button-1>", lambda e, nw=new_widget: (nw.on_drag_start(None), self.hierarchy.set_current_selection(nw)))

            if new_widget.__class__ in [ComboBox, OptionMenu]:
                try:
                    new_widget.set(d_copy["values"][0])
                except KeyError as e:
                    print(e)

            # new_widget.bind("<Button-1>", new_widget.on_drag_start)
            # new_widget.on_drag_start(None)

            if not copy:
                new_widget._inner_id = d[x]["ID"]
                self.id_mapped_widgets[new_widget._inner_id] = new_widget
            else:
                new_widget._inner_id = str(uuid.uuid4())
                self.id_mapped_widgets[new_widget._inner_id] = new_widget
                arr = self.properties.color_manager.get_all_changes(d[x]["ID"])
                for i in arr:
                    ar = self.properties.color_manager.on_change_list[i[0]]
                    ar.append([new_widget._inner_id, i[1][1], i[1][2]])
                    self.properties.color_manager.on_change_list[i[0]] = ar
            if new_widget.__class__ == Frame:
                new_widget.change_pack_propagate(d[x]["PACK_PROPAGATE"])
                d[x].pop("PACK_PROPAGATE")

            #ic(new_widget._inner_id, new_widget.cget("fg_color"), d, x)
            #self.hierarchy.delete_children()
            #self.hierarchy.update_list(self.widgets, 5)
            # new_widget.place(x=x, y=y)
            if new_widget.__class__ != SegmentedButton:
                self.drag_manager.update_children(children=parent.winfo_children())

            d[x].pop("TYPE")
            d[x].pop("pack_options")
            d[x].pop("parameters")
            d[x].pop("ID")

            self.current_widget_count.set(self.current_widget_count.get()+1)
            if d[x] != {}:
                #ic(d[x], new_widget, copy)
                #t2 = threading.Thread(target=self.loop_open, args=(d[x], new_widget), kwargs={"copy": copy})
                #t2.start()
                self.loop_open(d[x], new_widget, copy=copy)

    def get_number_of_widgets(self, d):
        # I could destroy every child in self.r but could not add new widgets after destroying the children.

        for x in list(d.keys()):

            y = d[x]["TYPE"]
            if y == "FRAME":
                d[x].pop("PACK_PROPAGATE")
            d[x].pop("TYPE")
            d[x].pop("pack_options")
            d[x].pop("parameters")
            d[x].pop("ID")
            self.widgetnumber.set(self.widgetnumber.get()+1)
            if d[x] != {}:
                self.get_number_of_widgets(d[x])

    def save(self, dir_, name):
        try:
            os.mkdir(path=os.path.join(dir_, name))
            os.mkdir(path=os.path.join(os.path.join(dir_, name), "Assets"))
            #shutil.copytree("temp", os.path.join(os.path.join(dir_, name), "Assets"))

            self.s = {self.r.get_name(): {}}
            self.loop_save(self.widgets, self.r.get_name(), self.s)
            self.s = self.s[self.r.get_name()]
            ##print(self.s)
            self.s[self.r.get_name()]["theme"] = self.theme_manager.name
            self.s[self.r.get_name()]["palette_on_change"] = self.properties.color_manager.on_change_list
            self.s[self.r.get_name()]["palette"] = self.properties.color_manager.colors
            self.file = [dir_, name]
            json_object = json.dumps(self.s, indent=4)
            with open(os.path.join(os.path.join(dir_, name), f"{name}.json"), "w") as outfile:
                outfile.write(json_object)
            with open(os.path.join(dir_, name, name + ".json"), "w") as f:
                f.write(json_object)
            # I have a doubt whether json is being written twice

            self.r.winfo_toplevel().title(f"Custom Tkinter Builder - {os.path.join(dir_, name)}")

            with open(resource_path("config.json"), 'r') as openfile:
                configure = json.load(openfile)

            self.project_files = configure["project_files"]
            self.project_files.append({"Name": name, "Directory": dir_})
            configure["project_files"] = self.project_files
            json_object = json.dumps(configure, indent=4)
            with open(resource_path("config.json"), 'w') as f:
                f.write(json_object)
            short_name = name[0:2].upper()
            self.r.winfo_toplevel().master.show_project(short_name, name, dir_)
            messagebox.showinfo("Saved", "Your file has been successfully saved")

        except FileExistsError as e:
            self.file = ""
            tkinter.messagebox.showerror("Error", f"File Exists: {os.path.join(dir_, name)}")
        #os.mkdir(path=os.path.join(os.path.join(dir_, name), "Assets"))
    def set_file(self, dir_, name):
        self.file = [dir_, name]
        self.save(dir_, name)

    def save_file(self, suppress_dialog=False):

        if self.file == "":
            f = SaveFileDialog(callback=self.set_file)

        if self.file != "":
            shutil.rmtree(os.path.join(os.path.join(self.file[0], self.file[1]), "Assets"))
            #shutil.copytree("temp", os.path.join(os.path.join(self.file[0], self.file[1]), "Assets"))
            os.mkdir(path=os.path.join(os.path.join(self.file[0], self.file[1]), "Assets"))
            self.s = {self.r.get_name(): {}}
            self.loop_save(self.widgets, self.r.get_name(), self.s)
            self.s = self.s[self.r.get_name()]
            self.s[self.r.get_name()]["theme"] = self.theme_manager.name
            self.s[self.r.get_name()]["palette_on_change"] = self.properties.color_manager.on_change_list
            self.s[self.r.get_name()]["palette"] = self.properties.color_manager.colors
            json_object = json.dumps(self.s, indent=4)
            with open(os.path.join(os.path.join(self.file[0], self.file[1]), f"{self.file[1]}.json"), "w") as outfile:
                outfile.write(json_object)
            if not suppress_dialog:
                self.message_box.show("File Saved")
                #messagebox.showinfo("Saved", "Your file has been successfully saved")


    def saveas_file(self):
        f = SaveFileDialog(callback=self.save)

    def loop_save(self, d, parent, code):
        ##print(d)
        for x in list(d.keys()):
            props = dict(x.props)
            if "image" in list(props.keys()):
                ##print(x.get_name(), x.props)
                img = os.path.basename(x.props["image"].cget("dark_image").filename)
                path = os.path.join("Assets", img)
                #ic(x.props["image"].cget("dark_image").filename, self.file)
                shutil.copy2(x.props["image"].cget("dark_image").filename, os.path.join(self.file[0], self.file[1],
                                                                                        "Assets"))
                props["image"] = {"image": img, "size": [x.size[0], x.size[1]]}
            if "font_family" in list(props.keys()):
                current_os = platform.system()
                if current_os == "Darwin":
                    current_os = "macOS"
                elif current_os == "Windows":
                    current_os = "Windows"
                elif current_os == "Linux":
                    current_os = "Linux"
                if props["font_family"] == self.theme["CTkFont"][current_os]["family"]:
                    props.pop("font_family")

            if x.get_class() == "CTkFrame":
                code[parent][x.get_name()] = {"TYPE": x.type, "parameters": props, "pack_options": x.pack_options, "ID": x._inner_id, "PACK_PROPAGATE": x.propagate_on_pack}
            else:
                code[parent][x.get_name()] = {"TYPE": x.type, "parameters": props, "pack_options": x.pack_options, "ID": x._inner_id}

            if d[x] != {}:
                self.loop_save(d[x], x.get_name(), code[parent])

        ##print(code)

    def escape_chars(self, text):
        if isinstance(text, str):
            return self.escape_special_chars(text)
        return text

    def _bool_change(self, value):
        return value.lower() == 'true'

    def get_class_name(self, type_str):
        return f"CTk{type_str.capitalize()}"

    def format_pack_options(self, pack_options):
        options = {}
        default_pack_options = {"expand": False, "anchor": "center", "fill": "none", "padx": 0, "pady": 0,
                                "side": "top", "ipadx": 0, "ipady": 0}
        for key, value in pack_options.items():
            if value != default_pack_options[key]:
                if isinstance(value, str):
                    options[key] = f'"{value}"'
                elif isinstance(value, (tuple, list)):
                    options[key] = f'({value[0]}, {value[1]})'
                else:
                    options[key] = repr(value)
            ic(key, value)

        return ", ".join(f"{k}={v}" for k, v in options.items())


    def loop_generate_oop(self, d, p, code):
        try:
            widget_code = self.template_env.get_template("ctk_widget.py.j2")
            widget_pack_propagate_code = self.template_env.get_template("ctk_widget_pack_propagate.py.j2")
            widget_pack_code = self.template_env.get_template("ctk_widget_pack.py.j2")

        except Exception as e:
            print(f"Error loading Jinja2 template 'ctk_widget.py.j2': {e}")

            return
        for parent, children in d.items():
            #ic(parent, children, type(parent))
            widget_type = parent.type
            widget_id = parent.get_name()
            parameters = parent.props
            pack_options = parent.pack_options
            ic(parameters)
            if parent.type == "Frame":
                pack_propagate = parent.propagate_on_pack
            else:
                pack_propagate = None
            children = {k: v for k, v in children.items() if
                        k not in ["TYPE", "parameters", "pack_options", "ID", "PACK_PROPAGATE"]}
            widget_class = parent.get_class()

            rendered_code = widget_code.render(
                widget_id=widget_id,
                widget_class=widget_class,
                parent=p,
                parameters=parameters,
                pack_options=pack_options,
                pack_propagate=pack_propagate,
                os=os,
                platform=platform,
                theme=self.theme,
                escape_special_chars=self.escape_chars,
                bool_change=self._bool_change,
                widget_type=widget_type,
                format_pack_options=self.format_pack_options,
            )
            code.add_line(rendered_code)
            rendered_code = widget_pack_propagate_code.render(
                widget_id=widget_id,
                widget_type=widget_type,
                pack_propagate=pack_propagate,
            )
            if rendered_code != "":
                code.add_line(rendered_code)

            rendered_code = widget_pack_code.render(
                widget_id=widget_id,
                pack_options=pack_options,
                format_pack_options=self.format_pack_options
            )
            code.add_line(rendered_code)
            if children != {}:
                self.loop_generate_oop(children, f"self.{parent.get_name()}", code)
    def get_parents(self, widget):
        if widget == self.r:
            self._parents.reverse()
            pass
        else:

            if not widget.master.__repr__().startswith("<"):
                self._parents.append(widget.master)
                self.get_parents(widget.master)

            else:
                self.get_parents(widget.master)




    def redraw(self, d):
        for x in list(d.keys()):

            if d[x] != {}:
                #btn = CTkButton(self, text=x.type, command=lambda x=x: x.on_drag_start(None))
                if x.pack_options == {}:
                    x.pack()
                else:
                    x.pack(**x.pack_options)
                self.redraw(d[x])
            else:
                if x.pack_options == {}:
                    x.pack()
                else:
                    x.pack(**x.pack_options)

    def destroy_children(self):
        for widget in self.r.winfo_children():
            widget.destroy()

    def add_to_dict(self, my_dict, key_list, value):
        current_dict = my_dict
        for key in key_list[:-1]:  # Iterate through all keys except the last one

            current_dict = current_dict[key]  # Move to the nested dictionary

        # If the current dict is not empty (There something already there)
        if current_dict[key_list[-1]] != {}:
            current_dict[key_list[-1]][value] = {}
            value.order = len(current_dict[key_list[-1]])

        # If the current dict is empty This is the first widget
        else:
            current_dict[key_list[-1]] = {value: {}}
            value.order = 1


    def get_first_degree_parent(self, my_dict, key_list):

        current_dict = my_dict
        for key in key_list[:-1]:  # Iterate through all keys except the last one

            current_dict = current_dict[key]  # Move to the nested dictionary

        return current_dict[key_list[-1]]

    def simple_order_dict(self, data_dict):
        """
        This function orders a dictionary by the 'order' variable of its class keys.

        Args:
            data_dict: The dictionary to be ordered.

        Returns:
            A new dictionary ordered by the 'order' attribute of the class keys.
        """
        # Use sorted with a lambda function directly accessing the order attribute
        return dict(sorted(data_dict.items(), key=lambda item: getattr(item[0], 'order', 0)))

    def loop_order_sort(self, d):
        """
        This function recursively sorts a dictionary based on class key order
        and sorts nested dictionaries (if possible).

        Args:
            d: The dictionary to be sorted.

        Returns:
            The modified dictionary with sorted elements.
        """

        new_d = self.simple_order_dict(d)


        for key in new_d:
            value = new_d[key]

            if value != {}:
                # Recursively sort nested dictionaries
                new_d[key] = self.loop_order_sort(value)

        return new_d

    def add_widget(self, w, properties, widget, x=0, y=0, part_of_component=False, return_widget=False, **kwargs):

        old_properties = properties
        if not part_of_component:
            if widget.master.master.__class__ == ScrollableFrame:
                new_widget = w(master=widget.master.master.get_me(), **properties, **kwargs)

            elif widget.master.master.master.__class__ == ScrollableFrame:
                new_widget = w(master=widget.master.master.master.get_me(), **properties, **kwargs)
            else:
                if widget.master.__class__ not in [ScrollableFrame, Frame, Main]:

                    new_widget = w(master=widget.master.master, **properties, **kwargs)

                else:
                    new_widget = w(master=widget.master, **properties, **kwargs)
        else:
            if widget.__class__ == ScrollableFrame:
                widget = widget.get_me()
            new_widget = w(master=widget, **properties, **kwargs)

        new_widget.num = self.total_num
        new_widget.name = new_widget.type + str(new_widget.num)
        self.apply_theme_to_widget(new_widget)
        new_widget._set_appearance_mode('light' if self.appearance.get() == 0 else 'dark')
        if new_widget.__class__ == Slider or new_widget.__class__ == Scrollbar or new_widget.__class__ == ScrollableFrame:
            new_widget.props["orientation"] = properties["orientation"]

        self.total_num += 1
        self.get_parents(new_widget)

        self.add_to_dict(self.widgets, self._parents, new_widget)

        self.id_mapped_widgets[new_widget._inner_id] = new_widget
        self._parents = []
        new_widget.configure(bg_color="transparent")
        new_widget.pack(padx=(0, 0), pady=(0, 0))

        if new_widget.__class__ == SegmentedButton:
            new_widget.configure(command=lambda e, nw=new_widget: (nw.on_drag_start(None), self.hierarchy.set_current_selection(nw)))
        elif new_widget.__class__ == ScrollableFrame:
            new_widget.scrollwindow.bind("<Button-1>", lambda e, nw=new_widget: (nw.on_drag_start(None), self.hierarchy.set_current_selection(nw)))
            new_widget.canv.bind("<Button-1>", lambda e, nw=new_widget: (nw.on_drag_start(None), self.hierarchy.set_current_selection(nw)))
        else:
            new_widget.bind("<Button-1>", lambda e, nw=new_widget: (nw.on_drag_start(None), self.hierarchy.set_current_selection(nw)))

        component = None

        try:
            component = new_widget.component
        except Exception as e:
            pass

        if component:
            new_widget.add_widgets(self.add_widget, properties=old_properties, widget=new_widget)
            ic(new_widget)

        #new_widget.bind("<Button-1>", new_widget.on_drag_start)

        self.hierarchy.delete_children()
        self.hierarchy.update_list(self.widgets, 5)
        #new_widget.place(x=x, y=y)
        if new_widget.__class__ != SegmentedButton:
            if widget.master.master.__class__ == ScrollableFrame:
                self.drag_manager.update_children(children=widget.master.master.winfo_children())
            elif widget.master.master.master.__class__ == ScrollableFrame:
                self.drag_manager.update_children(children=widget.master.master.master.winfo_children())
            else:
                self.drag_manager.update_children(children=widget.master.winfo_children())
        if return_widget:
            return new_widget

    def delete_from_dict(self, my_dict, key_list, value):
        current_dict = my_dict
        for key in key_list[:-1]:  # Iterate through all keys except the last one

            current_dict = current_dict[key]  # Move to the nested dictionary

        # If the current dict is not empty (There something already there)
        if current_dict[key_list[-1]] != {}:
            current_dict[key_list[-1]].pop(value)
    def show_palette(self, properties):
        #print(self.id_mapped_widgets, properties.color_manager.on_change_list)
        self.clear_toplevels()
        palette = PaletteEditor(color_manager=properties)
        self.windows_open.append(palette)

    def get_scrollbar_position(self, content_height, viewport_height, scrollbar_height):
        """
        Calculates the position of the scrollbar thumb.

        Args:
            content_height: The height of the content area.
            viewport_height: The height of the viewport (visible area).
            scrollbar_height: The height of the scrollbar.

        Returns:
            The position of the scrollbar thumb as a float between 0 and 1.
        """

        # Calculate the scrollable area (the difference between content height and viewport height)
        scrollable_area = content_height - viewport_height

        # If there is no scrollable area, the scrollbar is at the top (position 0)
        if scrollable_area <= 0:
            return 0

        # Calculate the ratio of the viewport height to the content height
        viewport_ratio = viewport_height / content_height

        # Calculate the ratio of the scrollbar height to the scrollable area
        scrollbar_ratio = scrollbar_height / scrollable_area

        # The scrollbar position is proportional to the offset of the content within the viewport
        # This offset can be found by multiplying the scrollable area by the ratio between the viewport height and content height
        offset = scrollable_area * (1 - viewport_ratio)

        # The scrollbar thumb position is then the offset normalized to the scrollable area, scaled by the ratio of the scrollbar height to the scrollable area
        position = offset / scrollable_area * scrollbar_ratio

        # Clamp the position between 0 and 1 to avoid going out of bounds
        return max(0.0, min(1.0, position))

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

    def on_vert_scrl(self, e):

        y = self.map_range(e, -100, 100, -self.vert_max_offset, self.vert_max_offset)
        self.r.place(y=y)
        self.r.winfo_toplevel().update()
        if self.current_selected_widget != None:
            self.draw_box(self.current_selected_widget)


    def on_vert_mouse(self, e):
        y = self.vert_scrl.get()
        y += e.delta
        y = max(-100, min(y, 100))
        self.vert_scrl.set(y)
        y = self.map_range(y, -100, 100, -self.vert_max_offset-100, self.vert_max_offset+100)
        self.r.place(y=y)
        self.r.winfo_toplevel().update()
        if self.current_selected_widget != None:
            self.draw_box(self.current_selected_widget)

    def move_delta(self, x, y):
        #print(x, y)
        self.r.place(x=x, y=y, anchor="center")
        self.r.winfo_toplevel().update()
        if self.current_selected_widget != None:
            self.draw_box(self.current_selected_widget)

    def on_horiz_scrl(self, e):

        x = self.map_range(e, -100, 100, -self.horiz_max_offset-100, self.horiz_max_offset+100)
        self.r.place(x=x)
        self.r.winfo_toplevel().update()
        if self.current_selected_widget != None:
            self.draw_box(self.current_selected_widget)

    def on_horiz_mouse(self, e):
        last_x = self.r.winfo_x()
        x = self.horiz_scrl.get()
        x += e.delta

        x = max(-100, min(x, 100))
        self.horiz_scrl.set(x)

        x = self.map_range(x, -100, 100, -self.horiz_max_offset, self.horiz_max_offset)

        self.r.place(x=x)
        self.r.winfo_toplevel().update()
        if self.current_selected_widget != None:
            self.draw_box(self.current_selected_widget)



    def get_x(self, widget):
        x = widget.winfo_x()
        y = 0
        if widget.master != self.r.master:
            y = self.get_x(widget.master)
        return x + y

    def get_y(self, widget):
        x = widget.winfo_y()
        y = 0
        if widget.master != self.r.master:
            y = self.get_y(widget.master)
        return x + y

    def draw_box(self, widget):
        if widget is not None:
            self.current_selected_widget = widget
            pad = 5
            x = self.get_x(widget) - pad
            y = self.get_y(widget) - pad
            parent = self.r.master
            width = widget.winfo_width() + (pad * 2)
            height = widget.winfo_height() + (pad * 2)
            self.destroy_box()
            self.left_box = CTkFrame(parent, width=2, height=height, fg_color="red", bg_color="red")
            self.left_box.place(x=x, y=y, anchor="nw")

            self.right_box = CTkFrame(parent, width=2, height=height, fg_color="red", bg_color="red")
            self.right_box.place(x=x+width, y=y, anchor="ne")

            self.top_box = CTkFrame(parent, width=width, height=2, fg_color="red", bg_color="red")
            self.top_box.place(x=x, y=y, anchor="nw")

            self.bottom_box = CTkFrame(parent, width=width, height=2, fg_color="red", bg_color="red")
            self.bottom_box.place(x=x, y=y+height, anchor="sw")
    def destroy_box(self):
        try:
            self.left_box.destroy()
            self.right_box.destroy()
            self.top_box.destroy()
            self.bottom_box.destroy()
        except Exception as e:
            pass

    def loop_clear_image(self, d):
        # I could destroy every child in self.r but could not add new widgets after destroying the children.

        for x in list(d.keys()):
            try:
                #x.cget("image").cget("light_image").close()
                #x.cget("image").cget("dark_image").close()
                #x.configure(image=None)
                x.img.cget("light_image").close()
                x.img.cget("dark_image").close()
                #x.img.configure(light_image=None)
                #x.img.configure(dark_image=None)

                #x.img = None

                #print("done")

            except Exception as e:
                #print(e)
                pass

            if d[x] != {}:
                self.loop_clear_image(d[x])


class WidgetButton(CTkButton):
    def __init__(self, on_drag, **kwargs):
        self.on_drag = on_drag

        super().__init__(**kwargs)
        self.configure(height=40)

    def pack(self, **kwargs):
        try:
            self.master.master.master.master.master.dragndrop_list.append(self) # OH MY GOD. WHY DID IT DO THIS!!!! REFACTOR REQUIRED!!
        except AttributeError as e:
            # There is a parent widget
            try:
                self.master.master.master.master.master.master.dragndrop_list.append(self) # OH MY GOD. WHY DID IT DO THIS!!!! REFACTOR REQUIRED!!
            except AttributeError as e:
                self.master.master.master.master.master.master.master.dragndrop_list.append(self) # OH MY GOD. WHY DID IT DO THIS!!!! REFACTOR REQUIRED!!

        super().pack(**kwargs)



class Hierarchy(CTkScrollableFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.change_parent_selection = None
        self.current_selection = None
        self.widget = None
        self.main = None
        self.mainwindow = None
        self.btns = []

    def set_current_selection(self, x):
        self.main.draw_box(x)
        #self.main.r.winfo_toplevel().update_idletasks()
        if x != self.main.r:
            for b in self.btns:
                b.configure(state="normal")
        else:

            for b in self.btns:
                b.configure(state="disabled")

        #self.current_selection = btn
        self.widget = x

        for child in self.winfo_children():

            if child.cget("text") != self.widget.get_name():
                child.configure(fg_color="#2B2B2B")
            else:
                self.current_selection = child
                child.configure(fg_color="#0084ff")


    def update_text(self, old_name, new_text):

        for child in self.winfo_children():
            if child.widget == self.widget and child.cget("text") == old_name:
                child.configure(text=new_text)

    def delete_widget(self):

        #self.widget.destroy()
        self.main._parents = []
        self.main.get_parents(self.widget)
        self.main.delete_from_dict(self.main.widgets, self.main._parents, self.widget)
        self.main._parents = []

        self.widget.destroy()
        self.widget = None
        self.current_selection = None
        self.main.destroy_box()
        self.delete_children()
        self.update_list(self.main.widgets, 5)
        for btn in self.btns:
            btn.configure(state="disabled")


    def move_up(self):
        if self.current_selection != None:
            self.main.get_parents(self.widget)
            parents = self.main._parents
            siblings = self.main.get_first_degree_parent(self.main.widgets, parents)
            selection_order = self.widget.order
            sib = None
            for sibling in siblings:
                if sibling.order + 1 == selection_order:
                    sib = sibling
                    break
            if sib is not None:
                sib.order = selection_order
                self.widget.order = sib.order - 1
                self.widget.pack(**self.widget.pack_options, before=sib)
                self.main.widgets = self.main.loop_order_sort(self.main.widgets)

                self.delete_children()
                self.update_list(self.main.widgets, 5)

            self.main._parents = []
            self.current_selection = None
            self.main.destroy_box()

            self.widget = None
            for btn in self.btns:
                btn.configure(state="disabled")
            ##print(self.main.widgets)
    def move_down(self):
        if self.current_selection != None:
            self.main.get_parents(self.widget)
            parents = self.main._parents
            siblings = self.main.get_first_degree_parent(self.main.widgets, parents)
            selection_order = self.widget.order
            sib = None
            for sibling in siblings:
                if sibling.order - 1 == selection_order:
                    sib = sibling
                    break
            if sib is not None:
                sib.order = selection_order
                self.widget.order = sib.order + 1
                self.widget.pack(**self.widget.pack_options, after=sib)
                self.main.widgets = self.main.loop_order_sort(self.main.widgets)

                self.delete_children()
                self.update_list(self.main.widgets, 5)

            self.main._parents = []
            self.current_selection = None
            self.main.destroy_box()

            self.widget = None
            for btn in self.btns:
                btn.configure(state="disabled")
            ##print(self.main.widgets)

    def update_list(self, d, pad):
        try:
            self.current_selection = None

            self.widget = None
            for x in list(d.keys()):
                if d[x] != {}:
                    btn = CTkButton(self, text=x.get_name(), fg_color="#2B2B2B", hover=False)
                    #x.bind("<Button-1>", lambda e, x=x, btn=btn: (x.on_drag_start(None), self.set_current_selection(btn, x)))
                    btn.configure(command=lambda x=x: (x.on_drag_start(None), self.set_current_selection(x)))
                    btn.widget = x
                    btn.pack(fill="x", padx=(pad, 5), pady=2.5)
                    self.update_list(d[x], pad+20)
                else:

                    btn = CTkButton(self, text=x.get_name(), fg_color="#2B2B2B", hover=False)
                    #x.bind("<Button-1>", lambda e, x=x, btn=btn: (x.on_drag_start(None), self.set_current_selection(btn, x)))
                    btn.configure(command=lambda x=x: (x.on_drag_start(None), self.set_current_selection(x)))
                    btn.widget = x
                    btn.pack(fill="x", padx=(pad, 5), pady=2.5)
            self.main.destroy_box()
        except tkinter.TclError as e:
            pass

    def _change_parent(self, widget, new_parent):

        self.s = {new_parent.get_name(): {}}
        self.main._parents = []
        self.main.get_parents(new_parent)
        self.parent_parents = self.main._parents
        self.main._parents = []
        self.main.get_parents(widget)

        # ic(self.main._parents)
        d = self.main.widgets.copy()

        for key in self.main._parents:
            d = d[key]

        val = d[widget]
        d = {widget: val}

        # ic(self.main.widgets)

        # ic(d)
        self.main._parents = []
        self.main.loop_save(d, new_parent.get_name(), self.s)
        self.s = self.s[new_parent.get_name()]

        # ic(self.main.widgets)
        self.main._parents = []
        self.main.get_parents(new_parent)
        self.main._parents.append(new_parent)

        self.main.loop_open(self.s, self.main._parents[-1], copy=False)
        self.main.hierarchy.delete_children()
        self.main.hierarchy.update_list(self.main.widgets, 5)

        self.main._parents = []

        # self.s[self.r.get_name()]["theme"] = self.theme_manager.name
        # ic(self.main.widgets)
        self.widget = widget
        self.delete_widget()
        self.top_level.destroy()
        self.main.destroy_box()



    def get_frames_scrollbar_only(self):
        new_arr = []
        children = self.winfo_children()
        for widget in children:
            #print(widget.widget)
            if widget.widget.__class__ in [Frame, Main, ScrollableFrame]:
                new_arr.append([widget, widget.pack_info()["padx"], widget.widget])
        return new_arr

    def set_change_parent_selection(self, x, btn):
        self.change_parent_selection = x
        self._change_parent(widget=self.widget, new_parent=self.change_parent_selection)


    def change_parent(self):
        self.top_level = CTkToplevel()
        self.top_level.geometry("500x500")
        self.top_level.title("Change Parent")
        self.top_level.after(20, self.top_level.lift)
        self.scrl = CTkScrollableFrame(self.top_level)
        self.scrl.pack(fill="both", expand=True)

        arr = self.get_frames_scrollbar_only()
        for x in arr:
            btn = CTkButton(self.scrl, text=x[2].get_name(), fg_color="#2B2B2B", hover=False)
            # x.bind("<Button-1>", lambda e, x=x, btn=btn: (x.on_drag_start(None), self.set_current_selection(btn, x)))
            btn.configure(command=lambda x=x[2], btn=btn: (self.set_change_parent_selection(x, btn)))
            btn.widget = x[2]
            btn.pack(fill="x", padx=x[1], pady=2.5)



    def duplicate_widget(self):
        # This method is not efficient
        #ic(self.main.widgets)
        self.s = {self.widget.get_name(): {}}
        self.main._parents = []
        self.main.get_parents(self.widget)

        #ic(self.main._parents)
        d = self.main.widgets.copy()
        for key in self.main._parents:
            d = d[key]

        val = d[self.widget]
        d = {self.widget: val}
        #ic(self.main.widgets)

        #ic(d)
        self.main._parents = []
        self.main.loop_save(d, self.widget.get_name(), self.s)
        self.s = self.s[self.widget.get_name()]
        #ic(self.main.widgets)
        self.main._parents = []
        self.main.get_parents(self.widget)


        ic(self.main.get_first_degree_parent(self.main.widgets, self.main._parents), self.main.widgets, self.widget, self.widget.master, self.s, self.main._parents)
        self.main.loop_open(self.s, self.main._parents[-1], copy=True)
        self.main.hierarchy.delete_children()
        self.main.hierarchy.update_list(self.main.widgets, 5)

        self.main._parents = []

        #self.s[self.r.get_name()]["theme"] = self.theme_manager.name
        #ic(self.main.widgets)


    def delete_children(self):
        for widget in self.winfo_children():
            widget.destroy()


class PaletteEditor(CTkToplevel):
    def __init__(self, *args, color_manager, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x500")
        self.color = "#FFFFFF"
        self.title("Palette Editor")
        self.after(20, self.lift)
        self.after(25, self.focus_get)
        self.wm_iconbitmap()
        self.iconpath = ImageTk.PhotoImage(file=resource_path('Logo.ico'))
        self.after(100, lambda: self.iconphoto(False, self.iconpath))

        self.current_selection = [None, None]
        self.clickables = []
        self.color_manager = color_manager.color_manager
        self.scrl = CTkScrollableFrame(self)
        self.scrl.pack(fill="both", expand=True, padx=10, pady=(10, 0))

        self.frame2 = CTkFrame(self)
        self.frame2.pack(fill="x", padx=10, pady=(10, 5))

        self.name_entry = CTkEntry(self.frame2, placeholder_text="Enter Name")
        self.name_entry.pack(side="left", fill="x", expand=True, padx=(10, 0), pady=5)

        self.add_btn = CTkButton(self.frame2, text="Add", width=50, command=self.add)
        self.add_btn.pack(side="left", padx=10)

        self.fr = CTkFrame(self)
        self.fr.pack(padx=10, pady=(5, 10), fill="x")

        self.c = CTkButton(self.fr, width=100, height=100, text="", fg_color=self.color, hover=False, command=self.get_color)
        self.c.pack(side="left")



        self.hex = CTkLabel(self.fr, text=f"HEX: {self.color}", anchor="w")
        self.hex.pack(fill="x", padx=10, pady=5, expand=True)


        self.rgb = CTkLabel(self.fr, text=f"RGB: {self.hex_to_rgb(self.color)}", anchor="w")
        self.rgb.pack(fill="x", padx=10, pady=(0, 5), expand=True)

        self.change_btn = CTkButton(self.fr, text=f"Change", command=self.use)
        self.change_btn.pack(fill="x", padx=10, pady=(0, 10), expand=True)

        for x in list(self.color_manager.colors.keys()):
            self.add_color_option(x, self.color_manager.get_color(x))

    def add(self):
        self.color_manager.add_color(name=self.name_entry.get(), color=self.c.cget("fg_color"))
        self.add_color_option(self.name_entry.get(), self.color_manager.get_color(self.name_entry.get()))
        self.name_entry.delete(0, "end")

    def hex_to_rgb(self, value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

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

        btn = CTkButton(c, text="X",fg_color="#D0255E", hover_color="#AE1E4F", width=50, height=50)
        btn.pack(side="left", padx=10)


        for x in [c, clr, fr, lbl, lbl2]:
            x.bind("<Button-1>", lambda e, name=name, val=val: (self.select(name, val), self.change_selection([fr, c])))
        btn.configure(command=lambda: (self.color_manager.delete_color(name), c.destroy()))
        self.select(name, val)
        self.change_selection([fr, c])
        self.clickables.append([fr, c])
    def get_color(self):
        c = askcolor(initialcolor=self.c.cget("fg_color"))
        if c != (None, None):
            self.c.configure(fg_color=c[1])

    def use(self):
        if self.command != None:
            #self.command(self.c.cget("fg_color"), self.current_selection)
            self.color_manager.edit(name=self.current_selection[0], val=self.c.cget("fg_color"))
            self.destroy()



    def change_selection(self, clr):
        for x in self.clickables:
            for y in x:
                y.configure(fg_color="transparent")
        for x in clr:
            x.configure(fg_color="#1F6AA5")

    def rgb2hex(self, c):
        return '#%02x%02x%02x' % c

class WindowResizer(CTkFrame):
    def __init__(self, *args, orientation="vertical", widget=None, multiplier=1.5, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = widget
        self.multiplier = multiplier
        self.orientation = orientation
        if widget != None:
            self.init()

    def init(self):
        self.lbl = CTkLabel(self, text="...", font=CTkFont(size=6, weight="bold"))
        self.lbl.pack(expand=True)
        if self.orientation == "vertical":
            self.configure(width=5)
            self.change_dir = "x"
            self.val = self.widget.cget("width")
            self.lbl.configure(cursor="sb_h_double_arrow",  wraplength=1)

            self.bind("<Enter>", lambda e: self.winfo_toplevel().configure(cursor="sb_h_double_arrow"))

        else:
            self.configure(height=5)
            self.change_dir = "y"
            self.val = self.widget.cget("height")
            self.lbl.configure(cursor="sb_v_double_arrow", text=". . .")
            self.bind("<Enter>", lambda e: self.winfo_toplevel().configure(cursor="sb_v_double_arrow"))

        self.bind("<Button-1>", self.pressed)
        self.lbl.bind("<Button-1>", self.pressed)
        self.bind("<ButtonRelease>", self.released)
        self.lbl.bind("<ButtonRelease>", self.released)
        self.bind("<Leave>", lambda e: self.winfo_toplevel().configure(cursor="arrow"))

        self.prev = 0

    def configure(self, require_redraw=False, **kwargs):
        if "widget" in kwargs:
            self.widget = kwargs.pop("widget")
            self.init()

        super().configure(**kwargs)


    def pressed(self, e):
        self.winfo_toplevel().bind("<B1-Motion>", self.dragged)
        if self.change_dir == "x":
            self.prev = self.winfo_pointerx()
        else:
            self.prev = self.winfo_pointery()

    def dragged(self, e):
        if self.change_dir == "x":
            delta = self.winfo_pointerx() - self.prev
            delta *= self.multiplier
            self.widget.configure(width=self.val + delta)
            self.prev = self.winfo_pointerx()
            self.val += delta
        else:
            delta = self.winfo_pointery() - self.prev
            print(delta)

            delta *= self.multiplier
            self.widget.configure(height=self.val + delta)
            self.prev = self.winfo_pointery()
            self.val += delta


    def released(self, e):
        self.winfo_toplevel().unbind("<B1-Motion>")




class App(CTkToplevel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.geometry("1900x1000+10+0")
        self.title("Custom Tkinter Builder")
        self.app_theme = "blue"
        self.canvas_theme = "green"
        self.after(20, self.lift)
        self.after(25, self.focus_get)

        self.after(100, lambda: (shutil.rmtree(tempify("temp")), os.mkdir(tempify("temp"))))

        self.tool_bar = CTkFrame(self, height=40)
        self.tool_bar.pack(side="top", fill="x", padx=10, pady=(10, 0))

        self.home_btn = CTkButton(self.tool_bar, text="", height=28, width=28, image=CTkImage(light_image=Image.open(resource_path(os.path.join(
            "Assets", "baseline_home_white_18dp_1x.png"))), dark_image=Image.open(resource_path(os.path.join("Assets", "baseline_home_white_18dp_1x.png"))), size=(18, 18)))
        self.home_btn.pack(side="left", padx=5, pady=5)
        #self.home_btn.configure(image=self.home_btn.image)

        self.save_btn = CTkButton(self.tool_bar, text="Save", fg_color="transparent", width=50)
        self.save_btn.pack(side="left", padx=5, pady=5)

        self.saveas_btn = CTkButton(self.tool_bar, text="Save As", fg_color="transparent", width=50)
        self.saveas_btn.pack(side="left", padx=5, pady=5)

        self.open_btn = CTkButton(self.tool_bar, text="Open", fg_color="transparent", width=50)
        #self.open_btn.pack(side="left", padx=5, pady=5)





        self.palette_btn = CTkButton(self.tool_bar, text="Edit Palette", fg_color="transparent", width=50)
        self.palette_btn.pack(side="left", padx=5, pady=5)



        self.run_code_btn = CTkButton(self.tool_bar, text="Run Code", fg_color="#0084ff", width=50, hover=False)
        self.run_code_btn.pack(side="right", padx=5, pady=5)


        self.export_code_btn = CTkButton(self.tool_bar, text="Export Code", fg_color="transparent", width=50)
        self.export_code_btn.pack(side="right", padx=5, pady=5)

        self.create_component_btn = CTkButton(self.tool_bar, text="Create Component", fg_color="transparent", width=50)
        #self.create_component_btn.pack(side="right", padx=5, pady=5)

        self.appearance_mode_switch = AppearanceButton(self.tool_bar)
        self.appearance_mode_switch.pack(side="right", padx=5, pady=5)

        if darkdetect.isDark():
            self.appearance_mode_switch.toggle()


        self.widget_panel = CTkTabview(self, width=350)
        self.widget_panel.pack(side=LEFT, padx=10, pady=(0, 10), fill="y")
        self.widget_panel.dragndrop_list = []
        self.widget_panel.add("Core Widgets")
        self.widget_panel.add("Themed Widgets")

        self.widget_panel_resizer = WindowResizer(self, orientation="vertical", widget=self.widget_panel)
        self.widget_panel_resizer.pack(side="left", fill="y")

        self.widget_panel_core_tab = self.widget_panel.tab("Core Widgets")
        self.widget_panel_themed_tab = self.widget_panel.tab("Themed Widgets")

        self.widget_panel_core = CTkScrollableFrame(self.widget_panel_core_tab, fg_color="transparent")
        self.widget_panel_core.pack(padx=(0, 5), pady=5, fill="both", expand=True)

        self.widget_panel_themed = CTkScrollableFrame(self.widget_panel_themed_tab, fg_color="transparent")
        self.widget_panel_themed.pack(padx=(0, 5), pady=5, fill="both", expand=True)

        self.add_frame_btn = WidgetButton(master=self.widget_panel_core, text="Frame", height=50,
                                          on_drag=lambda x, y, widget: self.main.add_widget(Frame, properties={"properties":self.properties_panel}, x=x, y=y, widget=widget))
        self.add_frame_btn.pack(padx=10, pady=(10, 0), fill="x")



        self.add_vert_scrl_frame_btn = WidgetButton(master=self.widget_panel_core, text="Vertical Scrollable Frame", height=50, on_drag=lambda x, y, widget: self.main.add_widget(ScrollableFrame, properties={"properties":self.properties_panel, "orientation": "vertical"}, x=x, y=y, widget=widget))
        self.add_vert_scrl_frame_btn.pack(padx=10, pady=(10, 0), fill="x")

        self.add_horiz_scrl_frame_btn = WidgetButton(master=self.widget_panel_core, text="Horizontal Scrollable Frame", height=50,
                                               on_drag=lambda x, y, widget: self.main.add_widget(ScrollableFrame,
                                                                                                 properties={
                                                                                                     "properties": self.properties_panel,
                                                                                                     "orientation": "horizontal"},
                                                                                                 x=x, y=y,
                                                                                                 widget=widget))
        self.add_horiz_scrl_frame_btn.pack(padx=10, pady=(10, 0), fill="x")

        self.add_label_btn = WidgetButton(master=self.widget_panel_core, text="Label", height=50, on_drag=lambda x, y, widget: self.main.add_widget(Label, properties={"properties":self.properties_panel}, x=x, y=y, widget=widget))
        self.add_label_btn.pack(padx=10, pady=(10, 0), fill="x")

        self.add_button_btn = WidgetButton(master=self.widget_panel_core, text="Button", height=50, on_drag=lambda x, y, widget: self.main.add_widget(Button, properties={"properties":self.properties_panel}, x=x, y=y, widget=widget))
        self.add_button_btn.pack(padx=10, pady=(10, 0), fill="x")

        self.add_entry_btn = WidgetButton(master=self.widget_panel_core, text="Entry", height=50,
                                          on_drag=lambda x, y, widget: self.main.add_widget(Entry, properties={"properties":self.properties_panel}, x=x, y=y, widget=widget))
        self.add_entry_btn.pack(padx=10, pady=(10, 0), fill="x")

        self.add_switch_btn = WidgetButton(master=self.widget_panel_core, text="Switch", height=50,
                                          on_drag=lambda x, y, widget: self.main.add_widget(Switch, properties={
                                              "properties": self.properties_panel}, x=x, y=y, widget=widget))
        self.add_switch_btn.pack(padx=10, pady=(10, 0), fill="x")


        self.add_checkbox_btn = WidgetButton(master=self.widget_panel_core, text="Check Box", height=50,
                                               on_drag=lambda x, y, widget: self.main.add_widget(CheckBox,
                                                                                                 properties={
                                                                                                     "properties": self.properties_panel},
                                                                                                 x=x, y=y,
                                                                                                 widget=widget))
        self.add_checkbox_btn.pack(padx=10, pady=(10, 0), fill="x")

        self.add_radiobutton_btn = WidgetButton(master=self.widget_panel_core, text="Radio Button", height=50,
                                             on_drag=lambda x, y, widget: self.main.add_widget(RadioButton,
                                                                                               properties={
                                                                                                   "properties": self.properties_panel},
                                                                                               x=x, y=y,
                                                                                               widget=widget))
        self.add_radiobutton_btn.pack(padx=10, pady=(10, 0), fill="x")




        self.add_horizontalslider_btn = WidgetButton(master=self.widget_panel_core, text="Horizontal Slider", height=50,
                                               on_drag=lambda x, y, widget: self.main.add_widget(Slider,
                                                                                                 properties={
                                                                                                     "properties": self.properties_panel, "orientation": "horizontal"},
                                                                                                 x=x, y=y,
                                                                                                 widget=widget))
        self.add_horizontalslider_btn.pack(padx=10, pady=(10, 0), fill="x")

        self.add_verticalslider_btn = WidgetButton(master=self.widget_panel_core, text="Vertical Slider", height=50,
                                           on_drag=lambda x, y, widget: self.main.add_widget(Slider,
                                                                                             properties={
                                                                                                 "properties": self.properties_panel, "orientation": "vertical"},
                                                                                             x=x, y=y,
                                                                                             widget=widget))
        self.add_verticalslider_btn.pack(padx=10, pady=(10, 0), fill="x")
        self.add_combobox_btn = WidgetButton(master=self.widget_panel_core, text="Combo Box", height=50,
                                                      on_drag=lambda x, y, widget: self.main.add_widget(ComboBox,
                                                                                                        properties={
                                                                                                            "properties": self.properties_panel},
                                                                                                        x=x, y=y,
                                                                                                        widget=widget))
        self.add_combobox_btn.pack(padx=10, pady=(10, 0), fill="x")

        self.add_optionmenu_btn = WidgetButton(master=self.widget_panel_core, text="Option Menu", height=50,
                                               on_drag=lambda x, y, widget: self.main.add_widget(OptionMenu,
                                                                                                 properties={
                                                                                                     "properties": self.properties_panel},
                                                                                                 x=x, y=y,
                                                                                                 widget=widget))
        self.add_optionmenu_btn.pack(padx=10, pady=(10, 0), fill="x")

        self.add_progressbar_btn = WidgetButton(master=self.widget_panel_core, text="Progress Bar", height=50,
                                          on_drag=lambda x, y, widget: self.main.add_widget(ProgressBar, properties={
                                              "properties": self.properties_panel}, x=x, y=y, widget=widget))
        self.add_progressbar_btn.pack(padx=10, pady=(10, 0), fill="x")

        self.add_segmentedbutton_btn = WidgetButton(master=self.widget_panel_core, text="Segmented Button", height=50,
                                                    on_drag=lambda x, y, widget: self.main.add_widget(SegmentedButton,
                                                                                                      properties={
                                                                                                          "properties": self.properties_panel},
                                                                                                      x=x, y=y,
                                                                                                      widget=widget))
        self.add_segmentedbutton_btn.pack(padx=10, pady=(10, 0), fill="x")

        self.add_textbox_btn = WidgetButton(master=self.widget_panel_core, text="TextBox", height=50,
                                          on_drag=lambda x, y, widget: self.main.add_widget(TextBox, properties={
                                              "properties": self.properties_panel}, x=x, y=y, widget=widget))
        self.add_textbox_btn.pack(padx=10, pady=(10, 0), fill="x")

        self.add_horizontalscrollbar_btn = WidgetButton(master=self.widget_panel_core, text="Horizontal Scrollbar", height=50,
                                                on_drag=lambda x, y, widget: self.main.add_widget(Scrollbar,
                                                                                                  properties={
                                                                                                      "properties": self.properties_panel, "orientation": "horizontal"},
                                                                                                  x=x, y=y,
                                                                                                  widget=widget))
        self.add_horizontalscrollbar_btn.pack(padx=10, pady=(10, 0), fill="x")

        self.add_verticalscrollbar_btn = WidgetButton(master=self.widget_panel_core, text="Vertical Scrollbar", height=50,
                                              on_drag=lambda x, y, widget: self.main.add_widget(Scrollbar,
                                                                                                properties={
                                                                                                    "properties": self.properties_panel, "orientation": "vertical"},
                                                                                                x=x, y=y,
                                                                                                widget=widget))
        self.add_verticalscrollbar_btn.pack(padx=10, pady=(10, 0), fill="x")




        self.temp_panel = CTkFrame(self, fg_color="transparent")
        self.temp_panel.pack(side="left", pady=10, fill="both", expand=True)

        self.main_window_panel = CTkFrame(self.temp_panel, fg_color=("#1D1D1D", "#EEEEEE"))
        self.main_window_panel.pack(fill="both", expand=True, padx=5, pady=5)

        self.horiz_scrlbar = CTkSlider(master=self.temp_panel, from_=100, to=-100, number_of_steps=200, orientation="horizontal",
                                       button_length=33, width=13)
        self.horiz_scrlbar.configure(progress_color=self.horiz_scrlbar.master.cget("bg_color"),
                                     fg_color=self.horiz_scrlbar.master.cget("bg_color"))
        self.horiz_scrlbar.pack(fill="x", padx=10)

        self.vert_scrlbar = CTkSlider(master=self, from_=-100, to=100, number_of_steps=200, orientation="vertical", button_length=33, width=13)
        self.vert_scrlbar.configure(progress_color=self.vert_scrlbar.cget("bg_color"), fg_color=self.vert_scrlbar.cget("bg_color"))
        self.vert_scrlbar.pack(side="left", fill="y", padx=(10, 0), pady=10)

        # Themed Widgets

        classes = self.get_component()
        for class_ in classes:

            self.btn = WidgetButton(master=self.widget_panel_themed, text=class_.as_str(), height=50,
                                                 on_drag=lambda x, y, widget: self.main.add_widget(
                                                     class_, properties={"properties": self.properties_panel}, x=x, y=y, widget=widget))
            self.btn.pack(fill="x", expand=True, padx=5, pady=(10, 0))



        t = CTkFrame(self.widget_panel_themed)
        t.pack(fill="x")
        self.add_button_1_btn = WidgetButton(master=t, text="Button 1", height=50,
                                           on_drag=lambda x, y, widget: self.main.add_widget(ThemedButton.Button_1, properties={
                                               "properties": self.properties_panel}, x=x, y=y, widget=widget))
        self.add_button_1_btn.pack(side="left", fill="x", expand=True, padx=5, pady=(10, 0))
        self.add_button_1_btn.configure(text="Button 1", width=140, height=38, corner_radius=3, fg_color=("#797979", "#000000"), hover_color=("#4e4e4e", "#434343"), border_color=("#000000", "#a2a2a2"), border_width=1, font=CTkFont(size=15, weight="normal"))

        self.add_button_2_btn = WidgetButton(master=t, text="Button 2", height=50,
                                           on_drag=lambda x, y, widget: self.main.add_widget(ThemedButton.Button_2, properties={
                                               "properties": self.properties_panel}, x=x, y=y, widget=widget))
        self.add_button_2_btn.pack(side="right", fill="x", expand=True, padx=5, pady=(10, 0))
        self.add_button_2_btn.configure(image=CTkImage(Image.open(resource_path(os.path.join("Assets", "baseline_arrow_forward_white_18dp_1x.png"))), size=(18, 18)), width=140, height=38, compound="right", text="Next", corner_radius=30, fg_color=("#2CC985", "#2FA572"), text_color=("gray98", "#DCE4EE"), hover_color=("#0C955A", "#106A43"), border_color=("#3E454A", "#949A9F"), border_width=0, text_color_disabled=("gray78", "gray68"), font=CTkFont(size=15, weight="normal"))
        t = CTkFrame(self.widget_panel_themed)
        t.pack(fill="x")

        self.add_button_3_btn = WidgetButton(master=t, text="Button 3", height=50,
                                           on_drag=lambda x, y, widget: self.main.add_widget(ThemedButton.Button_3, properties={
                                               "properties": self.properties_panel}, x=x, y=y, widget=widget))
        self.add_button_3_btn.pack(fill="x", side="left", expand=True, pady=(10, 0), padx=(5, 0))
        self.add_button_3_btn.configure(width=140, height=38, text="Purchase", corner_radius=3, fg_color=("#993500", "#282525"), text_color=("gray98", "#ffffff"), hover_color=("#2d2929", "#993500"), border_color=("#5f5f5f", "#ffffff"), border_width=1, text_color_disabled=("gray78", "gray68"), font=CTkFont(size=15, weight="bold"))

        o = CTkFrame(t, width=self.add_button_3_btn.cget("width"), height=50, fg_color="transparent")
        o.pack(fill="x", side="right", expand=True, padx=5, pady=(10, 0))
        o.pack_propagate(False)
        self.add_icon_white_btn = WidgetButton(master=o, text="Icon White", height=50,
                                           on_drag=lambda x, y, widget: self.main.add_widget(
                                               ThemedButton.Button_Icon_white, properties={
                                               "properties": self.properties_panel}, x=x, y=y, widget=widget))
        self.add_icon_white_btn.pack(side="left", expand=True)
        self.add_icon_white_btn.configure(width=40, height=40, text="", corner_radius=3, fg_color=("#3965FF", "#3965FF"), text_color=("#ffffff", "#ffffff"), hover_color=("#2B4DC6", "#2B4DC6"), border_color=("#3E454A", "#949A9F"), border_width=0, text_color_disabled=("gray78", "gray68"), image=CTkImage(Image.open(resource_path(os.path.join(
            "Assets", "baseline_people_white_18dp_1x.png"))), size=(18, 18)))

        self.add_icon_black_btn = WidgetButton(master=o, text="Icon Black", height=50,
                                           on_drag=lambda x, y, widget: self.main.add_widget(
                                               ThemedButton.Button_Icon_black, properties={
                                               "properties": self.properties_panel}, x=x, y=y, widget=widget))
        self.add_icon_black_btn.pack(side="right", expand=True)
        self.add_icon_black_btn.configure(width=40, height=40, text="", corner_radius=3, fg_color=("#40B6FF", "#40B6FF"), text_color=("#ffffff", "#ffffff"), hover_color=("#00D9FF", "#00D9FF"), border_color=("#3E454A", "#949A9F"), border_width=0, text_color_disabled=("gray78", "gray68"), image=CTkImage(Image.open(resource_path(os.path.join(
            "Assets", "baseline_people_black_18dp_1x.png"))), size=(18, 18)))

        self.add_heading_1_btn = WidgetButton(master=self.widget_panel_themed, text="Heading 1", height=50,
                                          on_drag=lambda x, y, widget: self.main.add_widget(ThemedText.Heading_1, properties={
                                              "properties": self.properties_panel}, x=x, y=y, widget=widget))
        self.add_heading_1_btn.pack(padx=5, pady=(10, 0), fill="x")
        self.add_heading_1_btn.configure(text="Heading 1", font=CTkFont(size=45, weight="bold"), border_width=0)

        self.add_heading_2_btn = WidgetButton(master=self.widget_panel_themed, text="Heading 2", height=50,
                                            on_drag=lambda x, y, widget: self.main.add_widget(ThemedText.Heading_2,
                                                                                              properties={
                                                                                                  "properties": self.properties_panel},
                                                                                              x=x, y=y, widget=widget))
        self.add_heading_2_btn.pack(padx=5, pady=(10, 0), fill="x")
        self.add_heading_2_btn.configure(text="Heading 2", font=CTkFont(size=45, weight="normal"), border_width=0)


        self.add_heading_3_btn = WidgetButton(master=self.widget_panel_themed, text="Sub Heading", height=50,
                                              on_drag=lambda x, y, widget: self.main.add_widget(ThemedText.SubHeading,
                                                                                                properties={
                                                                                                    "properties": self.properties_panel},
                                                                                                x=x, y=y,
                                                                                                widget=widget))
        self.add_heading_3_btn.pack(padx=5, pady=(10, 0), fill="x")
        self.add_heading_3_btn.configure(text="Sub Heading", font=CTkFont(size=30, weight="normal"), border_width=0)

        self.add_paragraph_1_btn = WidgetButton(master=self.widget_panel_themed, text="Paragraph 1", height=50,
                                              on_drag=lambda x, y, widget: self.main.add_widget(ThemedText.Paragraph_1,
                                                                                                properties={
                                                                                                    "properties": self.properties_panel},
                                                                                                x=x, y=y,
                                                                                                widget=widget))
        self.add_paragraph_1_btn.pack(padx=5, pady=(10, 0), fill="x")
        self.add_paragraph_1_btn.configure(text="I am Paragraph 1", font=CTkFont(size=15, weight="normal"), border_width=0)
        self.add_wrapped_paragraph_btn = WidgetButton(master=self.widget_panel_themed, text="Wrapped Paragraph", height=50,
                                                on_drag=lambda x, y, widget: self.main.add_widget(
                                                    ThemedText.WrappedParagraph,
                                                    properties={
                                                        "properties": self.properties_panel},
                                                    x=x, y=y,
                                                    widget=widget))
        self.add_wrapped_paragraph_btn.pack(padx=5, pady=(10, 0), fill="x")
        self.add_wrapped_paragraph_btn.configure(text="Lorem ipsum dolor sit amet,\n consectetur adipiscing elit,\n sed do eiusmod tempor\n incididunt ut labore et dolore\n magna aliqua.", font=CTkFont(size=15, weight="normal"), border_width=0)

        self.temp = CTkFrame(self.main_window_panel, fg_color=self.main_window_panel.cget("fg_color"))
        self.temp.pack(fill="both", expand=True, pady=10, padx=10)

        self.message_box = MessageBox(self.temp)
        self.message_box.place(relx=1, rely=1, x=-10, y=-10, anchor="se")

        self.drag_frame = CTkFrame(self.temp, fg_color="transparent")
        #self.drag_frame.place(x=0, y=0, relwidth=1, relheight=1)


        #self.temp.bind("<Button-1>", lambda e: self.temp.focus_set())

        self.main_window = Main(self.temp, properties=None, width=500, height=500, bg_color=("grey10", "grey80"))
        self.main_window.pack_propagate(False)
        self.main_window.place(anchor="center", relx=0.5, rely=0.5)
        self.main_window.type = "MAIN"
        self.main_window.num = -1
        self.main_window.name = self.main_window.type + str(self.main_window.num)
        self.drag_manager = DragManager(self.widget_panel.dragndrop_list, self.main_window, self)

        self.main = MainWindow(self.main_window, self.canvas_theme)
        self.main.drag_frame = self.drag_frame
        self.main.message_box = self.message_box
        self.main.drag_manager = self.drag_manager
        self.main_window.configure(fg_color=self.main.theme["CTk"]["fg_color"], bg_color=self.main_window.master.cget("fg_color")[1])

        self.hierarchy_and_properties_resizer = WindowResizer(self, orientation="vertical", multiplier=-1)
        self.hierarchy_and_properties_resizer.pack(side="left", fill="y", padx=(5, 0))
        self.container = CTkFrame(self, width=350, fg_color="transparent")
        self.container.pack(side=LEFT, padx=10, pady=10, fill="y")
        self.container.pack_propagate(False)
        self.hierarchy_and_properties_resizer.configure(widget=self.container)

        self.update()
        visible_area = self.main_window_panel.winfo_height()
        content_height = self.main_window.cget("height")
        hidden_area = (content_height - visible_area)
        offset = hidden_area//2
        offset += 50
        #print(offset, hidden_area, content_height, visible_area)

        #self.vert_scrlbar.set(scrollbar_position, scrollbar_height+scrollbar_position)
        self.main.vert_scrl = self.vert_scrlbar
        self.vert_scrlbar.configure(command=self.main.on_vert_scrl)
        self.main_window.bind("<MouseWheel>", self.main.on_vert_mouse)
        self.temp.bind("<MouseWheel>", self.main.on_vert_mouse)
        self.main.appearance = self.appearance_mode_switch

        self.main.vert_max_offset = abs(offset)

        visible_area = self.main_window_panel.winfo_width()
        content_height = self.main_window.cget("width")
        hidden_area = (content_height - visible_area)
        offset = hidden_area // 2
        offset += 50
        #print(offset, hidden_area, content_height, visible_area)

        # self.vert_scrlbar.set(scrollbar_position, scrollbar_height+scrollbar_position)
        self.main.horiz_scrl = self.horiz_scrlbar
        self.horiz_scrlbar.configure(command=self.main.on_horiz_scrl)
        self.main_window.bind("<Shift-MouseWheel>", self.main.on_horiz_mouse)
        self.temp.bind("<Shift-MouseWheel>", self.main.on_horiz_mouse)
        self.main.horiz_max_offset = abs(offset)



        self.hierarchy = Hierarchy(self.container, height=350)
        self.hierarchy.pack(fill="both")
        self.main.hierarchy = self.hierarchy
        self.hierarchy.main = self.main
        self.hierarchy.mainwindow = self.main_window
        self.hierarchy_tools_container = CTkFrame(self.container, height=40)
        self.hierarchy_tools_container.pack(fill="x", pady=(0, 10))

        #FontManager.load_font("Fonts/MaterialIconsOutlined-Regular.otf") # Can't load fonts
        self.move_top_btn = CTkButton(self.hierarchy_tools_container, text="south", font=("MaterialIconsOutlined-Regular", 22), width=30, height=30, command=self.hierarchy.move_up)
        self.move_top_btn.pack(side="left", padx=5)

        self.move_down_btn = CTkButton(self.hierarchy_tools_container, text="north", font=("MaterialIconsOutlined-Regular", 22), width=30, height=30, command=self.hierarchy.move_down)
        self.move_down_btn.pack(side="left", padx=5)

        self.delete_btn = CTkButton(self.hierarchy_tools_container, text="delete", font=("MaterialIconsOutlined-Regular", 22), width=30, height=30, command=self.hierarchy.delete_widget)
        self.delete_btn.pack(side="left", padx=5)

        self.duplicate_btn = CTkButton(self.hierarchy_tools_container, text="content_copy",
                                    font=("MaterialIconsOutlined-Regular", 22), width=30, height=30,
                                    command=self.hierarchy.duplicate_widget)
        self.duplicate_btn.pack(side="left", padx=5)

        self.change_parent_btn = CTkButton(self.hierarchy_tools_container, text="change_circle",
                                       font=("MaterialIconsOutlined-Regular", 22), width=30,
                                       height=30,
                                       command=self.hierarchy.change_parent)
        self.change_parent_btn.pack(side="left", padx=5)

        self.hierarchy.btns = [self.move_top_btn, self.move_down_btn, self.delete_btn, self.duplicate_btn, self.change_parent_btn]
        for btn in self.hierarchy.btns:
            btn.configure(state="disabled")

        self.properties_panel = PropertiesManager(self.container, main=self.main)
        self.properties_panel_resizer = WindowResizer(self.container, orientation="horizontal", multiplier=1, widget=self.hierarchy)
        self.properties_panel_resizer.pack(fill="x")

        self.main.properties = self.properties_panel
        self.properties_panel.pack(fill="both", expand=True)
        self.main_window.properties = self.properties_panel
        self.main_window.bind("<Button-1>", lambda e, nw=self.main_window: (nw.on_drag_start(None), self.hierarchy.set_current_selection(nw)))
        self.run_code_btn.configure(command=self.main.run_code)
        self.winfo_toplevel().bind_all('<KeyPress>', self.hotkey_manager)
        self.winfo_toplevel().bind("<Control-r>", lambda e: self.main.run_code)
        self.winfo_toplevel().bind('<Control-s>', lambda e: self.main.save_file)

        self.export_code_btn.configure(command=self.main.export_code)
        self.palette_btn.configure(command=lambda: self.main.show_palette(self.properties_panel))

        self.save_btn.configure(command=self.main.save_file)
        self.saveas_btn.configure(command=self.main.saveas_file)

        self.open_btn.configure(command=self.main.open_file)

        self.appearance_mode_switch.configure(command=lambda: self.main.change_appearance_mode(self.appearance_mode_switch.get()))
        #self.hierarchy.delete_children()
        #self.hierarchy.update_list(self.main.widgets, 5)
        self.home_btn.configure(command=lambda : self.on_closing(command=lambda: (self.master.deiconify(), self.destroy())))
        self.main.apply_theme_to_widget(self.main_window)

        self.toolbar = ToolBar(self, mainwindow=self.main, height=50, bg_color=self.main_window_panel.cget("fg_color"))
        self.toolbar.place(relx=0.5, rely=1, y=-50, anchor="s")
        self.main.change_appearance_mode(self.appearance_mode_switch.get())
        #self.create_component_btn.configure(command=self.main.create_component)
        self.wm_iconbitmap()
        self.iconpath = ImageTk.PhotoImage(file=resource_path('Logo.ico'))
        self.after(100, lambda: self.iconphoto(False, self.iconpath))



    def get_component(self):
        files = os.listdir("./customtkinterbuilder/Components")
        files.remove("__init__.py")
        files.remove("BaseComponent.py")
        try:
            files.remove("__pycache__")
        except Exception as e:
            pass

        classes = []
        for file in files:
            module_name = file.replace(".py", "")
            print(module_name)
            classname = eval(module_name)  # I know its dangerous
            classes.append(classname)
        return classes

    def hotkey_manager(self, event):
        key = event.keysym

        control = event.state & 0x4
        command = event.state & 0x8

        meta = control or command
        #print(key)
        if meta and key == 'r':
            self.main.run_code()
        elif meta and key == "s":
            self.main.save_file(suppress_dialog=True)
            self.message_box.show("File Saved")
        elif meta and key == "equal": # For +
            self.toolbar.zoomin()

        elif meta and key == "minus":
            self.toolbar.zoomout()
        elif meta and key == "0":
            self.toolbar.reset()
        elif meta and key == "e":
            self.main.export_code()


if __name__ == "__main__":
    set_default_color_theme("blue")
    app = App()
    app.mainloop()