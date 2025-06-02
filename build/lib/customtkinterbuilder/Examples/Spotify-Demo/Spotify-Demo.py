
from customtkinter import *
from PIL import Image

class App(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.top_panel = CTkFrame(master=self)
        self.top_panel.pack(pady=(0, 0), expand=1, fill="both")

        self.FRAME23 = CTkFrame(master=self.top_panel, width=250, corner_radius=0, fg_color=['#ababab', 'gray20'])
        self.FRAME23.pack(fill="y", side="left")

        self.FRAME25 = CTkFrame(master=self.FRAME23, fg_color="transparent")
        self.FRAME25.pack(pady=(30, 0), fill="x", padx=10)

        self.BUTTON26 = CTkButton(master=self.FRAME25, font=CTkFont(size=15), text="Home", corner_radius=3, height=40, image=CTkImage(Image.open(
            r"Assets/baseline_home_(255, 255, 255)_18dp_1x.png"), size=(18, 18)), anchor="w", compound="left", fg_color=['#cf245e', '#cf245e'], hover_color=['#ae1d4f', '#ae1d4f'], text_color=['gray98', '#ffffff'])
        self.BUTTON26.pack(pady=(10, 0), fill="x")

        self.BUTTON28_copy = CTkButton(master=self.FRAME25, font=CTkFont(size=15), text="Search", corner_radius=3, height=40, image=CTkImage(Image.open(
            r"Assets/baseline_search_(255, 255, 255)_18dp_1x.png"), size=(18, 18)), anchor="w", compound="left", fg_color="transparent", hover_color=['#ae1d4f', '#ae1d4f'], text_color=['gray98', '#ffffff'])
        self.BUTTON28_copy.pack(pady=(10, 0), fill="x")

        self.BUTTON29_copy = CTkButton(master=self.FRAME25, font=CTkFont(size=15), text="Your Library", corner_radius=3, height=40, image=CTkImage(Image.open(
            r"Assets/baseline_library_music_(255, 255, 255)_18dp_1x.png"), size=(18, 18)), anchor="w", compound="left", fg_color="transparent", hover_color=['#ae1d4f', '#ae1d4f'], text_color=['gray98', '#ffffff'])
        self.BUTTON29_copy.pack(pady=(10, 0), fill="x")

        self.FRAME31_copy = CTkFrame(master=self.FRAME23, fg_color="transparent")
        self.FRAME31_copy.pack(pady=(30, 0), fill="x", padx=10)

        self.LABEL35 = CTkLabel(master=self.FRAME31_copy, font=CTkFont(size=15), text="Playlists", text_color=['#ffffff', '#ffffff'], anchor="w", padx=7)
        self.LABEL35.pack(fill="x")

        self.BUTTON33_copy = CTkButton(master=self.FRAME31_copy, font=CTkFont(size=15), text="Create Playlist", corner_radius=3, height=40, image=CTkImage(Image.open(
            r"Assets/baseline_add_(255, 255, 255)_18dp_1x.png"), size=(18, 18)), anchor="w", compound="left", fg_color="transparent", hover_color=['#ae1d4f', '#ae1d4f'], text_color=['gray98', '#ffffff'])
        self.BUTTON33_copy.pack(pady=(10, 0), fill="x")

        self.BUTTON34_copy = CTkButton(master=self.FRAME31_copy, font=CTkFont(size=15), text="Liked Songs", corner_radius=3, height=40, image=CTkImage(Image.open(
            r"Assets/baseline_favorite_(255, 255, 255)_18dp_1x.png"), size=(18, 18)), anchor="w", compound="left", fg_color="transparent", hover_color=['#ae1d4f', '#ae1d4f'], text_color=['gray98', '#ffffff'])
        self.BUTTON34_copy.pack(pady=(10, 0), fill="x")

        self.separator = CTkFrame(master=self.FRAME23, corner_radius=0, height=1, fg_color=['gray86', '#6e6e6e'])
        self.separator.pack(pady=(5, 5), fill="x", padx=10)

        self.FRAME34 = CTkFrame(master=self.FRAME23, fg_color="transparent")
        self.FRAME34.pack(pady=(10, 0), fill="x", padx=10)

        self.BUTTON35 = CTkButton(master=self.FRAME34, font=CTkFont(size=15), text="2024 Greatest Hits", anchor="w", height=20, fg_color="transparent", hover_color=['#ae1d4f', '#ae1d4f'], corner_radius=3, text_color=['gray98', '#ffffff'])
        self.BUTTON35.pack(fill="x")

        self.BUTTON37_copy = CTkButton(master=self.FRAME34, font=CTkFont(size=15), text="At Work", anchor="w", height=20, fg_color="transparent", hover_color=['#ae1d4f', '#ae1d4f'], corner_radius=3, text_color=['gray98', '#ffffff'])
        self.BUTTON37_copy.pack(fill="x")

        self.BUTTON38_copy = CTkButton(master=self.FRAME34, font=CTkFont(size=15), text="Playlist #2", anchor="w", height=20, fg_color="transparent", hover_color=['#ae1d4f', '#ae1d4f'], corner_radius=3, text_color=['gray98', '#ffffff'], border_width=0)
        self.BUTTON38_copy.pack(fill="x")

        self.BUTTON39_copy = CTkButton(master=self.FRAME34, font=CTkFont(size=15), text="Playlist #4", anchor="w", height=20, fg_color="transparent", hover_color=['#ae1d4f', '#ae1d4f'], corner_radius=3, text_color=['gray98', '#ffffff'], state="normal", border_width=0)
        self.BUTTON39_copy.pack(fill="x")

        self.SCROLLABLEFRAME24 = CTkScrollableFrame(master=self.top_panel, orientation="vertical", fg_color=['gray86', '#2c2c2c'])
        self.SCROLLABLEFRAME24.pack(expand=True, fill="both")

        self.LABEL39 = CTkLabel(master=self.SCROLLABLEFRAME24, font=CTkFont(size=30), text="Good Morning", anchor="w", text_color=['gray10', '#ffffff'])
        self.LABEL39.pack(pady=(20, 0), fill="x", padx=(20, 0))

        self.FRAME40 = CTkFrame(master=self.SCROLLABLEFRAME24, fg_color="transparent")
        self.FRAME40.pack(pady=(10, 0), fill="x", padx=20)

        self.FRAME41 = CTkFrame(master=self.FRAME40, fg_color=['#c0c0c0', '#3a3a3a'], corner_radius=3, height=70)
        self.FRAME41.pack(side="left", expand=1, fill="x", padx=(0, 20))

        self.LABEL42 = CTkLabel(master=self.FRAME41, text="", width=70, height=70, fg_color=['#CF245E', '#cf245e'], corner_radius=3)
        self.LABEL42.pack(side="left")

        self.LABEL43 = CTkLabel(master=self.FRAME41, font=CTkFont(size=15), text="Daily Mix 1", anchor="w", text_color=['gray10', '#ffffff'])
        self.LABEL43.pack(padx=(10, 1), expand=1, fill="x", side="left")

        self.FRAME45_copy = CTkFrame(master=self.FRAME40, fg_color=['#c0c0c0', '#3a3a3a'], corner_radius=3, height=70)
        self.FRAME45_copy.pack(side="left", expand=1, fill="x", padx=(0, 20))

        self.LABEL46_copy = CTkLabel(master=self.FRAME45_copy, text="", width=70, height=70, fg_color=['#CF245E', '#cf245e'], corner_radius=3)
        self.LABEL46_copy.pack(side="left")

        self.LABEL47_copy = CTkLabel(master=self.FRAME45_copy, font=CTkFont(size=15), text="Daily Mix 2", anchor="w", text_color=['gray10', '#ffffff'])
        self.LABEL47_copy.pack(padx=(10, 1), expand=1, fill="x", side="left")

        self.FRAME48_copy = CTkFrame(master=self.FRAME40, fg_color=['#c0c0c0', '#3a3a3a'], corner_radius=3, height=70)
        self.FRAME48_copy.pack(padx=(0, 0), expand=1, fill="x", side="left")

        self.LABEL49_copy = CTkLabel(master=self.FRAME48_copy, text="", width=70, height=70, fg_color=['#CF245E', '#cf245e'], corner_radius=3)
        self.LABEL49_copy.pack(side="left")

        self.LABEL50_copy = CTkLabel(master=self.FRAME48_copy, font=CTkFont(size=15), text="Daily Mix 3", anchor="w", text_color=['gray10', '#ffffff'])
        self.LABEL50_copy.pack(padx=(10, 1), expand=1, fill="x", side="left")

        self.FRAME51_copy = CTkFrame(master=self.SCROLLABLEFRAME24, fg_color="transparent")
        self.FRAME51_copy.pack(pady=(20, 0), fill="x", padx=20)

        self.FRAME52_copy = CTkFrame(master=self.FRAME51_copy, fg_color=['#c0c0c0', '#3a3a3a'], corner_radius=3, height=70)
        self.FRAME52_copy.pack(side="left", expand=1, fill="x", padx=(0, 20))

        self.LABEL53_copy = CTkLabel(master=self.FRAME52_copy, text="", width=70, height=70, fg_color=['#CF245E', '#cf245e'], corner_radius=3)
        self.LABEL53_copy.pack(side="left")

        self.LABEL54_copy = CTkLabel(master=self.FRAME52_copy, font=CTkFont(size=15), text="Daily Mix 4", anchor="w", text_color=['gray10', '#ffffff'])
        self.LABEL54_copy.pack(padx=(10, 1), expand=1, fill="x", side="left")

        self.FRAME55_copy = CTkFrame(master=self.FRAME51_copy, fg_color=['#c0c0c0', '#3a3a3a'], corner_radius=3, height=70)
        self.FRAME55_copy.pack(side="left", expand=1, fill="x", padx=(0, 20))

        self.LABEL56_copy = CTkLabel(master=self.FRAME55_copy, text="", width=70, height=70, fg_color=['#CF245E', '#cf245e'], corner_radius=3)
        self.LABEL56_copy.pack(side="left")

        self.LABEL57_copy = CTkLabel(master=self.FRAME55_copy, font=CTkFont(size=15), text="Daily Mix 5", anchor="w", text_color=['gray10', '#ffffff'])
        self.LABEL57_copy.pack(padx=(10, 1), expand=1, fill="x", side="left")

        self.FRAME58_copy = CTkFrame(master=self.FRAME51_copy, fg_color=['#c0c0c0', '#3a3a3a'], corner_radius=3, height=70)
        self.FRAME58_copy.pack(padx=(0, 0), expand=1, fill="x", side="left")

        self.LABEL59_copy = CTkLabel(master=self.FRAME58_copy, text="", width=70, height=70, fg_color=['#CF245E', '#cf245e'], corner_radius=3)
        self.LABEL59_copy.pack(side="left")

        self.LABEL60_copy = CTkLabel(master=self.FRAME58_copy, font=CTkFont(size=15), text="Daily Mix 6", anchor="w", text_color=['gray10', '#ffffff'])
        self.LABEL60_copy.pack(padx=(10, 1), expand=1, fill="x", side="left")

        self.FRAME60 = CTkFrame(master=self.SCROLLABLEFRAME24, height=356, fg_color="transparent")
        self.FRAME60.pack(pady=(20, 0), fill="x", padx=20)

        self.LABEL61 = CTkLabel(master=self.FRAME60, font=CTkFont(size=19), text="Your Frequent Plays", text_color=['gray10', '#ffffff'], anchor="w", height=27)
        self.LABEL61.pack(fill="x")

        self.SCROLLABLEFRAME62 = CTkScrollableFrame(master=self.FRAME60, orientation="horizontal", fg_color=['#dfdfdf', '#313131'], height=270)
        self.SCROLLABLEFRAME62.pack(pady=(10, 0), fill="x")

        self.FRAME63 = CTkFrame(master=self.SCROLLABLEFRAME62, fg_color=['#c0c0c0', '#3a3a3a'])
        self.FRAME63.pack(padx=(0, 20), expand=1, fill="y", pady=(0, 10), side="left")

        self.LABEL64 = CTkLabel(master=self.FRAME63, text="", width=180, height=180, fg_color=['#CF245E', '#cf245e'], corner_radius=4)
        self.LABEL64.pack(pady=(10, 0))

        self.LABEL65 = CTkLabel(master=self.FRAME63, font=CTkFont(size=15), text="Music 1", text_color=['gray10', '#ffffff'], anchor="w")
        self.LABEL65.pack(pady=(10, 0), fill="x", padx=(10, 0))

        self.LABEL67_copy = CTkLabel(master=self.FRAME63, font=CTkFont(size=13), text="Somebody", text_color=['gray10', '#a4a4a4'], anchor="w", height=14)
        self.LABEL67_copy.pack(pady=(0, 0), fill="x", padx=(10, 0))

        self.FRAME68_copy = CTkFrame(master=self.SCROLLABLEFRAME62, fg_color=['#c0c0c0', '#3a3a3a'])
        self.FRAME68_copy.pack(padx=(0, 20), expand=1, fill="y", pady=(0, 10), side="left")

        self.LABEL69_copy = CTkLabel(master=self.FRAME68_copy, text="", width=180, height=180, fg_color=['#CF245E', '#cf245e'], corner_radius=4)
        self.LABEL69_copy.pack(pady=(10, 0))

        self.LABEL70_copy = CTkLabel(master=self.FRAME68_copy, font=CTkFont(size=15), text="Music 2", text_color=['gray10', '#ffffff'], anchor="w")
        self.LABEL70_copy.pack(pady=(10, 0), fill="x", padx=(10, 0))

        self.LABEL71_copy = CTkLabel(master=self.FRAME68_copy, font=CTkFont(size=13), text="Somebody", text_color=['gray10', '#a4a4a4'], anchor="w", height=14)
        self.LABEL71_copy.pack(pady=(0, 0), fill="x", padx=(10, 0))

        self.FRAME72_copy = CTkFrame(master=self.SCROLLABLEFRAME62, fg_color=['#c0c0c0', '#3a3a3a'])
        self.FRAME72_copy.pack(padx=(0, 20), expand=1, fill="y", pady=(0, 10), side="left")

        self.LABEL73_copy = CTkLabel(master=self.FRAME72_copy, text="", width=180, height=180, fg_color=['#CF245E', '#cf245e'], corner_radius=4)
        self.LABEL73_copy.pack(pady=(10, 0))

        self.LABEL74_copy = CTkLabel(master=self.FRAME72_copy, font=CTkFont(size=15), text="Music 3", text_color=['gray10', '#ffffff'], anchor="w")
        self.LABEL74_copy.pack(pady=(10, 0), fill="x", padx=(10, 0))

        self.LABEL75_copy = CTkLabel(master=self.FRAME72_copy, font=CTkFont(size=13), text="Somebody", text_color=['gray10', '#a4a4a4'], anchor="w", height=14)
        self.LABEL75_copy.pack(pady=(0, 0), fill="x", padx=(10, 0))

        self.FRAME76_copy = CTkFrame(master=self.SCROLLABLEFRAME62, fg_color=['#c0c0c0', '#3a3a3a'])
        self.FRAME76_copy.pack(padx=(0, 20), expand=1, fill="y", pady=(0, 10), side="left")

        self.LABEL77_copy = CTkLabel(master=self.FRAME76_copy, text="", width=180, height=180, fg_color=['#CF245E', '#cf245e'], corner_radius=4)
        self.LABEL77_copy.pack(pady=(10, 0))

        self.LABEL78_copy = CTkLabel(master=self.FRAME76_copy, font=CTkFont(size=15), text="Music 4", text_color=['gray10', '#ffffff'], anchor="w")
        self.LABEL78_copy.pack(pady=(10, 0), fill="x", padx=(10, 0))

        self.LABEL79_copy = CTkLabel(master=self.FRAME76_copy, font=CTkFont(size=13), text="Somebody", text_color=['gray10', '#a4a4a4'], anchor="w", height=14)
        self.LABEL79_copy.pack(pady=(0, 0), fill="x", padx=(10, 0))

        self.FRAME80_copy = CTkFrame(master=self.SCROLLABLEFRAME62, fg_color=['#c0c0c0', '#3a3a3a'])
        self.FRAME80_copy.pack(padx=(0, 20), expand=1, fill="y", pady=(0, 10), side="left")

        self.LABEL81_copy = CTkLabel(master=self.FRAME80_copy, text="", width=180, height=180, fg_color=['#CF245E', '#cf245e'], corner_radius=4)
        self.LABEL81_copy.pack(pady=(10, 0))

        self.LABEL82_copy = CTkLabel(master=self.FRAME80_copy, font=CTkFont(size=15), text="Music 5", text_color=['gray10', '#ffffff'], anchor="w")
        self.LABEL82_copy.pack(pady=(10, 0), fill="x", padx=(10, 0))

        self.LABEL83_copy = CTkLabel(master=self.FRAME80_copy, font=CTkFont(size=13), text="Somebody", text_color=['gray10', '#a4a4a4'], anchor="w", height=14)
        self.LABEL83_copy.pack(pady=(0, 0), fill="x", padx=(10, 0))

        self.FRAME84_copy = CTkFrame(master=self.SCROLLABLEFRAME62, fg_color=['#c0c0c0', '#3a3a3a'])
        self.FRAME84_copy.pack(padx=(0, 20), expand=1, fill="y", pady=(0, 10), side="left")

        self.LABEL85_copy = CTkLabel(master=self.FRAME84_copy, text="", width=180, height=180, fg_color=['#CF245E', '#cf245e'], corner_radius=4)
        self.LABEL85_copy.pack(pady=(10, 0))

        self.LABEL86_copy = CTkLabel(master=self.FRAME84_copy, font=CTkFont(size=15), text="Music 6", text_color=['gray10', '#ffffff'], anchor="w")
        self.LABEL86_copy.pack(pady=(10, 0), fill="x", padx=(10, 0))

        self.LABEL87_copy = CTkLabel(master=self.FRAME84_copy, font=CTkFont(size=13), text="Somebody", text_color=['gray10', '#a4a4a4'], anchor="w", height=14)
        self.LABEL87_copy.pack(pady=(0, 0), fill="x", padx=(10, 0))

        self.FRAME88_copy = CTkFrame(master=self.SCROLLABLEFRAME62, fg_color=['#c0c0c0', '#3a3a3a'])
        self.FRAME88_copy.pack(padx=(0, 20), expand=1, fill="y", pady=(0, 10), side="left")

        self.LABEL89_copy = CTkLabel(master=self.FRAME88_copy, text="", width=180, height=180, fg_color=['#CF245E', '#cf245e'], corner_radius=4)
        self.LABEL89_copy.pack(pady=(10, 0))

        self.LABEL90_copy = CTkLabel(master=self.FRAME88_copy, font=CTkFont(size=15), text="Music 7", text_color=['gray10', '#ffffff'], anchor="w")
        self.LABEL90_copy.pack(pady=(10, 0), fill="x", padx=(10, 0))

        self.LABEL91_copy = CTkLabel(master=self.FRAME88_copy, font=CTkFont(size=13), text="Somebody", text_color=['gray10', '#a4a4a4'], anchor="w", height=14)
        self.LABEL91_copy.pack(pady=(0, 0), fill="x", padx=(10, 0))

        self.FRAME92_copy = CTkFrame(master=self.SCROLLABLEFRAME62, fg_color=['#c0c0c0', '#3a3a3a'])
        self.FRAME92_copy.pack(padx=(0, 20), expand=1, fill="y", pady=(0, 10), side="left")

        self.LABEL93_copy = CTkLabel(master=self.FRAME92_copy, text="", width=180, height=180, fg_color=['#CF245E', '#cf245e'], corner_radius=4)
        self.LABEL93_copy.pack(pady=(10, 0))

        self.LABEL94_copy = CTkLabel(master=self.FRAME92_copy, font=CTkFont(size=15), text="Music 8", text_color=['gray10', '#ffffff'], anchor="w")
        self.LABEL94_copy.pack(pady=(10, 0), fill="x", padx=(10, 0))

        self.LABEL95_copy = CTkLabel(master=self.FRAME92_copy, font=CTkFont(size=13), text="Somebody", text_color=['gray10', '#a4a4a4'], anchor="w", height=14)
        self.LABEL95_copy.pack(pady=(0, 0), fill="x", padx=(10, 0))

        self.FRAME96_copy = CTkFrame(master=self.SCROLLABLEFRAME62, fg_color=['#c0c0c0', '#3a3a3a'])
        self.FRAME96_copy.pack(padx=(0, 20), expand=1, fill="y", pady=(0, 10), side="left")

        self.LABEL97_copy = CTkLabel(master=self.FRAME96_copy, text="", width=180, height=180, fg_color=['#CF245E', '#cf245e'], corner_radius=4)
        self.LABEL97_copy.pack(pady=(10, 0))

        self.LABEL98_copy = CTkLabel(master=self.FRAME96_copy, font=CTkFont(size=15), text="Music 9", text_color=['gray10', '#ffffff'], anchor="w")
        self.LABEL98_copy.pack(pady=(10, 0), fill="x", padx=(10, 0))

        self.LABEL99_copy = CTkLabel(master=self.FRAME96_copy, font=CTkFont(size=13), text="Somebody", text_color=['gray10', '#a4a4a4'], anchor="w", height=14)
        self.LABEL99_copy.pack(pady=(0, 0), fill="x", padx=(10, 0))

        self.FRAME100_copy = CTkFrame(master=self.SCROLLABLEFRAME62, fg_color=['#c0c0c0', '#3a3a3a'])
        self.FRAME100_copy.pack(padx=(0, 20), expand=1, fill="y", pady=(0, 10), side="left")

        self.LABEL101_copy = CTkLabel(master=self.FRAME100_copy, text="", width=180, height=180, fg_color=['#CF245E', '#cf245e'], corner_radius=4)
        self.LABEL101_copy.pack(pady=(10, 0))

        self.LABEL102_copy = CTkLabel(master=self.FRAME100_copy, font=CTkFont(size=15), text="Music 10", text_color=['gray10', '#ffffff'], anchor="w")
        self.LABEL102_copy.pack(pady=(10, 0), fill="x", padx=(10, 0))

        self.LABEL103_copy = CTkLabel(master=self.FRAME100_copy, font=CTkFont(size=13), text="Somebody", text_color=['gray10', '#a4a4a4'], anchor="w", height=14)
        self.LABEL103_copy.pack(pady=(0, 0), fill="x", padx=(10, 0))

        self.FRAME104_copy = CTkFrame(master=self.SCROLLABLEFRAME24, height=356, fg_color="transparent")
        self.FRAME104_copy.pack(pady=(20, 0), fill="x", padx=20)

        self.LABEL105_copy = CTkLabel(master=self.FRAME104_copy, font=CTkFont(size=19), text="Top 10 International", text_color=['gray10', '#ffffff'], anchor="w", height=27)
        self.LABEL105_copy.pack(fill="x")

        self.SCROLLABLEFRAME106_copy = CTkScrollableFrame(master=self.FRAME104_copy, orientation="horizontal", fg_color=['#dfdfdf', '#313131'], height=270)
        self.SCROLLABLEFRAME106_copy.pack(pady=(10, 0), fill="x")

        self.FRAME107_copy = CTkFrame(master=self.SCROLLABLEFRAME106_copy, fg_color=['#c0c0c0', '#3a3a3a'])
        self.FRAME107_copy.pack(padx=(0, 20), expand=1, fill="y", pady=(0, 10), side="left")

        self.LABEL108_copy = CTkLabel(master=self.FRAME107_copy, text="", width=180, height=180, fg_color=['#CF245E', '#cf245e'], corner_radius=4)
        self.LABEL108_copy.pack(pady=(10, 0))

        self.LABEL109_copy = CTkLabel(master=self.FRAME107_copy, font=CTkFont(size=15), text="Music 1", text_color=['gray10', '#ffffff'], anchor="w")
        self.LABEL109_copy.pack(pady=(10, 0), fill="x", padx=(10, 0))

        self.LABEL110_copy = CTkLabel(master=self.FRAME107_copy, font=CTkFont(size=13), text="Somebody", text_color=['gray10', '#a4a4a4'], anchor="w", height=14)
        self.LABEL110_copy.pack(pady=(0, 0), fill="x", padx=(10, 0))

        self.FRAME111_copy = CTkFrame(master=self.SCROLLABLEFRAME106_copy, fg_color=['#c0c0c0', '#3a3a3a'])
        self.FRAME111_copy.pack(padx=(0, 20), expand=1, fill="y", pady=(0, 10), side="left")

        self.LABEL112_copy = CTkLabel(master=self.FRAME111_copy, text="", width=180, height=180, fg_color=['#CF245E', '#cf245e'], corner_radius=4)
        self.LABEL112_copy.pack(pady=(10, 0))

        self.LABEL113_copy = CTkLabel(master=self.FRAME111_copy, font=CTkFont(size=15), text="Music 2", text_color=['gray10', '#ffffff'], anchor="w")
        self.LABEL113_copy.pack(pady=(10, 0), fill="x", padx=(10, 0))

        self.LABEL114_copy = CTkLabel(master=self.FRAME111_copy, font=CTkFont(size=13), text="Somebody", text_color=['gray10', '#a4a4a4'], anchor="w", height=14)
        self.LABEL114_copy.pack(pady=(0, 0), fill="x", padx=(10, 0))

        self.FRAME115_copy = CTkFrame(master=self.SCROLLABLEFRAME106_copy, fg_color=['#c0c0c0', '#3a3a3a'])
        self.FRAME115_copy.pack(padx=(0, 20), expand=1, fill="y", pady=(0, 10), side="left")

        self.LABEL116_copy = CTkLabel(master=self.FRAME115_copy, text="", width=180, height=180, fg_color=['#CF245E', '#cf245e'], corner_radius=4)
        self.LABEL116_copy.pack(pady=(10, 0))

        self.LABEL117_copy = CTkLabel(master=self.FRAME115_copy, font=CTkFont(size=15), text="Music 3", text_color=['gray10', '#ffffff'], anchor="w")
        self.LABEL117_copy.pack(pady=(10, 0), fill="x", padx=(10, 0))

        self.LABEL118_copy = CTkLabel(master=self.FRAME115_copy, font=CTkFont(size=13), text="Somebody", text_color=['gray10', '#a4a4a4'], anchor="w", height=14)
        self.LABEL118_copy.pack(pady=(0, 0), fill="x", padx=(10, 0))

        self.FRAME119_copy = CTkFrame(master=self.SCROLLABLEFRAME106_copy, fg_color=['#c0c0c0', '#3a3a3a'])
        self.FRAME119_copy.pack(padx=(0, 20), expand=1, fill="y", pady=(0, 10), side="left")

        self.LABEL120_copy = CTkLabel(master=self.FRAME119_copy, text="", width=180, height=180, fg_color=['#CF245E', '#cf245e'], corner_radius=4)
        self.LABEL120_copy.pack(pady=(10, 0))

        self.LABEL121_copy = CTkLabel(master=self.FRAME119_copy, font=CTkFont(size=15), text="Music 4", text_color=['gray10', '#ffffff'], anchor="w")
        self.LABEL121_copy.pack(pady=(10, 0), fill="x", padx=(10, 0))

        self.LABEL122_copy = CTkLabel(master=self.FRAME119_copy, font=CTkFont(size=13), text="Somebody", text_color=['gray10', '#a4a4a4'], anchor="w", height=14)
        self.LABEL122_copy.pack(pady=(0, 0), fill="x", padx=(10, 0))

        self.FRAME123_copy = CTkFrame(master=self.SCROLLABLEFRAME106_copy, fg_color=['#c0c0c0', '#3a3a3a'])
        self.FRAME123_copy.pack(padx=(0, 20), expand=1, fill="y", pady=(0, 10), side="left")

        self.LABEL124_copy = CTkLabel(master=self.FRAME123_copy, text="", width=180, height=180, fg_color=['#CF245E', '#cf245e'], corner_radius=4)
        self.LABEL124_copy.pack(pady=(10, 0))

        self.LABEL125_copy = CTkLabel(master=self.FRAME123_copy, font=CTkFont(size=15), text="Music 5", text_color=['gray10', '#ffffff'], anchor="w")
        self.LABEL125_copy.pack(pady=(10, 0), fill="x", padx=(10, 0))

        self.LABEL126_copy = CTkLabel(master=self.FRAME123_copy, font=CTkFont(size=13), text="Somebody", text_color=['gray10', '#a4a4a4'], anchor="w", height=14)
        self.LABEL126_copy.pack(pady=(0, 0), fill="x", padx=(10, 0))

        self.FRAME127_copy = CTkFrame(master=self.SCROLLABLEFRAME106_copy, fg_color=['#c0c0c0', '#3a3a3a'])
        self.FRAME127_copy.pack(padx=(0, 20), expand=1, fill="y", pady=(0, 10), side="left")

        self.LABEL128_copy = CTkLabel(master=self.FRAME127_copy, text="", width=180, height=180, fg_color=['#CF245E', '#cf245e'], corner_radius=4)
        self.LABEL128_copy.pack(pady=(10, 0))

        self.LABEL129_copy = CTkLabel(master=self.FRAME127_copy, font=CTkFont(size=15), text="Music 6", text_color=['gray10', '#ffffff'], anchor="w")
        self.LABEL129_copy.pack(pady=(10, 0), fill="x", padx=(10, 0))

        self.LABEL130_copy = CTkLabel(master=self.FRAME127_copy, font=CTkFont(size=13), text="Somebody", text_color=['gray10', '#a4a4a4'], anchor="w", height=14)
        self.LABEL130_copy.pack(pady=(0, 0), fill="x", padx=(10, 0))

        self.FRAME131_copy = CTkFrame(master=self.SCROLLABLEFRAME106_copy, fg_color=['#c0c0c0', '#3a3a3a'])
        self.FRAME131_copy.pack(padx=(0, 20), expand=1, fill="y", pady=(0, 10), side="left")

        self.LABEL132_copy = CTkLabel(master=self.FRAME131_copy, text="", width=180, height=180, fg_color=['#CF245E', '#cf245e'], corner_radius=4)
        self.LABEL132_copy.pack(pady=(10, 0))

        self.LABEL133_copy = CTkLabel(master=self.FRAME131_copy, font=CTkFont(size=15), text="Music 7", text_color=['gray10', '#ffffff'], anchor="w")
        self.LABEL133_copy.pack(pady=(10, 0), fill="x", padx=(10, 0))

        self.LABEL134_copy = CTkLabel(master=self.FRAME131_copy, font=CTkFont(size=13), text="Somebody", text_color=['gray10', '#a4a4a4'], anchor="w", height=14)
        self.LABEL134_copy.pack(pady=(0, 0), fill="x", padx=(10, 0))

        self.FRAME135_copy = CTkFrame(master=self.SCROLLABLEFRAME106_copy, fg_color=['#c0c0c0', '#3a3a3a'])
        self.FRAME135_copy.pack(padx=(0, 20), expand=1, fill="y", pady=(0, 10), side="left")

        self.LABEL136_copy = CTkLabel(master=self.FRAME135_copy, text="", width=180, height=180, fg_color=['#CF245E', '#cf245e'], corner_radius=4)
        self.LABEL136_copy.pack(pady=(10, 0))

        self.LABEL137_copy = CTkLabel(master=self.FRAME135_copy, font=CTkFont(size=15), text="Music 8", text_color=['gray10', '#ffffff'], anchor="w")
        self.LABEL137_copy.pack(pady=(10, 0), fill="x", padx=(10, 0))

        self.LABEL138_copy = CTkLabel(master=self.FRAME135_copy, font=CTkFont(size=13), text="Somebody", text_color=['gray10', '#a4a4a4'], anchor="w", height=14)
        self.LABEL138_copy.pack(pady=(0, 0), fill="x", padx=(10, 0))

        self.FRAME139_copy = CTkFrame(master=self.SCROLLABLEFRAME106_copy, fg_color=['#c0c0c0', '#3a3a3a'])
        self.FRAME139_copy.pack(padx=(0, 20), expand=1, fill="y", pady=(0, 10), side="left")

        self.LABEL140_copy = CTkLabel(master=self.FRAME139_copy, text="", width=180, height=180, fg_color=['#CF245E', '#cf245e'], corner_radius=4)
        self.LABEL140_copy.pack(pady=(10, 0))

        self.LABEL141_copy = CTkLabel(master=self.FRAME139_copy, font=CTkFont(size=15), text="Music 9", text_color=['gray10', '#ffffff'], anchor="w")
        self.LABEL141_copy.pack(pady=(10, 0), fill="x", padx=(10, 0))

        self.LABEL142_copy = CTkLabel(master=self.FRAME139_copy, font=CTkFont(size=13), text="Somebody", text_color=['gray10', '#a4a4a4'], anchor="w", height=14)
        self.LABEL142_copy.pack(pady=(0, 0), fill="x", padx=(10, 0))

        self.FRAME143_copy = CTkFrame(master=self.SCROLLABLEFRAME106_copy, fg_color=['#c0c0c0', '#3a3a3a'])
        self.FRAME143_copy.pack(padx=(0, 20), expand=1, fill="y", pady=(0, 10), side="left")

        self.LABEL144_copy = CTkLabel(master=self.FRAME143_copy, text="", width=180, height=180, fg_color=['#CF245E', '#cf245e'], corner_radius=4)
        self.LABEL144_copy.pack(pady=(10, 0))

        self.LABEL145_copy = CTkLabel(master=self.FRAME143_copy, font=CTkFont(size=15), text="Music 10", text_color=['gray10', '#ffffff'], anchor="w")
        self.LABEL145_copy.pack(pady=(10, 0), fill="x", padx=(10, 0))

        self.LABEL146_copy = CTkLabel(master=self.FRAME143_copy, font=CTkFont(size=13), text="Somebody", text_color=['gray10', '#a4a4a4'], anchor="w", height=14)
        self.LABEL146_copy.pack(pady=(0, 0), fill="x", padx=(10, 0))

        self.playbar = CTkFrame(master=self, height=100, fg_color=['#9f9f9f', '#161616'], corner_radius=0)
        self.playbar.pack(fill="x")

        self.FRAME2 = CTkFrame(master=self.playbar, width=200, height=75, fg_color="transparent")
        self.FRAME2.pack(pady=(5, 5), padx=5, side="left")

        self.LABEL5 = CTkLabel(master=self.FRAME2, text="", width=60, fg_color=['#CF245E', '#cf245e'], height=60, corner_radius=3)
        self.LABEL5.pack(padx=(5, 0), side="left")

        self.FRAME6 = CTkFrame(master=self.FRAME2, height=20, width=153, fg_color="transparent")
        self.FRAME6.pack(padx=(15, 5), expand=1, side="left")

        self.LABEL7 = CTkLabel(master=self.FRAME6, font=CTkFont(size=15), text="Music 1", anchor="w", height=2, text_color=['gray10', '#ffffff'])
        self.LABEL7.pack(fill="x")

        self.LABEL9_copy = CTkLabel(master=self.FRAME6, font=CTkFont(size=11), text="Somebody", compound="top", anchor="w", height=15, text_color=['gray10', '#ffffff'])
        self.LABEL9_copy.pack(fill="x")

        self.BUTTON9 = CTkButton(master=self.FRAME2, text="", width=30, height=30, image=CTkImage(Image.open(
            r"Assets/baseline_favorite_border_(255, 255, 255)_18dp_1x.png"), size=(18, 18)), fg_color="transparent", hover=False)
        self.BUTTON9.pack(padx=(0, 10), side="left")

        self.FRAME4_copy = CTkFrame(master=self.playbar, width=219, height=75, fg_color="transparent")
        self.FRAME4_copy.pack(side="right", padx=5, pady=5)

        self.BUTTON20 = CTkButton(master=self.FRAME4_copy, text="", width=35, height=35, image=CTkImage(Image.open(
            r"Assets/baseline_open_in_full_(255, 255, 255)_18dp_1x.png"), size=(18, 18)), fg_color="transparent", hover_color=['#ae1d4f', '#ae1d4f'])
        self.BUTTON20.pack(side="right")

        self.SLIDER24_copy = CTkSlider(master=self.FRAME4_copy, from_=0, to=100, number_of_steps=100, orientation="horizontal", button_length=0, button_corner_radius=2, button_color=['#cf245e', '#cf245e'], button_hover_color=['#ae1d4f', '#ae1d4f'], width=100)
        self.SLIDER24_copy.pack(side="right", expand=1, fill="x")

        self.BUTTON25_copy = CTkButton(master=self.FRAME4_copy, text="", width=35, height=35, image=CTkImage(Image.open(
            r"Assets/baseline_volume_up_(255, 255, 255)_18dp_1x.png"), size=(18, 18)), fg_color="transparent", hover_color=['#ae1d4f', '#ae1d4f'])
        self.BUTTON25_copy.pack(side="right")

        self.FRAME5_copy = CTkFrame(master=self.playbar, width=200, height=100, fg_color="transparent", bg_color="transparent")
        self.FRAME5_copy.pack(expand=True, fill="x", padx=5, pady=5, side="left")

        self.scrubber_frame = CTkFrame(master=self.FRAME5_copy, width=176, height=34, fg_color="transparent")
        self.scrubber_frame.pack(pady=(0, 5), fill="x", padx=10, side="bottom")

        self.time_indicator = CTkLabel(master=self.scrubber_frame, text="0:00", text_color=['gray10', '#ffffff'])
        self.time_indicator.pack(side="left")

        self.LABEL13_copy = CTkLabel(master=self.scrubber_frame, text="3:38", text_color=['gray10', '#ffffff'])
        self.LABEL13_copy.pack(side="right")

        self.SLIDER13 = CTkSlider(master=self.scrubber_frame, from_=0, to=202, number_of_steps=202, orientation="horizontal", button_length=0, button_corner_radius=2, button_color=['#cf245e', '#cf245e'], button_hover_color=['#ae1d4f', '#ae1d4f'])
        self.SLIDER13.pack(expand=True, fill="x")

        self.FRAME14 = CTkFrame(master=self.FRAME5_copy, fg_color="transparent")
        self.FRAME14.pack(expand=1, padx=5, pady=(5, 0))

        self.BUTTON15 = CTkButton(master=self.FRAME14, text="", width=40, height=40, corner_radius=6, image=CTkImage(Image.open(
            r"Assets/baseline_shuffle_(255, 255, 255)_18dp_1x.png"), size=(18, 18)), fg_color="transparent", hover_color=['#ae1d4f', '#ae1d4f'])
        self.BUTTON15.pack(side="left")

        self.BUTTON17_copy = CTkButton(master=self.FRAME14, text="", width=40, height=40, corner_radius=6, image=CTkImage(Image.open(
            r"Assets/baseline_skip_previous_(255, 255, 255)_18dp_1x.png"), size=(18, 18)), fg_color="transparent", hover_color=['#ae1d4f', '#ae1d4f'], border_width=0)
        self.BUTTON17_copy.pack(padx=(10, 0), side="left")

        self.BUTTON18_copy = CTkButton(master=self.FRAME14, font=CTkFont(overstrike=False), text="", width=40, height=40, corner_radius=6, image=CTkImage(Image.open(
            r"Assets/baseline_play_arrow_(255, 255, 255)_18dp_1x.png"), size=(18, 18)), fg_color=['#cf245e', '#cf245e'], hover_color=['#ae1d4f', '#ae1d4f'])
        self.BUTTON18_copy.pack(padx=(10, 0), side="left")

        self.BUTTON19_copy = CTkButton(master=self.FRAME14, font=CTkFont(overstrike=False), text="", width=40, height=40, corner_radius=6, image=CTkImage(Image.open(
            r"Assets/baseline_skip_next_(255, 255, 255)_18dp_1x.png"), size=(18, 18)), fg_color="transparent", hover_color=['#ae1d4f', '#ae1d4f'])
        self.BUTTON19_copy.pack(padx=(10, 0), side="left")

        self.BUTTON20_copy = CTkButton(master=self.FRAME14, font=CTkFont(overstrike=False), text="", width=40, height=40, corner_radius=6, image=CTkImage(Image.open(
            r"Assets/baseline_repeat_(255, 255, 255)_18dp_1x.png"), size=(18, 18)), fg_color="transparent", hover_color=['#ae1d4f', '#ae1d4f'])
        self.BUTTON20_copy.pack(padx=(10, 0), side="left")

        
set_default_color_theme("green")
root = App()
root.geometry("1365x770")
root.title("Custom Tkinter Builder- Spotify Demo")
root.configure(fg_color=['gray92', 'gray14'])
root.mainloop()
            
