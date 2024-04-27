import uuid
import json
from tkinter.filedialog import askdirectory

from customtkinter import *
from PIL import Image
from main import SaveFileDialog, App
class Root(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.FRAME0 = CTkFrame(master=self, width=300, fg_color=['#f1f0ea', '#0d0c1d'])
        self.FRAME0.pack_propagate(False)
        self.FRAME0.pack(fill="y", anchor="center", expand=0, ipadx=0, ipady=0, padx=0, pady=0, side="left")
        self.LABEL3 = CTkLabel(master=self.FRAME0, text="Custom Tkinter\nBuilder", compound="left", justify="left", image=CTkImage(Image.open("Assets/baseline_logo_dev_white_48dp_2x.png"), size=(96, 96)), text_color=['#0d0c1d', '#f1f0ea'], font=CTkFont(family="SF Display", size=25))
        self.LABEL3.pack(pady=['20', 30], anchor="center", expand=0, fill="none", ipadx=0, ipady=0, padx=0, side="top")
        self.BUTTON4 = CTkButton(master=self.FRAME0, text="     Projects", height=40, anchor="w", corner_radius=0, fg_color=['#cf245e', '#cf245e'], hover_color=['#ae1d4f', '#ae1d4f'], text_color=['#f1f0ea', '#f1f0ea'], font=CTkFont(family="SF Display", size=20))
        self.BUTTON4.pack(fill="x", anchor="center", expand=0, ipadx=0, ipady=0, padx=0, pady=0, side="top")
        self.BUTTON6_copy = CTkButton(master=self.FRAME0, text="     Customize", height=40, anchor="w", corner_radius=0, fg_color="transparent", hover_color=['#ae1d4f', '#ae1d4f'], text_color=['#0d0c1d', '#f1f0ea'], font=CTkFont(family="SF Display", size=20))
        #self.BUTTON6_copy.pack(fill="x", anchor="center", expand=0, ipadx=0, ipady=0, padx=0, pady=0, side="top")
        self.FRAME3_copy = CTkFrame(master=self, width=300, fg_color=['#e0ddcf', '#161b33'])
        self.FRAME3_copy.pack_propagate(False)
        self.FRAME3_copy.pack(pady=['10', 10], anchor="center", expand=1, fill="both", ipadx=0, ipady=0, padx=[0, 10], side="left")

        self.FRAME6 = CTkFrame(master=self.FRAME3_copy, height=55, fg_color=['#e0ddcf', '#161b33'])
        self.FRAME6.pack_propagate(False)
        self.FRAME6.pack(pady=['10', 10], anchor="center", expand=0, fill="x", ipadx=0, ipady=0, padx=10, side="top")
        self.FRAME7 = CTkFrame(master=self.FRAME6, fg_color=['#e0ddcf', '#161b33'])
        self.FRAME7.pack_propagate(False)
        self.FRAME7.pack(pady=['5', 5], anchor="center", expand=1, fill="x", ipadx=0, ipady=0, padx=5, side="left")
        self.LABEL8 = CTkLabel(master=self.FRAME7, text="", image=CTkImage(Image.open("Assets/baseline_search_white_24dp_1x.png"), size=(24, 24)), font=CTkFont(family="SF Display"))
        self.LABEL8.pack(padx=[10, '0'], anchor="center", expand=0, fill="none", ipadx=0, ipady=0, pady=0, side="left")
        self.ENTRY9 = CTkEntry(master=self.FRAME7, placeholder_text="Search Projects", fg_color=['#e0ddcf', '#161b33'], border_width=0, text_color=['#0d0c1d', '#f1f0ea'], placeholder_text_color=['#161b33', '#e0ddcf'], font=CTkFont(family="SF Display", size=14))
        self.ENTRY9.pack(padx=['10', 10], anchor="center", expand=1, fill="x", ipadx=0, ipady=0, pady=0, side="left")
        self.BUTTON10 = CTkButton(master=self.FRAME6, text="New Project", corner_radius=3, fg_color=['#cf245e', '#cf245e'], hover_color=['#ae1d4f', '#ae1d4f'], text_color=['gray98', '#f1f0ea'], font=CTkFont(family="SF Display", size=14), command=lambda: SaveFileDialog(callback=self.create_project))
        self.BUTTON10.pack(padx=[5, '5'], anchor="center", expand=0, fill="none", ipadx=0, ipady=0, pady=0, side="left")
        self.BUTTON13_copy = CTkButton(master=self.FRAME6, text="Open", corner_radius=3, fg_color=['#cf245e', '#cf245e'], hover_color=['#ae1d4f', '#ae1d4f'], text_color=['gray98', '#f1f0ea'], width=90, font=CTkFont(family="SF Display", size=14), command=self.open_project_from_disk)
        self.BUTTON13_copy.pack(padx=['5', 10], anchor="center", expand=0, fill="none", ipadx=0, ipady=0, pady=0, side="left")

        self.FRAME20_copy = CTkScrollableFrame(master=self.FRAME3_copy, width=300, fg_color=['#e0ddcf', '#161b33'])

        self.FRAME20_copy.pack(pady=[10, 10], anchor="center", expand=1, fill="both", ipadx=0, ipady=0, padx=[10, 10])

    def open_project_in_editor(self, dir_, name):
        print(dir_, name)

        self.withdraw()
        set_default_color_theme(os.path.join("Themes", "ctktheme.json"))
        app = App()
        app.main.file = [dir_, name]
        app.main.open_file_without_asking()
        app.mainloop()

    def open_project_from_disk(self):
        file = askdirectory()
        if file != "":
            file = [os.path.dirname(file), os.path.basename(file)]
            with open("config.json", 'r') as openfile:
                configure = json.load(openfile)
            project_files = configure["project_files"]
            project_files.append({"Name": file[1], "Directory": file[0]})
            configure["project_files"] = project_files
            json_object = json.dumps(configure, indent=4)
            with open("config.json", 'w') as f:
                f.write(json_object)

            short_name = file[1][0:2].upper()
            self.show_project(short_name, file[1], file[0])

    def show_project(self, short_name, name, dir_):
        FRAME13 = CTkFrame(master=self.FRAME20_copy, height=65, fg_color=['#f1f0ea', '#0d0c1d'])
        FRAME13.pack_propagate(False)
        FRAME13.pack(padx=['15', 20], anchor="center", expand=0, fill="x", ipadx=0, ipady=0, pady=[10, 0],
                          side="bottom")
        LABEL14 = CTkLabel(master=FRAME13, text=short_name.upper(), width=50, height=50,
                                fg_color=['#cf245e', '#cf245e'], corner_radius=3, text_color=['#f1f0ea', '#f1f0ea'],
                                font=CTkFont(family="SF Display", size=14))
        LABEL14.pack(padx=[8, '0'], anchor="center", expand=0, fill="none", ipadx=0, ipady=0, pady=0, side="left")
        FRAME15 = CTkFrame(master=FRAME13, height=45, fg_color=['#f1f0ea', '#0d0c1d'])
        FRAME15.pack_propagate(False)
        FRAME15.pack(padx=['10', 10], anchor="center", expand=1, fill="x", ipadx=0, ipady=0, pady=1, side="top")
        LABEL16 = CTkLabel(master=FRAME15, text=name, text_color=['gray10', '#f1f0ea'], anchor="w", height=22,
                                font=CTkFont(family="SF Display", size=14))
        LABEL16.pack(expand="true", anchor="center", fill="x", ipadx=0, ipady=0, padx=0, pady=0, side="top")
        LABEL18_copy = CTkLabel(master=FRAME15, text=dir_, text_color=['#adaba7', '#adaba7'], anchor="w",
                                     font=CTkFont(family="SF Display", size=14))
        LABEL18_copy.pack(expand="true", anchor="center", fill="x", ipadx=0, ipady=0, padx=0, pady=0, side="top")
        #self.FRAME13.bind('<Double-Button-1>', lambda e, dir_=dir_, name=name: self.open_project_in_editor(dir_=dir_, name=name))
        for x in [FRAME13, FRAME15, LABEL14, LABEL16, LABEL18_copy]:
            x.bind('<Double-Button-1>', lambda e, dir_=dir_, name=name: self.open_project_in_editor(dir_=dir_, name=name))
    def create_project(self, name="Project 1", dir_="~/Project 1"):
        try:
            json_ = {
                "MAIN-1": {
                    "TYPE": "MAIN",
                    "parameters": {},
                    "pack_options": {},
                    "ID": str(uuid.uuid4()),
                    "theme": "green",
                    "palette_on_change": {},
                    "palette": {}
                }
            }
            os.mkdir(os.path.join(dir_, name))
            os.mkdir(os.path.join(dir_, name, "Assets"))
            json_object = json.dumps(json_, indent=4)
            with open(os.path.join(dir_, name, name+".json"), "w") as f:
                f.write(json_object)
            with open("config.json", 'r') as openfile:
                configure = json.load(openfile)
            project_files = configure["project_files"]
            project_files.append({"Name": name, "Directory": dir_})
            configure["project_files"] = project_files
            json_object = json.dumps(configure, indent=4)
            with open("config.json", 'w') as f:
                f.write(json_object)

            short_name = name[0:2].upper()
            self.show_project(short_name, name, dir_)


        except Exception as e:
            print(e)

set_default_color_theme(os.path.join("Themes", "ctktheme.json"))
root = Root()
root.geometry("1000x600")
root.title("Welcome To Custom Tkinter Builder")
root.configure(fg_color=['#f1f0ea', '#0d0c1d'])
#for x in range(100):
with open("config.json", 'r') as openfile:
    configure = json.load(openfile)
project_file = configure["project_files"]
for project in project_file:
    root.show_project(project["Name"][0:2], project["Name"], project["Directory"])
root.mainloop()
            
