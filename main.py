import json
from properties import PropertiesManager
from tkinter.filedialog import asksaveasfilename, askopenfilename
from customtkinter import *
from widgets import *
from dragndrop import DragManager
from Widgets.Button import Button
from Widgets.Label import Label
from Widgets.Frame import Frame
from Widgets.Entry import Entry
from Widgets.Switch import Switch
from Widgets.TextBox import TextBox
from Widgets.ProgressBar import ProgressBar
from Widgets.SegmentedButton import SegmentedButton
from CodeGenerator import CodeGenerator
from CustomtkinterCodeViewer import CTkCodeViewer

class MainWindow:
    def __init__(self, root):
        self.type = "ROOT"
        self.widgets = {}
        self.hierarchy = None
        self.r = root
        self.widgets[root] = {}
        self.drag_manager = None
        self._parents = []
        self.temp_widgets = {}
        self.file = ""
        self.total_num = 0

    def run_code(self):

        code = CodeGenerator(indentation="\t")
        code.add_line(f"""
root = CTkToplevel()
root.title("CTk Window")
root.geometry("{self.r.cget('width')}x{self.r.cget('height')}")

""")
        self.loop_generate(d=self.widgets[self.r], parent="root", code=code)
        print(code.get_code())
        # I know this is not that safe. Do create an issue if there are any safer ways to do this
        exec(code.get_code())

    def export(self, code):
        filename = asksaveasfilename(filetypes=[(".py", "py")])
        if filename != "":
            with open(filename, "w") as f:
                f.write(code)


    def export_code(self):
        code = CodeGenerator(indentation="    ")
        code.add_line(f"""
from customtkinter import *
from PIL import Image

root = CTk()
root.title("CTk Window")
root.geometry("{self.r.cget('width')}x{self.r.cget('height')}")

""")
        self.loop_generate(d=self.widgets[self.r], parent="root", code=code)
        code.add_line("root.mainloop()")

        oop_code = CodeGenerator(indentation="    ")
        oop_code.add_line("""
from customtkinter import *
from PIL import Image

class Root(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
""")
        oop_code.indent()
        oop_code.indent()
        self.loop_generate_oop(d=self.widgets[self.r], parent="self", code=oop_code)
        oop_code.add_line("""
app = App()
app.mainloop()
            """)

        top = CTkToplevel()
        top.geometry("1000x800+500+100")
        top.title("Export Code")
        top.configure(fg_color=["gray95", "gray10"])

        self.codeviewer = CTkCodeViewer.CTkCodeViewer(top, code=oop_code.get_code(), language="python", theme="monokai", font=CTkFont(size=20))
        self.codeviewer.configure(wrap="none")
        self.codeviewer.pack(expand=True, fill="both", padx=20, pady=20)

        self.oop_code_switch = CTkSwitch(top, text="OOP Code", command=self.change_oop)
        self.oop_code_switch.pack(side="left", padx=20, pady=(0, 20))
        self.oop_code_switch.select()

        exp_btn = CTkButton(top, text="Export Code", command=lambda: self.export(self.current.get_code()))
        exp_btn.pack(side="right", padx=20, pady=(0, 20))

        self.current = oop_code
        self.not_current = code

    def change_oop(self):

        if self.oop_code_switch.get() == 0:
            code = self.not_current
            oop_code = self.current
            self.current = code
            self.not_current = oop_code

        else:
            oop_code = self.not_current
            code = self.current
            self.current = oop_code
            self.not_current = code
        self.codeviewer.delete(1.0, "end")
        self.codeviewer._add_code(self.current.get_code(), "python")

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

    def loop_generate(self, d, parent, code):
        for x in list(d.keys()):
            if x.props == {}:
                code.add_line(f"{x.get_name()} = {x.get_class()}(master={parent})")
                if x.type == "FRAME":
                    code.add_line(f"{x.get_name()}.pack_propagate(False)")
            else:
                p = ""
                font = "font=CTkFont("
                for key in list(x.props.keys()):
                    if key == "image" and x.props["image"] != None:
                        p += f'image=CTkImage(Image.open("{x.props["image"].cget("dark_image").filename}"), size=({x.props["image"].cget("size")[0]}, {x.props["image"].cget("size")[1]})), '
                    elif key in ["font_family", "font_size", "font_weight", "font_slant", "font_underline",
                               "font_overstrike"]:
                        if type(x.props[key]) == str:

                            font += f'{key[5::]}="{x.props[key]}", '
                        else:
                            font += f'{key[5::]}={x.props[key]}, '
                    else:
                        if type(x.props[key]) == str:
                            k = self.escape_special_chars(x.props[key])
                            p += f'{key}="{k}", '
                        elif type(x.props[key]) == tuple:
                            if type(x.props[key][0]) == str and type(x.props[key][1]) == str:
                                p += f'{key}=("{x.props[key][0]}", "{x.props[key][1]}"), '
                            else:
                                p += f"{key}=({x.props[key][0]}, {x.props[key][1]}), "
                        else:
                            p += f"{key}={x.props[key]}, "

                font = font[0:-2] # Delete ', ' at last part
                font += ")"
                print(font)
                if font != "font=CTkFon)": # Which means there is no change in font
                    p += font
                else:
                    p = p[0:-2]
                code.add_line(f"{x.get_name()} = {x.get_class()}(master={parent}, {p})")
                if x.type == "FRAME":
                    code.add_line(f"{x.get_name()}.pack_propagate(False)")
            if x.pack_options == {}:
                code.add_line(f"{x.get_name()}.pack()")
            else:
                p = ""
                for key in list(x.pack_options.keys()):
                    if type(x.pack_options[key]) == str:
                        p += f'{key}="{x.pack_options[key]}", '
                    elif type(x.pack_options[key]) == tuple:
                        if type(x.pack_options[key][0]) == str and type(x.pack_options[key][1]) == str:
                            p += f'{key}=("{x.pack_options[key][0]}", "{x.pack_options[key][1]}"), '
                        else:
                            p += f"{key}=({x.pack_options[key][0]}, {x.pack_options[key][1]}), "
                    else:
                        p += f"{key}={x.pack_options[key]}, "

                p = p[0:-2]  # Delete ', ' at last part
                code.add_line(f"{x.get_name()}.pack({p})")
            if d[x] != {}:
                #btn = CTkButton(self, text=x.type, command=lambda x=x: x.on_drag_start(None))

                self.loop_generate(d=d[x], parent=x.get_name(), code=code)

    def open_file(self):
        file = askopenfilename(filetypes=[(".json", "json")])
        if file != "":
            with open(file, 'r') as openfile:
                d = json.load(openfile)
            d = d["MAIN-1"]
            d.pop("TYPE")
            d.pop("parameters")
            d.pop("pack_options")

            self.loop_open(d, self.r)

    def loop_open(self, d, parent):
        # I could destroy every child in self.r but could not add new widgets after destroying the children.
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
            elif y == "ENTRY":
                w = Entry
            elif y == "MAIN":
                w = Frame # I should create a new one for MAIN
            elif y == "TEXTBOX":
                w = TextBox
            elif y == "PROGRESSBAR":
                w = ProgressBar
            elif y == "SEGMENTEDBUTTON":
                w = SegmentedButton
            else:
                raise ModuleNotFoundError(f"The Widget is not available. Perhaps the file is edited. The unknown widget was {x}")

            f = CTkFont()
            i = None
            d_copy = dict(d[x]["parameters"])
            for p in dict(d[x]["parameters"]):
                if p == "image":
                    i = CTkImage(light_image=Image.open(d[x]["parameters"]["image"]["image"]), dark_image=Image.open(d[x]["parameters"]["image"]["image"]), size=(d[x]["parameters"]["image"]["size"][0], d[x]["parameters"]["image"]["size"][1]))
                    d[x]["parameters"]["image"] = i

                elif p == "font_family":
                    print(d[x], p)
                    f.configure(family=d[x]["parameters"][p])
                    d[x]["parameters"].pop("font_family")
                    d[x]["parameters"]["font"] = f
                elif p == "font_size":
                    f.configure(size=d[x]["parameters"][p])
                    d[x]["parameters"].pop("font_size")
                    d[x]["parameters"]["font"] = f
                elif p == "font_weight":
                    f.configure(weight=d[x]["parameters"][p])
                    d[x]["parameters"].pop("font_weight")
                    d[x]["parameters"]["font"] = f
                elif p == "font_slant":
                    f.configure(slant=d[x]["parameters"][p])
                    d[x]["parameters"].pop("font_slant")
                    d[x]["parameters"]["font"] = f
                elif p == "font_underline":
                    f.configure(underline=d[x]["parameters"][p])
                    d[x]["parameters"].pop("font_underline")
                    d[x]["parameters"]["font"] = f
                elif p == "font_overstrike":
                    f.configure(overstrike=d[x]["parameters"][p])
                    d[x]["parameters"].pop("font_overstrike")
                    d[x]["parameters"]["font"] = f
            try:
                print(d[x]["parameters"]["font"].cget("size"))
            except Exception as e:
                print(e)
            #print(w, parent.get_name(), d[x]["parameters"])
            if d[x]["parameters"] != {}:
                new_widget = w(master=parent, **d[x]["parameters"], properties=self.r.properties)
                try:
                    print(d_copy)
                    new_widget.image = d_copy["image"]["image"]
                    img = d[x]["parameters"]["image"]
                    d_copy["image"] = img
                    new_widget.size = (d[x]["parameters"]["image"].cget("size")[0], d[x]["parameters"]["image"].cget("size")[1])
                    print(d_copy)
                except KeyError as e:
                    pass

                new_widget.props = d_copy

            else:
                new_widget = w(master=parent, properties=self.r.properties)


            new_widget.num = self.total_num
            new_widget.name = x

            self.total_num += 1
            self.get_parents(new_widget)
            self.add_to_dict(self.widgets, self._parents, new_widget)

            self._parents = []
            new_widget.pack(**d[x]["pack_options"])
            new_widget.pack_options = d[x]["pack_options"]
            #new_widget.configure(bg_color=parent.cget("fg_color"))
            if new_widget.__class__ == SegmentedButton:
                new_widget.configure(command=lambda e, nw=new_widget: (nw.on_drag_start(None), self.hierarchy.set_current_selection(nw)))
            else:
                new_widget.bind("<Button-1>", lambda e, nw=new_widget: (nw.on_drag_start(None), self.hierarchy.set_current_selection(nw)))

            # new_widget.bind("<Button-1>", new_widget.on_drag_start)

            self.hierarchy.delete_children()
            self.hierarchy.update_list(self.widgets, 5)
            # new_widget.place(x=x, y=y)
            if new_widget.__class__ != SegmentedButton:
                self.drag_manager.update_children(children=parent.winfo_children())
            d[x].pop("TYPE")
            d[x].pop("pack_options")
            d[x].pop("parameters")

            if d[x] != {}:
                self.loop_open(d[x], new_widget)

    def save_file(self):
        self.s = {self.r.get_name(): {}}
        self.loop_save(self.widgets, self.r.get_name(), self.s)
        self.s = self.s[self.r.get_name()]
        print(self.s)
        if self.file == "":
            f = asksaveasfilename(filetypes=[(".json", "json")])
            if f != "":
                self.file = f
                json_object = json.dumps(self.s, indent=4)
                with open(f, "w") as outfile:
                    outfile.write(json_object)
        if self.file != "":
            json_object = json.dumps(self.s, indent=4)
            with open(self.file, "w") as outfile:
                outfile.write(json_object)
    def saveas_file(self):
        self.s = {self.r.get_name(): {}}
        self.loop_save(self.widgets, self.r.get_name(), self.s)
        self.s = self.s[self.r.get_name()]
        print(self.s)
        f = asksaveasfilename(filetypes=[(".json", "json")])
        if f != "":
            json_object = json.dumps(self.s, indent=4)
            with open(f, "w") as outfile:
                outfile.write(json_object)

    def loop_save(self, d, parent, code):
        print(d)
        for x in list(d.keys()):
            props = dict(x.props)
            if "image" in list(props.keys()):
                print(x.get_name(), x.props)
                props["image"] = {"image": str(x.props["image"].cget("dark_image").filename), "size": [x.size[0], x.size[1]]}

            code[parent][x.get_name()] = {"TYPE": x.type, "parameters": props, "pack_options": x.pack_options}

            if d[x] != {}:
                self.loop_save(d[x], x.get_name(), code[parent])

        print(code)

    def loop_generate_oop(self, d, parent, code):

        for x in list(d.keys()):
            if x.props == {}:

                code.add_line(f"self.{x.get_name()} = {x.get_class()}(master={parent})")
                if x.type == "FRAME":
                    code.add_line(f"self.{x.get_name()}.pack_propagate(False)")
            else:


                p = ""
                font = "font=CTkFont("
                for key in list(x.props.keys()):
                    if key == "image" and x.props["image"] != None:
                        p += f'image=CTkImage(Image.open("{x.props["image"].cget("dark_image").filename}"), size=({x.props["image"].cget("size")[0]}, {x.props["image"].cget("size")[1]})), '
                    elif key in ["font_family", "font_size", "font_weight", "font_slant", "font_underline",
                               "font_overstrike"]:
                        if type(x.props[key]) == str:

                            font += f'{key[5::]}="{x.props[key]}", '
                        else:
                            font += f'{key[5::]}={x.props[key]}, '
                    else:
                        if type(x.props[key]) == str:
                            k = self.escape_special_chars(x.props[key])
                            p += f'{key}="{k}", '
                        elif type(x.props[key]) == tuple:
                            if type(x.props[key][0]) == str and type(x.props[key][1]) == str:
                                p += f'{key}=("{x.props[key][0]}", "{x.props[key][1]}"), '
                            else:
                                p += f"{key}=({x.props[key][0]}, {x.props[key][1]}), "
                        else:
                            p += f"{key}={x.props[key]}, "

                font = font[0:-2] # Delete ', ' at last part
                font += ")"
                print(font)
                if font != "font=CTkFon)": # Which means there is no change in font
                    p += font
                else:
                    p = p[0:-2]
                code.add_line(f"self.{x.get_name()} = {x.get_class()}(master={parent}, {p})")
                if x.type == "FRAME":
                    code.add_line(f"self.{x.get_name()}.pack_propagate(False)")
            if x.pack_options == {}:
                code.add_line(f"self.{x.get_name()}.pack()")
            else:
                p = ""
                for key in list(x.pack_options.keys()):
                    if type(x.pack_options[key]) == str:
                        p += f'{key}="{x.pack_options[key]}", '
                    elif type(x.pack_options[key]) == tuple:
                        if type(x.pack_options[key][0]) == str and type(x.pack_options[key][1]) == str:
                            p += f'{key}=("{x.pack_options[key][0]}", "{x.pack_options[key][1]}"), '
                        else:
                            p += f"{key}=({x.pack_options[key][0]}, {x.pack_options[key][1]}), "
                    else:
                        p += f"{key}={x.pack_options[key]}, "

                p = p[0:-2]  # Delete ', ' at last part
                code.add_line(f"self.{x.get_name()}.pack({p})")
            if d[x] != {}:
                #btn = CTkButton(self, text=x.type, command=lambda x=x: x.on_drag_start(None))

                self.loop_generate_oop(d=d[x], parent="self." + x.get_name(), code=code)


    def get_parents(self, widget):
        if widget == self.r:
            self._parents.reverse()
            pass
        else:
            self._parents.append(widget.master)
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

    def add_widget(self, w, properties, widget, x=0, y=0):

        new_widget = w(master=widget.master, **properties)
        new_widget.num = self.total_num
        new_widget.name = new_widget.type + str(new_widget.num)

        self.total_num += 1
        self.get_parents(new_widget)
        self.add_to_dict(self.widgets, self._parents, new_widget)

        self._parents = []
        new_widget.pack(padx=(0, 0), pady=(0, 0))
        #new_widget.configure(bg_color=widget.master.cget("fg_color"))
        if new_widget.__class__ == SegmentedButton:
            new_widget.configure(command=lambda e, nw=new_widget: (nw.on_drag_start(None), self.hierarchy.set_current_selection(nw)))
        else:
            new_widget.bind("<Button-1>", lambda e, nw=new_widget: (nw.on_drag_start(None), self.hierarchy.set_current_selection(nw)))

        #new_widget.bind("<Button-1>", new_widget.on_drag_start)

        self.hierarchy.delete_children()
        self.hierarchy.update_list(self.widgets, 5)
        #new_widget.place(x=x, y=y)
        if new_widget.__class__ != SegmentedButton:
            self.drag_manager.update_children(children=widget.master.winfo_children())

    def delete_from_dict(self, my_dict, key_list, value):
        current_dict = my_dict
        for key in key_list[:-1]:  # Iterate through all keys except the last one

            current_dict = current_dict[key]  # Move to the nested dictionary

        # If the current dict is not empty (There something already there)
        if current_dict[key_list[-1]] != {}:
            current_dict[key_list[-1]].pop(value)



