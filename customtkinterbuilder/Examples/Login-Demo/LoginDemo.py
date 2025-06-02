from customtkinter import *
from PIL import Image

class App(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.FRAME0 = CTkFrame(master=self, fg_color="transparent")
        self.FRAME0.pack(pady=(5, 5), expand=1, fill="both", padx=(5, 0), side="left")

        self.LABEL19 = CTkLabel(master=self.FRAME0, font=CTkFont(size=15), text="", anchor="w", text_color=['gray10', '#FFFFFF'], image=CTkImage(Image.open(
            r"Assets/baseline_logo_dev_(145, 91, 255)_24dp_2x.png"), size=(48, 48)))
        self.LABEL19.pack(pady=(20, 0), fill="x", padx=(20, 0))

        self.LABEL18 = CTkLabel(master=self.FRAME0, font=CTkFont(size=82), text="Welcome\nBack !", justify="left", anchor="w", text_color=['gray10', '#FFFFFF'])
        self.LABEL18.pack(padx=(30, 0), expand=1, fill="x")

        self.FRAME2_copy = CTkFrame(master=self)
        self.FRAME2_copy.pack(pady=(20, 20), expand=1, fill="both", padx=(5, 20), side="left")

        self.FRAME2 = CTkFrame(master=self.FRAME2_copy, width=465, height=400, fg_color="transparent")
        self.FRAME2.pack(expand=1, padx=50, pady=50)

        self.LABEL3 = CTkLabel(master=self.FRAME2, font=CTkFont(size=39), text="Login", anchor="w", text_color=['gray10', '#FFFFFF'])
        self.LABEL3.pack(fill="x")

        self.LABEL5_copy = CTkLabel(master=self.FRAME2, font=CTkFont(size=14), text="Welcome Back! Please login to your account", anchor="w", text_color=['gray10', '#b4b4b4'], wraplength=332, justify="left")
        self.LABEL5_copy.pack(pady=(10, 10), fill="x")

        self.FRAME5 = CTkFrame(master=self.FRAME2, fg_color="transparent")
        self.FRAME5.pack(pady=(0, 0), fill="x")

        self.LABEL8_copy = CTkLabel(master=self.FRAME5, font=CTkFont(size=15), text="User Name", anchor="w", text_color=['gray10', '#FFFFFF'])
        self.LABEL8_copy.pack(fill="x")

        self.ENTRY9 = CTkEntry(master=self.FRAME5, placeholder_text="example@gmail.com", height=35, corner_radius=3, text_color=['gray10', '#FFFFFF'], width=222)
        self.ENTRY9.pack(fill="x")

        self.FRAME11_copy = CTkFrame(master=self.FRAME2, fg_color="transparent")
        self.FRAME11_copy.pack(pady=(10, 0), fill="x")

        self.LABEL12_copy = CTkLabel(master=self.FRAME11_copy, font=CTkFont(size=15), text="Password", anchor="w", text_color=['gray10', '#FFFFFF'])
        self.LABEL12_copy.pack(fill="x")

        self.ENTRY13_copy = CTkEntry(master=self.FRAME11_copy, placeholder_text="", height=35, corner_radius=3, text_color=['gray10', '#FFFFFF'])
        self.ENTRY13_copy.pack(fill="x")

        self.FRAME13 = CTkFrame(master=self.FRAME2, fg_color="transparent")
        self.FRAME13.pack(pady=(20, 20), fill="x")

        self.CHECKBOX14 = CTkCheckBox(master=self.FRAME13, text="Remember Me", fg_color=['#8651ff', '#8651ff'], hover_color=['#6940c9', '#6940c9'], text_color=['gray10', '#FFFFFF'], state="normal", corner_radius=3)
        self.CHECKBOX14.pack(side="left")

        self.BUTTON15 = CTkButton(master=self.FRAME13, text="Forgot Password?", fg_color="transparent", hover=False, text_color=['#000000', '#FFFFFF'])
        self.BUTTON15.pack(side="right")

        self.BUTTON16 = CTkButton(master=self.FRAME2, text="Login", height=35, text_color=['gray98', '#FFFFFF'], fg_color=['#8651ff', '#8651ff'], hover_color=['#6940c9', '#6940c9'], width=500, corner_radius=3)
        self.BUTTON16.pack(fill="x")

        self.FRAME17 = CTkFrame(master=self.FRAME2, fg_color="transparent")
        self.FRAME17.pack(pady=(10, 0), fill="x")

        self.LABEL18 = CTkLabel(master=self.FRAME17, text="New User?", text_color=['gray10', '#FFFFFF'])
        self.LABEL18.pack(side="left")

        self.BUTTON19 = CTkButton(master=self.FRAME17, text="Sign Up", width=70, fg_color="transparent", hover=False, height=0, text_color=['#000000', '#FFFFFF'])
        self.BUTTON19.pack(side="left")

        
set_default_color_theme("green")
root = App()
root.geometry("1000x600")
root.title("Custom Tkinter Builder - Login Demo")
root.configure(fg_color=['gray92', 'gray14'])
root.mainloop()

