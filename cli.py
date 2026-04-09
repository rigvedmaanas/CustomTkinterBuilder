import argparse
import subprocess
import sys


def update_package():
    package_name = "CustomTkinterBuilder"
    command = [sys.executable, "-m", "pip", "install", "--upgrade", package_name]
    subprocess.check_call(command)


def main():
    parser = argparse.ArgumentParser(prog="customtkinterbuilder")
    parser.add_argument("--update", action="store_true", help="Update CustomTkinterBuilder to the latest version")
    args = parser.parse_args()

    if args.update:
        update_package()
        return

    from WelcomePage import launch
    launch()


if __name__ == "__main__":
    main()
