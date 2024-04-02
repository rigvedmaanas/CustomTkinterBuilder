from properties import PropertiesManager
from customtkinter import *
from widgets import *
from dragndrop import DragManager
from Widgets.Button import Button
from Widgets.Label import Label
from Widgets.Frame import Frame
from Widgets.Entry import Entry


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

    def get_parents(self, widget):
        if widget == self.r:
            self._parents.reverse()
            pass
        else:
            self._parents.append(widget.master)
            self.get_parents(widget.master)

    def redraw(self, d):
        for x in list(d.keys()):
            print(x)
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
        #print(self.widgets)
        #print(widget.master, new_widget)
        self.get_parents(new_widget)
        self.add_to_dict(self.widgets, self._parents, new_widget)

        self._parents = []
        new_widget.pack(padx=(0, 0), pady=(0, 0))
        new_widget.configure(bg_color=widget.master.cget("fg_color"))
        self.hierarchy.delete_children()
        self.hierarchy.update_list(self.widgets, 5)
        #new_widget.place(x=x, y=y)
        self.drag_manager.update_children(children=widget.master.winfo_children())



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

    def set_current_selection(self, btn, x):
        self.current_selection = btn
        self.widget = x

        for child in self.winfo_children():
            if child != self.current_selection:
                child.configure(fg_color="#113D5F")
            else:
                child.configure(fg_color="#1F6AA5")


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
                print(self.main.widgets, "Last")
                self.delete_children()
                self.update_list(self.main.widgets, 5)

            self.main._parents = []
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
                print(self.main.widgets, "Last")
                self.delete_children()
                self.update_list(self.main.widgets, 5)

            self.main._parents = []


    def update_list(self, d, pad):
        self.current_selection = None
        self.widget = None
        for x in list(d.keys()):
            if d[x] != {}:
                btn = CTkButton(self, text=x.get_name(), fg_color="#113D5F")
                btn.configure(command=lambda x=x, btn=btn: (x.on_drag_start(None), self.set_current_selection(btn, x)))
                btn.pack(fill="x", padx=(pad, 5), pady=2.5)
                self.update_list(d[x], pad+20)
            else:

                btn = CTkButton(self, text=x.get_name(), fg_color="#113D5F")
                btn.configure(command=lambda x=x, btn=btn: (x.on_drag_start(None), self.set_current_selection(btn, x)))

                btn.pack(fill="x", padx=(pad, 5), pady=2.5)


    def delete_children(self):
        for widget in self.winfo_children():
            widget.destroy()


class App(CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.geometry("1900x1000+10+0")
        self.title("Custom Tkinter Designer")
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
        self.main_window = Frame(self.main_window_panel, width=500, height=500, fg_color="gray10", properties=None)
        self.main_window.pack_propagate(False)
        self.main_window.place(anchor="center", relx=0.5, rely=0.5)
        self.main_window.type = "MAIN"


        self.drag_manager = DragManager([self.add_frame_btn, self.add_button_btn, self.add_entry_btn, self.add_label_btn], self.main_window, self)
        self.main = MainWindow(self.main_window)
        self.main.drag_manager = self.drag_manager
        #print(self.main_window, self.main_window_panel)
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
        self.move_top_btn.pack(side="left", padx=10)

        self.move_down_btn = CTkButton(self.hierarchy_tools_container, text="⌄", width=30, height=30, command=self.hierarchy.move_down)
        self.move_down_btn.pack(side="left", padx=10)


        self.properties_panel = PropertiesManager(self.container, main=self.main)
        self.properties_panel.pack(fill="both", expand=True)
        self.main_window.properties = self.properties_panel

#set_default_color_theme("Extreme/extreme.json")
#set_appearance_mode("dark")
app = App()
app.mainloop()