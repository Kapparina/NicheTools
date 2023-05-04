import sys
import pyperclip as clipboard
import json
import textwrap
import os

SAVED_DATA = f"{os.getcwd()}/clipboard.json"


def save_data(_file_path, _data):
    with open(_file_path, "w") as f:
        json.dump(_data, f)


def load_data(_file_path):
    try:
        with open(_file_path, "r") as f:
            _data = json.load(f)
            return _data
    except FileNotFoundError:
        return {}


if len(sys.argv) == 2:
    command = sys.argv[1]
    data = load_data(SAVED_DATA)

    if command == "help" or command == "?":
        print(textwrap.dedent(f"""
            This application allows for persistent storage of clipboard contents, catering to various use-cases.
            Upon storing a value, a 'clipboard.json' file will be created in the same directory as the application.
            When the 'clear' command is used, the 'clipboard.json' file will be deleted.

            Available commands include:
            | 'save' or 's' or 'p' (ie: CTRL + V): Saves/pastes the contents of your clipboard.
            | 'load' or 'l' or 'c' (ie: CTRL + C): Loads/copies the value of a specified key to your clipboard.
            | 'all' or 'a' (ie: 'see all'): Lists the currently stored items.
            | 'delete' or 'd' (ie: 'remove'): Deletes/removes the value at the specified key from storage.
            | 'wipe' or 'w' (ie: 'wipe'): Clears/wipes all data previously stored.

            E.g. if running as executable, wishing to save:
            | <filename (default: sharedclipboard)>.exe save
            Or:
            | <filename (default: sharedclipboard)> save

            If running from Python script, wishing to load:
            | <filename (default: sharedclipboard>.py load
            """))

    elif command == "save" or command == "s" or command == "p":
        key = input("Enter a key: ")
        data[key] = clipboard.paste()
        print(f"Value stored at key: '{key}'.")
        save_data(SAVED_DATA, data)

    elif command == "load" or command == "l" or command == "c":
        key = input("Enter a key: ")

        if key in data:
            clipboard.copy(data[key])
            print("Key value copied to clipboard.")
        else:
            print("Key does not exist.")

    elif command == "list" or command == "a":
        if len(data.keys()) < 1:
            print("No values to list.")
        else:
            for key, value in data.items():
                print(f"| {key}: {value}")

    elif command == "delete" or command == "d":
        key = input("Enter a key to be deleted: ")
        print(f"Deleting {key} from persistent clipboard...")
        data.pop(key)
        save_data(SAVED_DATA, data)

    elif command == "clear" or command == "w":
        print("Would you like to clear all stored values?")
        key = input("Y/N: ")

        if key.casefold() == "y":
            data.clear()
            print("Stored items cleared...")
            save_data(SAVED_DATA, data)
            os.remove(SAVED_DATA)

        else:
            print("Retaining currently stored items.")
    else:
        print("Unknown command.")

else:
    print("Please provide a command, or type 'help' or '?' for a list of commands.")
