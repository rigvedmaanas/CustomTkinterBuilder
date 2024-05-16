import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def tempify(path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS

        # From - '/Users/######/Build/CustomTkinterBuilder Release/Custom Tkinter Builder.app/Contents'
        # To - ''/Users/######/Build/CustomTkinterBuilder Release/'
        if sys.platform == "darwin":
            base_path = os.path.dirname(base_path)
            base_path = os.path.dirname(base_path)
            base_path = os.path.dirname(base_path)
        elif sys.platform.startswith("win"):
            print(base_path)
            base_path = os.path.dirname(base_path)


    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, path)

def joinpath(rootdir, targetdir):
    return os.path.join(rootdir, targetdir)

escape_dict={'\a':r'\a',
           '\b':r'\b',
           '\c':r'\c',
           '\f':r'\f',
           '\n':r'\n',
           '\r':r'\r',
           '\t':r'\t',
           '\v':r'\v',
           '\'':r'\'',
           '\"':r'\"',
           '\0':r'\0',
           '\1':r'\1',
           '\2':r'\2',
           '\3':r'\3',
           '\4':r'\4',
           '\5':r'\5',
           '\6':r'\6',
           '\7':r'\7',
           '\8':r'\8',
           '\9':r'\9'}

def rawify(text):
    """Returns a raw string representation of text"""
    new_string=''
    for char in text:
        try:
            new_string += escape_dict[char]
        except KeyError:
            new_string += char
    return new_string
