
from customtkinter import *
from PIL import Image

class App(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.top_bar = CTkFrame(master=self, height=75)
        self.top_bar.pack(pady=(5, 5), fill="x", padx=5)

        self.LABEL4 = CTkLabel(master=self.top_bar, font=CTkFont(size=24), text="Youtube")
        self.LABEL4.pack(padx=(10, 0), side="left")

        self.FRAME5 = CTkFrame(master=self.top_bar, fg_color="transparent")
        self.FRAME5.pack(padx=(0, 5), side="right")

        self.profile = CTkButton(master=self.FRAME5, text="", image=CTkImage(Image.open(
            r"Assets/outline_account_circle_(255, 255, 255)_24dp_1x.png"), size=(24, 24)), width=45, fg_color=['#202020', '#202020'], hover=False)
        self.profile.pack(side="right")

        self.BUTTON8_copy = CTkButton(master=self.FRAME5, text="", image=CTkImage(Image.open(
            r"Assets/outline_notifications_(255, 255, 255)_24dp_1x.png"), size=(24, 24)), width=45, fg_color=['#202020', '#202020'], hover=False)
        self.BUTTON8_copy.pack(side="right")

        self.BUTTON9_copy = CTkButton(master=self.FRAME5, text="", image=CTkImage(Image.open(
            r"Assets/outline_videocam_(255, 255, 255)_24dp_1x.png"), size=(24, 24)), width=45, fg_color=['#202020', '#202020'], hover=False)
        self.BUTTON9_copy.pack(side="right")

        self.FRAME7 = CTkFrame(master=self.top_bar, width=400, fg_color="transparent")
        self.FRAME7.pack(expand=True)

        self.FRAME8 = CTkFrame(master=self.FRAME7, width=300, fg_color=['gray90', '#454545'])
        self.FRAME8.pack(side="left", expand=1)

        self.entry = CTkEntry(master=self.FRAME8, placeholder_text="Search", corner_radius=0, border_width=0, width=500, fg_color=['#e5e5e5', '#454545'])
        self.entry.pack(pady=(5, 5), expand=1, fill="both", padx=(5, 0), side="left")

        self.search = CTkButton(master=self.FRAME8, text="", image=CTkImage(Image.open(
            r"Assets/outline_search_(255, 255, 255)_24dp_1x.png"), size=(24, 24)), width=15, fg_color=['#000000', '#454545'], hover_color=['#353535', '#2e2e2e'])
        self.search.pack(pady=(5, 5), expand=1, fill="both", padx=(0, 5), side="left")

        self.BUTTON12_copy = CTkButton(master=self.FRAME7, text="", image=CTkImage(Image.open(
            r"Assets/outline_mic_(255, 255, 255)_24dp_1x.png"), size=(24, 24)), width=45, fg_color=['#202020', '#202020'], hover=False)
        self.BUTTON12_copy.pack(side="right")

        self.SCROLLABLEFRAME12 = CTkScrollableFrame(master=self, orientation="vertical", width=250, fg_color=['gray90', '#242424'])
        self.SCROLLABLEFRAME12.pack(padx=(5, 5), fill="y", pady=(0, 5), side="left")

        self.BUTTON13 = CTkButton(master=self.SCROLLABLEFRAME12, text="Home", height=40, image=CTkImage(Image.open(
            r"Assets/baseline_home_(255, 255, 255)_24dp_1x.png"), size=(24, 24)), anchor="w", compound="left", fg_color=['#3a7ebf', '#404040'], hover_color=['#325882', '#5f5f5f'])
        self.BUTTON13.pack(fill="x")

        self.BUTTON15_copy = CTkButton(master=self.SCROLLABLEFRAME12, text="Shorts", height=40, image=CTkImage(Image.open(
            r"Assets/outline_recent_actors_(255, 255, 255)_24dp_1x.png"), size=(24, 24)), anchor="w", compound="left", fg_color="transparent", hover_color=['#325882', '#404040'])
        self.BUTTON15_copy.pack(pady=(5, 0), fill="x")

        self.BUTTON16_copy = CTkButton(master=self.SCROLLABLEFRAME12, text="Subscriptions", height=40, image=CTkImage(Image.open(
            r"Assets/outline_video_library_(255, 255, 255)_24dp_1x.png"), size=(24, 24)), anchor="w", compound="left", fg_color="transparent", hover_color=['#325882', '#404040'])
        self.BUTTON16_copy.pack(pady=(5, 0), fill="x")

        self.FRAME15 = CTkFrame(master=self.SCROLLABLEFRAME12, fg_color=['#a8a8a8', '#a7a7a7'], corner_radius=0, height=1)
        self.FRAME15.pack(pady=(5, 5), fill="x")

        self.BUTTON17_copy = CTkButton(master=self.SCROLLABLEFRAME12, font=CTkFont(size=18), text="You", height=40, image=CTkImage(Image.open(
            r"Assets/outline_chevron_right_(255, 255, 255)_24dp_1x.png"), size=(24, 24)), anchor="w", compound="right", fg_color="transparent", hover_color=['#325882', '#404040'])
        self.BUTTON17_copy.pack(pady=(5, 0), fill="x")

        self.BUTTON18_copy = CTkButton(master=self.SCROLLABLEFRAME12, text="Your channel", height=40, image=CTkImage(Image.open(
            r"Assets/baseline_live_tv_(255, 255, 255)_24dp_1x.png"), size=(24, 24)), anchor="w", compound="left", fg_color="transparent", hover_color=['#325882', '#404040'])
        self.BUTTON18_copy.pack(pady=(5, 0), fill="x")

        self.BUTTON19_copy = CTkButton(master=self.SCROLLABLEFRAME12, text="History", height=40, image=CTkImage(Image.open(
            r"Assets/baseline_history_(255, 255, 255)_24dp_1x.png"), size=(24, 24)), anchor="w", compound="left", fg_color="transparent", hover_color=['#325882', '#404040'])
        self.BUTTON19_copy.pack(pady=(5, 0), fill="x")

        self.BUTTON20_copy = CTkButton(master=self.SCROLLABLEFRAME12, text="Playlists", height=40, image=CTkImage(Image.open(
            r"Assets/baseline_playlist_play_(255, 255, 255)_24dp_1x.png"), size=(24, 24)), anchor="w", compound="left", fg_color="transparent", hover_color=['#325882', '#404040'])
        self.BUTTON20_copy.pack(pady=(5, 0), fill="x")

        self.BUTTON21_copy = CTkButton(master=self.SCROLLABLEFRAME12, text="Your videos", height=40, image=CTkImage(Image.open(
            r"Assets/outline_smart_display_(255, 255, 255)_24dp_1x.png"), size=(24, 24)), anchor="w", compound="left", fg_color="transparent", hover_color=['#325882', '#404040'])
        self.BUTTON21_copy.pack(pady=(5, 0), fill="x")

        self.BUTTON22_copy = CTkButton(master=self.SCROLLABLEFRAME12, text="Watch later", height=40, image=CTkImage(Image.open(
            r"Assets/outline_schedule_(255, 255, 255)_24dp_1x.png"), size=(24, 24)), anchor="w", compound="left", fg_color="transparent", hover_color=['#325882', '#404040'])
        self.BUTTON22_copy.pack(pady=(5, 0), fill="x")

        self.BUTTON23_copy = CTkButton(master=self.SCROLLABLEFRAME12, text="Liked videos", height=40, image=CTkImage(Image.open(
            r"Assets/outline_thumb_up_(255, 255, 255)_24dp_1x.png"), size=(24, 24)), anchor="w", compound="left", fg_color="transparent", hover_color=['#325882', '#404040'])
        self.BUTTON23_copy.pack(pady=(5, 0), fill="x")

        self.FRAME36_copy = CTkFrame(master=self.SCROLLABLEFRAME12, fg_color=['#a8a8a8', '#a7a7a7'], corner_radius=0, height=1)
        self.FRAME36_copy.pack(pady=(5, 5), fill="x")

        self.LABEL36 = CTkLabel(master=self.SCROLLABLEFRAME12, font=CTkFont(size=18), text="Subscriptions", anchor="w", fg_color="transparent")
        self.LABEL36.pack(pady=(5, 5), fill="x", padx=(10, 0))

        self.BUTTON38_copy = CTkButton(master=self.SCROLLABLEFRAME12, text="Channel 1", height=40, image=CTkImage(Image.open(
            r"Assets/outline_account_circle_(255, 255, 255)_24dp_1x.png"), size=(24, 24)), anchor="w", compound="left", fg_color="transparent", hover_color=['#325882', '#404040'])
        self.BUTTON38_copy.pack(pady=(5, 0), fill="x")

        self.BUTTON39_copy = CTkButton(master=self.SCROLLABLEFRAME12, text="Channel 2", height=40, image=CTkImage(Image.open(
            r"Assets/outline_account_circle_(255, 255, 255)_24dp_1x.png"), size=(24, 24)), anchor="w", compound="left", fg_color="transparent", hover_color=['#325882', '#404040'])
        self.BUTTON39_copy.pack(pady=(5, 0), fill="x")

        self.BUTTON40_copy = CTkButton(master=self.SCROLLABLEFRAME12, text="Channel 3", height=40, image=CTkImage(Image.open(
            r"Assets/outline_account_circle_(255, 255, 255)_24dp_1x.png"), size=(24, 24)), anchor="w", compound="left", fg_color="transparent", hover_color=['#325882', '#404040'])
        self.BUTTON40_copy.pack(pady=(5, 0), fill="x")

        self.BUTTON41_copy = CTkButton(master=self.SCROLLABLEFRAME12, text="Channel 4", height=40, image=CTkImage(Image.open(
            r"Assets/outline_account_circle_(255, 255, 255)_24dp_1x.png"), size=(24, 24)), anchor="w", compound="left", fg_color="transparent", hover_color=['#325882', '#404040'])
        self.BUTTON41_copy.pack(pady=(5, 0), fill="x")

        self.BUTTON42_copy = CTkButton(master=self.SCROLLABLEFRAME12, text="Channel 5", height=40, image=CTkImage(Image.open(
            r"Assets/outline_account_circle_(255, 255, 255)_24dp_1x.png"), size=(24, 24)), anchor="w", compound="left", fg_color="transparent", hover_color=['#325882', '#404040'])
        self.BUTTON42_copy.pack(pady=(5, 0), fill="x")

        self.FRAME99 = CTkFrame(master=self)
        self.FRAME99.pack(expand=True, fill="both")

        self.SEGMENTEDBUTTON167 = CTkSegmentedButton(master=self.FRAME99, values=['All', 'New', 'Programming', 'Music', 'Python GUI', 'Custom Tkinter', 'Movies', 'Mixes', 'Algorithms', 'New To You'], selected_color=['#3a7ebf', '#242424'], selected_hover_color=['#325882', '#3f3f3f'])
        self.SEGMENTEDBUTTON167.pack(padx=(10, 10), fill="x")

        self.SCROLLABLEFRAME42 = CTkScrollableFrame(master=self.FRAME99, orientation="vertical", fg_color=['gray90', '#242424'])
        self.SCROLLABLEFRAME42.pack(pady=(0, 5), expand=1, fill="both", padx=5)

        self.video_panel1 = CTkFrame(master=self.SCROLLABLEFRAME42, height=296, fg_color="transparent")
        self.video_panel1.pack(fill="x", padx=5, pady=(5, 0))

        self.video_card = CTkFrame(master=self.video_panel1, width=311, height=268, corner_radius=6)
        self.video_card.pack(pady=(5, 5), padx=5, side="left")

        self.LABEL45 = CTkLabel(master=self.video_card, text="", width=311, height=175, image=CTkImage(Image.open(
            r"Assets/16-311x175.jpg"), size=(311, 175)), corner_radius=0)
        self.LABEL45.pack(pady=(5, 0), padx=5)

        self.FRAME35 = CTkFrame(master=self.video_card, width=220, fg_color="transparent")
        self.FRAME35.pack(expand=True, fill="x", side="right")

        self.LABEL38_copy = CTkLabel(master=self.FRAME35, font=CTkFont(weight="bold", size=15), text="Unboxing a Deep Sea Mystery ", anchor="w", wraplength=254, justify="left")
        self.LABEL38_copy.pack(fill="x")

        self.LABEL36 = CTkLabel(master=self.FRAME35, font=CTkFont(weight="normal", size=15), text="Ocean Odyssey", anchor="w", wraplength=254, justify="left", image=CTkImage(Image.open(
            r"Assets/baseline_verified_(120, 174, 255)_18dp_1x.png"), size=(18, 18)), compound="right", height=16)
        self.LABEL36.pack(fill="x")

        self.LABEL39_copy = CTkLabel(master=self.FRAME35, font=CTkFont(weight="normal", size=15), text="12M • 1 week ago", anchor="w", wraplength=254, justify="left", compound="right", height=0)
        self.LABEL39_copy.pack(fill="x")

        self.LABEL34 = CTkLabel(master=self.video_card, text="", image=CTkImage(Image.open(
            r"Assets/outline_account_circle_(255, 255, 255)_24dp_2x.png"), size=(48, 48)))
        self.LABEL34.pack(pady=(5, 0), padx=5)

        self.FRAME47_copy = CTkFrame(master=self.video_panel1, width=311, height=268)
        self.FRAME47_copy.pack(pady=(5, 5), padx=5, side="left")

        self.LABEL48_copy = CTkLabel(master=self.FRAME47_copy, text="", width=311, height=175, image=CTkImage(Image.open(
            r"Assets/160-311x175.jpg"), size=(311, 175)), corner_radius=0)
        self.LABEL48_copy.pack(pady=(5, 0), padx=5)

        self.FRAME49_copy = CTkFrame(master=self.FRAME47_copy, width=220, fg_color="transparent")
        self.FRAME49_copy.pack(expand=True, fill="x", side="right")

        self.LABEL50_copy = CTkLabel(master=self.FRAME49_copy, font=CTkFont(weight="bold", size=15), text="Is This the End of Online Privacy?", anchor="w", wraplength=254, justify="left")
        self.LABEL50_copy.pack(fill="x")

        self.LABEL51_copy = CTkLabel(master=self.FRAME49_copy, font=CTkFont(weight="normal", size=15), text="The Privacy Paradox", anchor="w", wraplength=254, justify="left", image=CTkImage(Image.open(
            r"Assets/baseline_verified_(120, 174, 255)_18dp_1x.png"), size=(18, 18)), compound="right", height=16)
        self.LABEL51_copy.pack(fill="x")

        self.LABEL52_copy = CTkLabel(master=self.FRAME49_copy, font=CTkFont(weight="normal", size=15), text="27M • 2 months ago", anchor="w", wraplength=254, justify="left", compound="right", height=0)
        self.LABEL52_copy.pack(fill="x")

        self.LABEL53_copy = CTkLabel(master=self.FRAME47_copy, text="", image=CTkImage(Image.open(
            r"Assets/outline_account_circle_(255, 255, 255)_24dp_2x.png"), size=(48, 48)))
        self.LABEL53_copy.pack(pady=(5, 0), padx=5)

        self.FRAME54_copy = CTkFrame(master=self.video_panel1, width=311, height=268)
        self.FRAME54_copy.pack(pady=(5, 5), padx=5, side="left")

        self.LABEL55_copy = CTkLabel(master=self.FRAME54_copy, text="", width=311, height=175, image=CTkImage(Image.open(
            r"Assets/464-311x175.jpg"), size=(311, 175)), corner_radius=0)
        self.LABEL55_copy.pack(pady=(5, 0), padx=5)

        self.FRAME56_copy = CTkFrame(master=self.FRAME54_copy, width=220, fg_color="transparent")
        self.FRAME56_copy.pack(expand=True, fill="x", side="right")

        self.LABEL57_copy = CTkLabel(master=self.FRAME56_copy, font=CTkFont(weight="bold", size=15), text="Lost Languages: Can We Crack the Code?", anchor="w", wraplength=254, justify="left")
        self.LABEL57_copy.pack(fill="x")

        self.LABEL58_copy = CTkLabel(master=self.FRAME56_copy, font=CTkFont(weight="normal", size=15), text="Linguistics Lab", anchor="w", wraplength=254, justify="left", compound="right", height=16)
        self.LABEL58_copy.pack(fill="x")

        self.LABEL59_copy = CTkLabel(master=self.FRAME56_copy, font=CTkFont(weight="normal", size=15), text="102K • 1 month ago", anchor="w", wraplength=254, justify="left", compound="right", height=0)
        self.LABEL59_copy.pack(fill="x")

        self.LABEL60_copy = CTkLabel(master=self.FRAME54_copy, text="", image=CTkImage(Image.open(
            r"Assets/outline_account_circle_(255, 255, 255)_24dp_2x.png"), size=(48, 48)))
        self.LABEL60_copy.pack(pady=(5, 0), padx=5)

        self.FRAME55_copy = CTkFrame(master=self.SCROLLABLEFRAME42, height=296, fg_color="transparent")
        self.FRAME55_copy.pack(fill="x", padx=5, pady=(5, 0))

        self.FRAME56_copy = CTkFrame(master=self.FRAME55_copy, width=311, height=268)
        self.FRAME56_copy.pack(pady=(5, 5), padx=5, side="left")

        self.LABEL57_copy = CTkLabel(master=self.FRAME56_copy, text="", width=311, height=175, image=CTkImage(Image.open(
            r"Assets/957-311x175.jpg"), size=(311, 175)), corner_radius=0)
        self.LABEL57_copy.pack(pady=(5, 0), padx=5)

        self.FRAME58_copy = CTkFrame(master=self.FRAME56_copy, width=220, fg_color="transparent")
        self.FRAME58_copy.pack(expand=True, fill="x", side="right")

        self.LABEL59_copy = CTkLabel(master=self.FRAME58_copy, font=CTkFont(weight="bold", size=15), text="Climate Change: The Next 10 Years", anchor="w", wraplength=254, justify="left")
        self.LABEL59_copy.pack(fill="x")

        self.LABEL60_copy = CTkLabel(master=self.FRAME58_copy, font=CTkFont(weight="normal", size=15), text="Earth Speak", anchor="w", wraplength=254, justify="left", image=CTkImage(Image.open(
            r"Assets/baseline_verified_(120, 174, 255)_18dp_1x.png"), size=(18, 18)), compound="right", height=16)
        self.LABEL60_copy.pack(fill="x")

        self.LABEL61_copy = CTkLabel(master=self.FRAME58_copy, font=CTkFont(weight="normal", size=15), text="1M • 6 months ago", anchor="w", wraplength=254, justify="left", compound="right", height=0)
        self.LABEL61_copy.pack(fill="x")

        self.LABEL62_copy = CTkLabel(master=self.FRAME56_copy, text="", image=CTkImage(Image.open(
            r"Assets/outline_account_circle_(255, 255, 255)_24dp_2x.png"), size=(48, 48)))
        self.LABEL62_copy.pack(pady=(5, 0), padx=5)

        self.FRAME63_copy = CTkFrame(master=self.FRAME55_copy, width=311, height=268)
        self.FRAME63_copy.pack(pady=(5, 5), padx=5, side="left")

        self.LABEL64_copy = CTkLabel(master=self.FRAME63_copy, text="", width=311, height=175, image=CTkImage(Image.open(
            r"Assets/974-311x175.jpg"), size=(311, 175)), corner_radius=0)
        self.LABEL64_copy.pack(pady=(5, 0), padx=5)

        self.FRAME65_copy = CTkFrame(master=self.FRAME63_copy, width=220, fg_color="transparent")
        self.FRAME65_copy.pack(expand=True, fill="x", side="right")

        self.LABEL66_copy = CTkLabel(master=self.FRAME65_copy, font=CTkFont(weight="bold", size=15), text="The Ethics of Artificial Intelligence", anchor="w", wraplength=254, justify="left")
        self.LABEL66_copy.pack(fill="x")

        self.LABEL67_copy = CTkLabel(master=self.FRAME65_copy, font=CTkFont(weight="normal", size=15), text="Future Lens", anchor="w", wraplength=254, justify="left", compound="right", height=16)
        self.LABEL67_copy.pack(fill="x")

        self.LABEL68_copy = CTkLabel(master=self.FRAME65_copy, font=CTkFont(weight="normal", size=15), text="100 views • 1 month ago", anchor="w", wraplength=254, justify="left", compound="right", height=0)
        self.LABEL68_copy.pack(fill="x")

        self.LABEL69_copy = CTkLabel(master=self.FRAME63_copy, text="", image=CTkImage(Image.open(
            r"Assets/outline_account_circle_(255, 255, 255)_24dp_2x.png"), size=(48, 48)))
        self.LABEL69_copy.pack(pady=(5, 0), padx=5)

        self.FRAME70_copy = CTkFrame(master=self.FRAME55_copy, width=311, height=268)
        self.FRAME70_copy.pack(pady=(5, 5), padx=5, side="left")

        self.LABEL71_copy = CTkLabel(master=self.FRAME70_copy, text="", width=311, height=175, image=CTkImage(Image.open(
            r"Assets/6-311x175.jpg"), size=(311, 175)), corner_radius=0)
        self.LABEL71_copy.pack(pady=(5, 0), padx=5)

        self.FRAME72_copy = CTkFrame(master=self.FRAME70_copy, width=220, fg_color="transparent")
        self.FRAME72_copy.pack(expand=True, fill="x", side="right")

        self.LABEL73_copy = CTkLabel(master=self.FRAME72_copy, font=CTkFont(weight="bold", size=15), text="The Psychology of Addiction: Breaking Free", anchor="w", wraplength=254, justify="left")
        self.LABEL73_copy.pack(fill="x")

        self.LABEL74_copy = CTkLabel(master=self.FRAME72_copy, font=CTkFont(weight="normal", size=15), text="Balanced Mind", anchor="w", wraplength=254, justify="left", compound="right", height=16)
        self.LABEL74_copy.pack(fill="x")

        self.LABEL75_copy = CTkLabel(master=self.FRAME72_copy, font=CTkFont(weight="normal", size=15), text="10K • 2 years ago", anchor="w", wraplength=254, justify="left", compound="right", height=0)
        self.LABEL75_copy.pack(fill="x")

        self.LABEL76_copy = CTkLabel(master=self.FRAME70_copy, text="", image=CTkImage(Image.open(
            r"Assets/outline_account_circle_(255, 255, 255)_24dp_2x.png"), size=(48, 48)))
        self.LABEL76_copy.pack(pady=(5, 0), padx=5)

        self.FRAME77_copy = CTkFrame(master=self.SCROLLABLEFRAME42, height=296, fg_color="transparent")
        self.FRAME77_copy.pack(fill="x", padx=5, pady=(5, 0))

        self.FRAME78_copy = CTkFrame(master=self.FRAME77_copy, width=311, height=268)
        self.FRAME78_copy.pack(pady=(5, 5), padx=5, side="left")

        self.LABEL79_copy = CTkLabel(master=self.FRAME78_copy, text="", width=311, height=175, image=CTkImage(Image.open(
            r"Assets/385-311x175.jpg"), size=(311, 175)), corner_radius=0)
        self.LABEL79_copy.pack(pady=(5, 0), padx=5)

        self.FRAME80_copy = CTkFrame(master=self.FRAME78_copy, width=220, fg_color="transparent")
        self.FRAME80_copy.pack(expand=True, fill="x", side="right")

        self.LABEL81_copy = CTkLabel(master=self.FRAME80_copy, font=CTkFont(weight="bold", size=15), text="The Search for Extraterrestrial Life: Update 2024", anchor="w", wraplength=254, justify="left")
        self.LABEL81_copy.pack(fill="x")

        self.LABEL82_copy = CTkLabel(master=self.FRAME80_copy, font=CTkFont(weight="normal", size=15), text="Aliens", anchor="w", wraplength=254, justify="left", image=CTkImage(Image.open(
            r"Assets/baseline_verified_(120, 174, 255)_18dp_1x.png"), size=(18, 18)), compound="right", height=16)
        self.LABEL82_copy.pack(fill="x")

        self.LABEL83_copy = CTkLabel(master=self.FRAME80_copy, font=CTkFont(weight="normal", size=15), text="30M • 1 day ago", anchor="w", wraplength=254, justify="left", compound="right", height=0)
        self.LABEL83_copy.pack(fill="x")

        self.LABEL84_copy = CTkLabel(master=self.FRAME78_copy, text="", image=CTkImage(Image.open(
            r"Assets/outline_account_circle_(255, 255, 255)_24dp_2x.png"), size=(48, 48)))
        self.LABEL84_copy.pack(pady=(5, 0), padx=5)

        self.FRAME85_copy = CTkFrame(master=self.FRAME77_copy, width=311, height=268)
        self.FRAME85_copy.pack(pady=(5, 5), padx=5, side="left")

        self.LABEL86_copy = CTkLabel(master=self.FRAME85_copy, text="", width=311, height=175, image=CTkImage(Image.open(
            r"Assets/492-311x175.jpg"), size=(311, 175)), corner_radius=0)
        self.LABEL86_copy.pack(pady=(5, 0), padx=5)

        self.FRAME87_copy = CTkFrame(master=self.FRAME85_copy, width=220, fg_color="transparent")
        self.FRAME87_copy.pack(expand=True, fill="x", side="right")

        self.LABEL88_copy = CTkLabel(master=self.FRAME87_copy, font=CTkFont(weight="bold", size=15), text="The Future of Food: Sustainable Solutions ", anchor="w", wraplength=254, justify="left")
        self.LABEL88_copy.pack(fill="x")

        self.LABEL89_copy = CTkLabel(master=self.FRAME87_copy, font=CTkFont(weight="normal", size=15), text="Food Revolution", anchor="w", wraplength=254, justify="left", compound="right", height=16)
        self.LABEL89_copy.pack(fill="x")

        self.LABEL90_copy = CTkLabel(master=self.FRAME87_copy, font=CTkFont(weight="normal", size=15), text="1K • 3 months ago", anchor="w", wraplength=254, justify="left", compound="right", height=0)
        self.LABEL90_copy.pack(fill="x")

        self.LABEL91_copy = CTkLabel(master=self.FRAME85_copy, text="", image=CTkImage(Image.open(
            r"Assets/outline_account_circle_(255, 255, 255)_24dp_2x.png"), size=(48, 48)))
        self.LABEL91_copy.pack(pady=(5, 0), padx=5)

        self.FRAME92_copy = CTkFrame(master=self.FRAME77_copy, width=311, height=268)
        self.FRAME92_copy.pack(pady=(5, 5), padx=5, side="left")

        self.LABEL93_copy = CTkLabel(master=self.FRAME92_copy, text="", width=311, height=175, image=CTkImage(Image.open(
            r"Assets/128-311x175.jpg"), size=(311, 175)), corner_radius=0)
        self.LABEL93_copy.pack(pady=(5, 0), padx=5)

        self.FRAME94_copy = CTkFrame(master=self.FRAME92_copy, width=220, fg_color="transparent")
        self.FRAME94_copy.pack(expand=True, fill="x", side="right")

        self.LABEL95_copy = CTkLabel(master=self.FRAME94_copy, font=CTkFont(weight="bold", size=15), text="Universal Basic Income: A Viable Solution?", anchor="w", wraplength=254, justify="left")
        self.LABEL95_copy.pack(fill="x")

        self.LABEL96_copy = CTkLabel(master=self.FRAME94_copy, font=CTkFont(weight="normal", size=15), text="The Policy Post", anchor="w", wraplength=254, justify="left", compound="right", height=16)
        self.LABEL96_copy.pack(fill="x")

        self.LABEL97_copy = CTkLabel(master=self.FRAME94_copy, font=CTkFont(weight="normal", size=15), text="10K • 5 months ago", anchor="w", wraplength=254, justify="left", compound="right", height=0)
        self.LABEL97_copy.pack(fill="x")

        self.LABEL98_copy = CTkLabel(master=self.FRAME92_copy, text="", image=CTkImage(Image.open(
            r"Assets/outline_account_circle_(255, 255, 255)_24dp_2x.png"), size=(48, 48)))
        self.LABEL98_copy.pack(pady=(5, 0), padx=5)

        
set_default_color_theme("dark-blue")
root = App()
root.geometry("1300x730")
root.title("Custom Tkinter Builder - Youtube Demo")
root.configure(fg_color=['gray92', 'gray14'])
root.mainloop()
            
