from customtkinter import CTkLabel
from icecream import ic

from .Widgets.SegmentedButton import SegmentedButton
from .Widgets.ScrollableFrame import ScrollableFrame


class DragManager:
    def __init__(self, buttons, window, root):
        self.add_buttons = buttons
        self.main_window = window
        self.root = root
        for btn in self.add_buttons:

            btn.bind("<Button-1>", lambda e, btn=btn: self.pressed(btn.cget("text")))
            btn.bind("<B1-Motion>", self.dragged)
            btn.bind("<ButtonRelease>", lambda e, btn=btn: self.released(btn.on_drag))
        self.onTop = False
        self.called_widget = None
        self.main_x = -1000
        self.main_y = -1000
        self.main_window.bind("<Enter>", lambda e: self.set_on_top(True, e.widget))
        self.main_window.bind("<Leave>", lambda e: self.set_on_top(False, e.widget))
        for w in self.main_window.winfo_children():
            w.bind("<Enter>", lambda e: self.set_on_top(True, e.widget))
            w.bind("<Leave>", lambda e: self.set_on_top(False, e.widget))

    def update_children(self, children):

        for w in children:

            if w.__class__ == SegmentedButton:
                pass

            elif w.__class__ == ScrollableFrame:
                ic("Found", w)
                w.scrollwindow.bind("<Enter>", lambda e, w=w: self.set_on_top(True, w.scrollwindow))
                w.scrollwindow.bind("<Leave>", lambda e, w=w: self.set_on_top(False, w.scrollwindow))
                w.canv.bind("<Enter>", lambda e, w=w: self.set_on_top(True, w.scrollwindow))
                w.canv.bind("<Leave>", lambda e, w=w: self.set_on_top(False, w.scrollwindow))
                #w.scrollwindow.bind("<Enter>", print)
                #w.scrollwindow.bind("<Leave>", print)


            else:
                w.bind("<Enter>", lambda e: self.set_on_top(True, e.widget))
                w.bind("<Leave>", lambda e: self.set_on_top(False, e.widget))




    def set_on_top(self, state, widget):
        self.onTop = state
        self.called_widget = widget


    def pressed(self, e):
        self.tip = CTkLabel(self.root, text=e)
        abs_coord_x = self.root.winfo_pointerx() - self.root.winfo_rootx() + 10
        abs_coord_y = self.root.winfo_pointery() - self.root.winfo_rooty() + 10
        self.tip.place(x=abs_coord_x, y=abs_coord_y)

    def dragged(self, e):
        abs_coord_x = self.root.winfo_pointerx() - self.root.winfo_rootx() + 10
        abs_coord_y = self.root.winfo_pointery() - self.root.winfo_rooty() + 10
        self.tip.place(x=abs_coord_x, y=abs_coord_y)


    def check_add(self, e):
        if self.onTop:

            abs_coord_x = self.main_window.winfo_pointerx() - self.main_window.winfo_rootx() + 10
            abs_coord_y = self.main_window.winfo_pointery() - self.main_window.winfo_rooty() + 10
            ##print(abs_coord_x, abs_coord_y, self.called_widget.master)
            #print(self.called_widget)
            e(x=abs_coord_x, y=abs_coord_y, widget=self.called_widget)
    def released(self, e):
        try:
            self.tip.destroy()
            self.root.after(10, lambda: self.check_add(e)) # I had to add this due to some awkward issue. The enter event was not firing

        except Exception as e:
            pass
            #print(e)
        ##print(self.root, self.main_window)
        #for widget in self.main_window.winfo_children():
        #    #print(widget)
