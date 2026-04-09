import sys
import os
import shutil
import json
import tempfile

APP_NAME = "CustomTkinterBuilder"

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    candidate_base_paths = []
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        candidate_base_paths.append(sys._MEIPASS)
    except Exception:
        pass

    candidate_base_paths.extend([
        os.path.dirname(os.path.abspath(__file__)),
        os.path.abspath("."),
        os.path.join(sys.prefix, "share", APP_NAME),
    ])

    for base_path in candidate_base_paths:
        path = os.path.join(base_path, relative_path)
        if os.path.exists(path):
            return path

    return os.path.join(candidate_base_paths[0], relative_path)

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
        base_path = os.path.join(tempfile.gettempdir(), APP_NAME)
        os.makedirs(base_path, exist_ok=True)

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


def get_config_directory():
    if sys.platform.startswith("win"):
        root = os.getenv("APPDATA") or os.path.join(os.path.expanduser("~"), "AppData", "Roaming")
    else:
        root = os.getenv("XDG_CONFIG_HOME") or os.path.join(os.path.expanduser("~"), ".config")

    config_dir = os.path.join(root, APP_NAME)
    os.makedirs(config_dir, exist_ok=True)
    return config_dir


def get_settings_path(filename="config.json"):
    settings_path = os.path.join(get_config_directory(), filename)

    if not os.path.exists(settings_path):
        default_config = resource_path(filename)
        if os.path.exists(default_config):
            shutil.copy2(default_config, settings_path)
        else:
            with open(settings_path, "w", encoding="utf-8") as f:
                f.write(json.dumps({"project_files": []}, indent=4))

    return settings_path
