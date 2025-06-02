import setuptools
import re

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def get_version():
    with open("customtkinterbuilder/__init__.py") as f:
        content = f.read()
    version_match = re.search(r'^__version__ = ["\']([^"\']*)["\']', content, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

def parse_requirements(filename):
    with open(filename) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


setuptools.setup(
    name="customtkinterbuilder",
    version=get_version(),
    author="Rigved Maanas M",
    author_email="rigvedmaanas@gmail.com",
    description="This is a Free and Open Source RAD tool for Custom Tkinter. This software allows you to create complex UI faster than ever⚡",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rigvedmaanas/CustomTkinterBuilder",
    project_urls={
        "Bug Tracker": "https://github.com/rigvedmaanas/CustomTkinterBuilder/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "CustomTkinterBuilder=customtkinterbuilder.__main__:main",
        ],
    },
    install_requires=parse_requirements("requirements.txt")
)
