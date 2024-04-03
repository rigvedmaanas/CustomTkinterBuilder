from properties import PropertiesManager
from tkinter.filedialog import asksaveasfilename
from customtkinter import *
from widgets import *
from dragndrop import DragManager
from Widgets.Button import Button
from Widgets.Label import Label
from Widgets.Frame import Frame
from Widgets.Entry import Entry
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

    def run_code(self):

        code = CodeGenerator(indentation="\t")
        code.add_line(f"""
# from customtkinter import *


root = CTkToplevel()
root.title("CTk Window")
root.geometry("{self.r.cget('width')}x{self.r.cget('height')}")
root.configure(fg_color=["gray95", "gray10"])
""")
        self.loop_generate(d=self.widgets[self.r], parent="root", code=code)
        #code.add_line("root.mainloop()")
        print(code.get_code())
        # I know this is not that safe. Do create an issue if there are any safer ways to do this
        exec(code.get_code())

    def export(self, code):
        filename = asksaveasfilename(filetypes=[(".py", "py")])
        if filename != "":
            with open(filename, "w") as f:
                f.write(code)


    def export_code(self):
        code = CodeGenerator(indentation="\t")
        code.add_line(f"""
from customtkinter import *


root = CTk()
root.title("CTk Window")
root.geometry("{self.r.cget('width')}x{self.r.cget('height')}")
root.configure(fg_color=["gray95", "gray10"])
""")
        self.loop_generate(d=self.widgets[self.r], parent="root", code=code)
        code.add_line("root.mainloop()")

        top = CTkToplevel()
        top.geometry("1000x800+500+100")
        top.title("Export Code")
        top.configure(fg_color=["gray95", "gray10"])


        codeviewer = CTkCodeViewer.CTkCodeViewer(top, code=code.get_code(), language="python", theme="monokai", font=CTkFont(size=20))
        codeviewer.pack(expand=True, fill="both", padx=20, pady=20)

        exp_btn = CTkButton(top, text="Export Code", command=lambda code=code: self.export(code.get_code()))
        exp_btn.pack(side="right", padx=20, pady=(0, 20))



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
                    if key in ["font_family", "font_size", "font_weight", "font_slant", "font_underline",
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
        self.get_parents(new_widget)
        self.add_to_dict(self.widgets, self._parents, new_widget)

        self._parents = []
        new_widget.pack(padx=(0, 0), pady=(0, 0))
        new_widget.configure(bg_color=widget.master.cget("fg_color"))
        new_widget.bind("<Button-1>", new_widget.on_drag_start)

        self.hierarchy.delete_children()
        self.hierarchy.update_list(self.widgets, 5)
        #new_widget.place(x=x, y=y)
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

    def set_current_selection(self, btn, x):
        for b in self.btns:
            b.configure(state="normal")

        self.current_selection = btn
        self.widget = x

        for child in self.winfo_children():

            if child != self.current_selection:
                child.configure(fg_color="#113D5F")
            else:
                child.configure(fg_color="#1F6AA5")

    def clone_widget(self, widget=None, master=None):
        # Code Snippet from https://stackoverflow.com/questions/46505982/is-there-a-way-to-clone-a-tkinter-widget. Thanks :)
        # Changes Made Suitably
        """
        Create a cloned version o a widget



        Returns
        -------
        cloned : tkinter widget
            Clone of input widget onto master widget.

        """
        # Get main info

        if widget is None:
            widget = self.widget

        parent = master if master else widget.master
        cls = widget.__class__

        # Clone the widget configuration
        cfg = {}

        for key in widget.props:
            if key in ["font_family", "font_size", "font_weight", "font_slant", "font_underline", "font_overstrike"]:
                cfg["font"] = widget.cget("font")
            else:
                cfg[key] = widget.cget(key)

        cloned = cls(parent, **cfg, properties=self.mainwindow.properties)
        cloned.configure(bg_color=cloned.master.cget("fg_color"))
        self.main._parents = []
        self.main.get_parents(self.widget)
        self.main.add_to_dict(self.main.widgets, self.main._parents, cloned)
        self.main._parents = []
        self.widget = None
        self.current_selection = None
        self.delete_children()
        self.update_list(self.main.widgets, 5)
        self.main.redraw(self.main.widgets[self.main.r])
        for btn in self.btns:
            btn.configure(state="disabled")
        print(self.main.widgets)

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
                x.bind("<Button-1>", lambda e, x=x, btn=btn: (x.on_drag_start(None), self.set_current_selection(btn, x)))
                btn.configure(command=lambda x=x, btn=btn: (x.on_drag_start(None), self.set_current_selection(btn, x)))
                btn.pack(fill="x", padx=(pad, 5), pady=2.5)
                self.update_list(d[x], pad+20)
            else:

                btn = CTkButton(self, text=x.get_name(), fg_color="#113D5F")
                x.bind("<Button-1>", lambda e, x=x, btn=btn: (x.on_drag_start(None), self.set_current_selection(btn, x)))
                btn.configure(command=lambda x=x, btn=btn: (x.on_drag_start(None), self.set_current_selection(btn, x)))

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
        self.main_window_panel = CTkFrame(self)
        self.main_window_panel.pack(side=LEFT, pady=10, fill="both", expand=True)


        # Need to create a seperate Class for main. This is just for now
        self.main_window = Frame(self.main_window_panel, width=500, height=500, fg_color=["gray95", "gray10"], properties=None)
        self.main_window.pack_propagate(False)
        self.main_window.place(anchor="center", relx=0.5, rely=0.5)
        self.main_window.type = "MAIN"


        self.drag_manager = DragManager([self.add_frame_btn, self.add_button_btn, self.add_entry_btn, self.add_label_btn], self.main_window, self)
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

        self.dup_btn = CTkButton(self.hierarchy_tools_container, text="", image=CTkImage(Image.open("Icons/duplicate.png")), width=30, height=30, command=self.hierarchy.clone_widget)
        self.dup_btn.pack(side="left", padx=5)

        self.hierarchy.btns = [self.move_top_btn, self.move_down_btn, self.delete_btn, self.dup_btn]
        for btn in self.hierarchy.btns:
            btn.configure(state="disabled")
        self.properties_panel = PropertiesManager(self.container, main=self.main)
        self.properties_panel.pack(fill="both", expand=True)
        self.main_window.properties = self.properties_panel

        self.run_code_btn.configure(command=self.main.run_code)
        self.export_code_btn.configure(command=self.main.export_code)


#set_default_color_theme("Extreme/extreme.json")
#set_appearance_mode("dark")
app = App()
app.mainloop()