class WidgetButton(CTkButton):
    def __init__(self, on_drag, **kwargs):
        self.on_drag = on_drag
        super().__init__(**kwargs)


class Hierarchy(CTkScrollableFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_selection = None
        self.widget = None
        self.main = None
        self.mainwindow = None
        self.btns = []

    def set_current_selection(self, x):
        for b in self.btns:
            b.configure(state="normal")

        #self.current_selection = btn
        self.widget = x

        for child in self.winfo_children():

            if child.cget("text") != self.widget.get_name():
                child.configure(fg_color="#113D5F")
            else:
                self.current_selection = child
                child.configure(fg_color="#1F6AA5")

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
            self.widget = None
            for btn in self.btns:
                btn.configure(state="disabled")
            print(self.main.widgets)
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
            self.widget = None
            for btn in self.btns:
                btn.configure(state="disabled")
            print(self.main.widgets)

    def update_list(self, d, pad):
        self.current_selection = None
        self.widget = None
        for x in list(d.keys()):
            if d[x] != {}:
                btn = CTkButton(self, text=x.get_name(), fg_color="#113D5F")
                #x.bind("<Button-1>", lambda e, x=x, btn=btn: (x.on_drag_start(None), self.set_current_selection(btn, x)))
                btn.configure(command=lambda x=x: (x.on_drag_start(None), self.set_current_selection(x)))
                btn.widget = x
                btn.pack(fill="x", padx=(pad, 5), pady=2.5)
                self.update_list(d[x], pad+20)
            else:

                btn = CTkButton(self, text=x.get_name(), fg_color="#113D5F")
                #x.bind("<Button-1>", lambda e, x=x, btn=btn: (x.on_drag_start(None), self.set_current_selection(btn, x)))
                btn.configure(command=lambda x=x: (x.on_drag_start(None), self.set_current_selection(x)))
                btn.widget = x
                btn.pack(fill="x", padx=(pad, 5), pady=2.5)


    def delete_children(self):
        for widget in self.winfo_children():
            widget.destroy()


class App(CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.geometry("1900x1000+10+0")
        self.title("Custom Tkinter Builder")

        self.tool_bar = CTkFrame(self, height=40)
        self.tool_bar.pack(side="top", fill="x", padx=10, pady=(10, 0))

        self.save_btn = CTkButton(self.tool_bar, text="Save")
        self.save_btn.pack(side="left", padx=5, pady=5)

        self.saveas_btn = CTkButton(self.tool_bar, text="Save As")
        self.saveas_btn.pack(side="left", padx=5, pady=5)

        self.open_btn = CTkButton(self.tool_bar, text="Open")
        self.open_btn.pack(side="left", padx=5, pady=5)

        self.run_code_btn = CTkButton(self.tool_bar, text="Run Code")
        self.run_code_btn.pack(side="left", padx=5, pady=5)

        self.export_code_btn = CTkButton(self.tool_bar, text="Export Code")
        self.export_code_btn.pack(side="left", padx=5, pady=5)

        self.widget_panel = CTkScrollableFrame(self, width=350)
        self.widget_panel.pack(side=LEFT, padx=10, pady=10, fill="y")

        self.add_frame_btn = WidgetButton(master=self.widget_panel, text="CTk Frame", height=50,
                                          on_drag=lambda x, y, widget: self.main.add_widget(Frame, properties={"properties":self.properties_panel}, x=x, y=y, widget=widget))
        self.add_frame_btn.pack(padx=10, pady=(10, 0), fill="x")

        self.add_button_btn = WidgetButton(master=self.widget_panel, text="CTk Button", height=50, on_drag=lambda x, y, widget: self.main.add_widget(Button, properties={"properties":self.properties_panel}, x=x, y=y, widget=widget))
        self.add_button_btn.pack(padx=10, pady=(10, 0), fill="x")

        self.add_label_btn = WidgetButton(master=self.widget_panel, text="CTk Label", height=50, on_drag=lambda x, y, widget: self.main.add_widget(Label, properties={"properties":self.properties_panel}, x=x, y=y, widget=widget))
        self.add_label_btn.pack(padx=10, pady=(10, 0), fill="x")

        self.add_entry_btn = WidgetButton(master=self.widget_panel, text="CTk Entry", height=50,
                                          on_drag=lambda x, y, widget: self.main.add_widget(Entry, properties={"properties":self.properties_panel}, x=x, y=y, widget=widget))
        self.add_entry_btn.pack(padx=10, pady=(10, 0), fill="x")

        self.add_switch_btn = WidgetButton(master=self.widget_panel, text="CTk Switch", height=50,
                                          on_drag=lambda x, y, widget: self.main.add_widget(Switch, properties={
                                              "properties": self.properties_panel}, x=x, y=y, widget=widget))
        self.add_switch_btn.pack(padx=10, pady=(10, 0), fill="x")

        self.add_textbox_btn = WidgetButton(master=self.widget_panel, text="CTk TextBox", height=50,
                                          on_drag=lambda x, y, widget: self.main.add_widget(TextBox, properties={
                                              "properties": self.properties_panel}, x=x, y=y, widget=widget))
        self.add_textbox_btn.pack(padx=10, pady=(10, 0), fill="x")

        self.add_progressbar_btn = WidgetButton(master=self.widget_panel, text="CTk Progress Bar", height=50,
                                          on_drag=lambda x, y, widget: self.main.add_widget(ProgressBar, properties={
                                              "properties": self.properties_panel}, x=x, y=y, widget=widget))
        self.add_progressbar_btn.pack(padx=10, pady=(10, 0), fill="x")

        self.add_segmentedbutton_btn = WidgetButton(master=self.widget_panel, text="CTk Segmented Button", height=50,
                                               on_drag=lambda x, y, widget: self.main.add_widget(SegmentedButton,
                                                                                                 properties={
                                                                                                     "properties": self.properties_panel},
                                                                                                 x=x, y=y,
                                                                                                 widget=widget))
        self.add_segmentedbutton_btn.pack(padx=10, pady=(10, 0), fill="x")

        self.main_window_panel = CTkFrame(self)
        self.main_window_panel.pack(side=LEFT, pady=10, fill="both", expand=True)

        self.temp = CTkFrame(self.main_window_panel)
        self.temp.pack(fill="both", expand=True)


        # Need to create a seperate Class for main. This is just for now
        self.main_window = Frame(self.temp, width=500, height=500, properties=None, fg_color=["gray92", "gray14"])
        self.main_window.pack_propagate(False)
        self.main_window.place(anchor="center", relx=0.5, rely=0.5)
        self.main_window.type = "MAIN"
        self.main_window.num = -1
        self.main_window.name = self.main_window.type + str(self.main_window.num)


        self.drag_manager = DragManager([self.add_frame_btn, self.add_button_btn, self.add_entry_btn, self.add_label_btn, self.add_switch_btn, self.add_textbox_btn, self.add_progressbar_btn, self.add_segmentedbutton_btn], self.main_window, self)
        self.main = MainWindow(self.main_window)
        self.main.drag_manager = self.drag_manager

        self.container = CTkFrame(self, width=350)
        self.container.pack(side=LEFT, padx=10, pady=10, fill="y")
        self.container.pack_propagate(False)

        self.hierarchy = Hierarchy(self.container, height=350)
        self.hierarchy.pack(fill="both")
        self.main.hierarchy = self.hierarchy
        self.hierarchy.main = self.main
        self.hierarchy.mainwindow = self.main_window
        self.hierarchy_tools_container = CTkFrame(self.container, height=40)
        self.hierarchy_tools_container.pack(fill="x", pady=(0, 10))

        # Need to change those unicode with icons
        self.move_top_btn = CTkButton(self.hierarchy_tools_container, text="^", width=30, height=30, command=self.hierarchy.move_up)
        self.move_top_btn.pack(side="left", padx=5)

        self.move_down_btn = CTkButton(self.hierarchy_tools_container, text="⌄", width=30, height=30, command=self.hierarchy.move_down)
        self.move_down_btn.pack(side="left", padx=5)

        self.delete_btn = CTkButton(self.hierarchy_tools_container, text="", image=CTkImage(Image.open("Icons/waste.png")), width=30, height=30, command=self.hierarchy.delete_widget)
        self.delete_btn.pack(side="left", padx=5)

        self.hierarchy.btns = [self.move_top_btn, self.move_down_btn, self.delete_btn]
        for btn in self.hierarchy.btns:
            btn.configure(state="disabled")
        self.properties_panel = PropertiesManager(self.container, main=self.main)
        self.properties_panel.pack(fill="both", expand=True)
        self.main_window.properties = self.properties_panel

        self.run_code_btn.configure(command=self.main.run_code)
        self.export_code_btn.configure(command=self.main.export_code)
        self.save_btn.configure(command=self.main.save_file)
        self.saveas_btn.configure(command=self.main.saveas_file)

        self.open_btn.configure(command=self.main.open_file)



# Need to create a custom theme with corner_radius - 3 (Will look more elegant and professional)
set_default_color_theme("blue")
#set_appearance_mode("dark")
app = App()
app.mainloop()