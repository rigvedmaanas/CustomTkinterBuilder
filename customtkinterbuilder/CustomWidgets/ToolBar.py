from customtkinter import *
from PIL import Image
import time

class ToolBar(CTkFrame):
    def __init__(self, master, mainwindow, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.main = mainwindow
        self.zoom_properties_toggled = False
        self.zoom = IntVar(self, 100)
        self.zoom.trace("w", self._on_zoom_change)
        self.zoom_amt = 10
        self.current_tool = "select"
        self.time_interval = 0.01
        self.prev_time = 0

        image_path = "customtkinterbuilder/Assets/select_tool.png"
        self.select_tool_image = CTkImage(
            light_image=Image.open(image_path),
            dark_image=Image.open(image_path),
            size=(20, 20)
        )

        self.select_tool = CTkButton(self, text="", width=50, image=self.select_tool_image)
        self.select_tool.pack(side="left", padx=(10, 0), pady=10)

        image_path = "customtkinterbuilder/Assets/move_tool.png"
        self.move_tool_image = CTkImage(
            light_image=Image.open(image_path),
            dark_image=Image.open(image_path),
            size=(20, 20)
        )

        self.move_tool = CTkButton(self, text="", width=50, image=self.move_tool_image, command=self.change_current_tool)
        #self.move_tool.pack(side="left", padx=(10, 0), pady=10)

        image_path = "customtkinterbuilder/Assets/Arrow_down.png"
        self.zoom_tool_image = CTkImage(
            light_image=Image.open(image_path),
            dark_image=Image.open(image_path),
            size=(20, 20)
        )


        self.zoom_tool = CTkButton(self, text=f"{self.zoom.get()}%", command=self.toggle_zoom_properties, width=80,
                                   image=self.zoom_tool_image, compound="right")
        self.zoom_tool.pack(side="left", padx=(10, 10), pady=10)

        if self.current_tool == "select":
            self.move_tool.configure(fg_color="transparent")
            self.select_tool.configure(fg_color="#1D1D1D")

        #self.main.drag_frame.bind('<ButtonPress-1>', self.click, add=True)
        #self.main.drag_frame.bind('<ButtonRelease-1>', self.release, add=True)
        #self.main.drag_frame.bind("<B1-Motion>", self.drag, add=True)

    def click(self, e):
        if self.current_tool == "move":
            self.prev_time = time.time()
            self.x = e.x_root
            self.y = e.y_root
            self.x_original = self.main.r.winfo_x()
            self.y_original = self.main.r.winfo_y()
            print("Called")



    def release(self, e):
        if self.current_tool == "move":
            self.x = None
            self.y = None
            self.x_original = None
            self.y_original = None

    def drag(self, e):
        if self.current_tool == "move" and self.x is not None and self.y is not None:
            # Setting up a debouncer so that it doesn't crash due to recursive function calling
            if time.time() - self.prev_time > self.time_interval:
                # 0, 0 is center. How????????????????????????????

                #self.prev_time = time.time()
                #print((self.x_original, (self.x , e.x_root), self.x_original + (e.x_root - self.x ), self.y_original , (self.y , e.y_root)),  self.y_original + (e.y_root - self.y))
                #self.main.move_delta(self.x_original + (e.x_root - self.x ), self.y_original + (e.y_root - self.y))
                self.main.move_delta((e.x_root - self.x ), (e.y_root - self.y))
                self.update_idletasks()
            else:
                self.click()


    def change_current_tool(self):
        if self.current_tool == "select":
            self.current_tool = "move"
            self.move_tool.configure(fg_color="#1D1D1D")
            self.select_tool.configure(fg_color="transparent")
        else:
            self.current_tool = "select"
            self.select_tool.configure(fg_color="#1D1D1D")
            self.move_tool.configure(fg_color="transparent")

    def _on_zoom_change(self, *args):
        new_zoom_value = self.zoom.get()
        self.zoom_tool.configure(text=f"{new_zoom_value}%")
        self.main.change_scale(new_zoom_value / 100)

    def show_zoom_properties(self):
        if self.zoom_properties_toggled:
            return


        self.zoom_properties_toggled = True
        self.zoom_properties = CTkFrame(master=self.winfo_toplevel(), bg_color=self.cget("bg_color"))

        self.zoom_properties.pack_propagate(False)
        self.zoom_properties.configure(width=150, height=120)

        self.zoom_properties.place_forget()

        self.zoom_in = CTkButton(self.zoom_properties, text="Zoom In",
                                 command=lambda : self.zoom.set(self.zoom.get() + self.zoom_amt),
                                 fg_color="transparent", anchor="w")
        self.zoom_in.pack(fill="x", pady=(5, 0), padx=5)

        self.zoom_out = CTkButton(self.zoom_properties, text="Zoom Out",
                                  command=lambda : self.zoom.set(self.zoom.get() - self.zoom_amt),
                                  fg_color="transparent", anchor="w")
        self.zoom_out.pack(fill="x", pady=(5, 0), padx=5)

        self.zoom_100 = CTkButton(self.zoom_properties, text="Zoom 100%",
                                  command=lambda : self.zoom.set(100),
                                  fg_color="transparent", anchor="w")
        self.zoom_100.pack(fill="x", pady=5, padx=5)




        self.update_idletasks()
        zt_x = self.zoom_tool.winfo_rootx()
        zt_y = self.zoom_tool.winfo_rooty()
        zt_width = self.zoom_tool.winfo_width()
        zt_height = self.zoom_tool.winfo_height()

        tl_x = self.winfo_toplevel().winfo_rootx()
        tl_y = self.winfo_toplevel().winfo_rooty()

        x_pos = zt_x - tl_x
        y_pos = zt_y - tl_y - zt_height + 10



        self.zoom_properties.place(x=x_pos, y=y_pos, anchor="sw")
        self.update_idletasks()
        self.winfo_toplevel().bind("<Button-1>", self._on_toplevel_click) # <--- IMPORTANT: no add=True here, we want to control this specific bind

    def hide_zoom_properties(self):
        if not self.zoom_properties_toggled:
            return


        self.zoom_properties_toggled = False
        self.zoom_properties.destroy()
        self.winfo_toplevel().unbind("<Button-1>")


    def toggle_zoom_properties(self):
        if self.zoom_properties_toggled:
            self.hide_zoom_properties()
        else:
            self.show_zoom_properties()

    def _on_toplevel_click(self, event):

        if not self.zoom_properties_toggled:
            return

        if self.zoom_properties.winfo_containing(event.x_root, event.y_root).master == self.zoom_properties or self.zoom_properties.winfo_containing(event.x_root, event.y_root).master in [self.zoom_in, self.zoom_100, self.zoom_out]:
            return

        self.hide_zoom_properties()