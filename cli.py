import argparse
import subprocess
import sys
from get_path import APP_NAME


def update_package():
    command = [sys.executable, "-m", "pip", "install", "--upgrade", APP_NAME]
    try:
        subprocess.check_call(command)
        print("CustomTkinterBuilder updated successfully.")
        return 0
    except subprocess.CalledProcessError as error:
        print(f"Update failed (exit code {error.returncode}). Please run the command manually:")
        print(" ".join(command))
        return error.returncode


def main():
    parser = argparse.ArgumentParser(prog="customtkinterbuilder")
    parser.add_argument("--update", action="store_true", help="Update CustomTkinterBuilder to the latest version")
    args = parser.parse_args()

    if args.update:
        raise SystemExit(update_package())

    from WelcomePage import launch
    launch()


if __name__ == "__main__":
    main()
