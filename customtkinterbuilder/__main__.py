from .WelcomePage import run
import argparse
import os
import subprocess
import sys
import shutil

def main():
    parser = argparse.ArgumentParser(description="CustomTkinterBuilder Software")
    parser.add_argument(
        "command",
        nargs="?",
        default=None,
        help="Choose from: temp, config, upgrade"
    )

    parser.add_argument(
        "--new_config",
        type=os.path.abspath,
        help="Absolute path to a new config file"
    )

    args = parser.parse_args()

    if args.command == "temp":
        print("Creating temp directory!")
        try:
            os.mkdir("temp")
        except FileExistsError:
            print("temp directory exists!!")


    if args.command == "upgrade":
        config_backup_path = "./customtkinterbuilder/config.json"
        if os.path.exists(config_backup_path):
            shutil.copy(config_backup_path, "config_backup.json")
            print("🔁 Backed up config.json")

        print("⬆️ Upgrading CustomTkinterBuilder...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "customtkinterbuilder"])

        if os.path.exists("config_backup.json"):
            os.makedirs("customtkinterbuilder", exist_ok=True)
            shutil.move("config_backup.json", config_backup_path)
            print("✅ Restored config.json after upgrade")

        sys.exit(0)

    print("🚀 Running CustomTkinterBuilder")
    print("Note: If the software crashes with the error \"temp not found\", try running the following command to resolve it: customtkinterbuilder temp")
    run()


if __name__ == "__main__":
    main()
