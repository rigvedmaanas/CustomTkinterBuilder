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

        if current_dict[key_list[-1]] != {}:
            current_dict[key_list[-1]][value] = {}
        else:
            current_dict[key_list[-1]] = {value: {}}

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

    def update_list(self, d, pad):

        for x in list(d.keys()):
            if d[x] != {}:
                btn = CTkButton(self, text=x.type, command=lambda x=x: x.on_drag_start(None))
                btn.pack(fill="x", padx=(pad, 5), pady=2.5)
                self.update_list(d[x], pad+20)
            else:

                btn = CTkButton(self, text=x.type, command=lambda x=x: x.on_drag_start(None))
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

        self.main_window = CTkFrame(self.main_window_panel, width=500, height=500, fg_color="gray10")
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
        self.hierarchy.pack(fill="both", pady=(0, 10))
        self.main.hierarchy = self.hierarchy
        self.properties_panel = PropertiesManager(self.container, main=self.main)
        self.properties_panel.pack(fill="both", expand=True)

#set_default_color_theme("Extreme/extreme.json")
#set_appearance_mode("dark")
app = App()
app.mainloop()