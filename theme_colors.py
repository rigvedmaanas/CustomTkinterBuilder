import json
import os

from get_path import resource_path

_COLORS_CACHE = None


def _load_colors():
    global _COLORS_CACHE
    if _COLORS_CACHE is None:
        with open(resource_path(os.path.join("ThemeAssets", "ui_colors.json")), "r", encoding="utf-8") as color_file:
            _COLORS_CACHE = json.load(color_file)
    return _COLORS_CACHE


def get_ui_color(key):
    colors = _load_colors()
    if key not in colors:
        raise KeyError(f"Color key '{key}' not found in ThemeAssets/ui_colors.json")
    return colors[key]
