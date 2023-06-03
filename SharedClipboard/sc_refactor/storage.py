import json
import os


def save_data(_file_path, _data):
    with open(_file_path, "w") as f:
        try:
            json.dump(_data, f)
        except json.JSONDecodeError:
            if os.path.isfile(SAVED_DATA):
                os.remove(SAVED_DATA)


def load_data(_file_path):
    try:
        with open(_file_path, "r") as f:
            _data = json.load(f)
            return _data
    except FileNotFoundError:
        return {}
