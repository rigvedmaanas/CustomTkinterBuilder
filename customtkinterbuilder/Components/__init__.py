import os
import importlib
import inspect

__all__ = []

current_dir = os.path.dirname(__file__)

for filename in os.listdir(current_dir):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = filename[:-3]
        full_module_name = f"{__name__}.{module_name}"

        module = importlib.import_module(full_module_name)

        for name, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ == full_module_name:
                globals()[name] = obj
                __all__.append(name)
