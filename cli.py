import argparse
import subprocess
import sys


def update_package():
    package_name = "CustomTkinterBuilder"
    command = [sys.executable, "-m", "pip", "install", "--upgrade", package_name]
    try:
        subprocess.check_call(command)
        print("CustomTkinterBuilder updated successfully.")
    except subprocess.CalledProcessError as error:
        print(f"Update failed (exit code {error.returncode}). Please run the command manually:")
        print(" ".join(command))
        raise SystemExit(error.returncode) from error


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
