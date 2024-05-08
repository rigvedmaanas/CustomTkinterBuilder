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
        base_path = os.path.dirname(base_path)
        base_path = os.path.dirname(base_path)
        base_path = os.path.dirname(base_path)

    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, path)
