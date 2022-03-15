import sys
from os import getenv
from pathlib import Path


def user_data_dir():
    if sys.platform.startswith("win"):
        os_path = getenv("LOCALAPPDATA")
    elif sys.platform.startswith("darwin"):
        os_path = "~/Library/Application Support"
    else:
        # linux
        os_path = getenv("XDG_DATA_HOME", "~/.local/share")

    path = Path(os_path).expanduser() / "HouseBot"
    path.mkdir(parents=True, exist_ok=True)

    return path


def get_user_data_file_path(file_name):
    file_path = user_data_dir() / file_name
    file_path.touch(exist_ok=True)
    return file_path
