import pyperclip as clipboard
from tabulate import tabulate
import json
import textwrap
import os
import time

tabulate.PRESERVE_WHITESPACE = True


SAVED_DATA = f"{os.getcwd()}/clipboard.json"


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


def tabulated_data(_data):
    formatted_data = {"KEY": [key for key in _data.keys()],
                      "VALUE": [value for value in _data.values()]}
    data_table = tabulate(formatted_data, headers=["KEYS", "VALUES"],
                          tablefmt="grid", maxcolwidths=[1, 15, 50],
                          showindex=range(1, len([item for item in formatted_data["KEY"]]) + 1))
    return data_table


def blurb():
    print(textwrap.dedent(f"""
        _________________________________________________
        This application allows for persistent storage of 
        clipboard contents, catering to various use cases.
        
        Upon storing a value, a 'clipboard.json' file will 
        be created in the same directory as the application
        (if such a file doesn't already exist).
        
        Upon quitting (via 'quit'), you will be asked
        if the 'clipboard.json' should be deleted.
        
        For commands, type 'help' or '?'.
        _________________________________________________
        """))


def help_text():
    print(textwrap.dedent(f"""
        _________________________________________________
        Available commands include:
        |> 'save' (ie: CTRL + V): 
        | Saves/pastes the contents of your clipboard.
        
        |> 'load' (ie: CTRL + C): 
        | Loads/copies the value of a specified key to your clipboard.
        
        |> 'all' (ie: 'see all'): 
        | Lists the currently stored items.
        
        |> 'delete' (ie: 'remove'): 
        | Deletes/removes the value at the specified key from storage.
        
        |> 'wipe' (ie: 'clear'): 
        | Clears/wipes all data previously stored.
        
        |> 'quit' (ie: 'exit'):
        | Exits the application after asking whether to clean up. 
        _________________________________________________
        """))


def main(_command):
    if _command == "save" or _command == "s" or _command == "p":
        key = input("Enter a key to save the value against: ")
        data[key] = clipboard.paste()
        print(f"Value stored at key: '{key}'.")
        save_data(SAVED_DATA, data)

    elif _command == "load" or _command == "l" or _command == "c":
        key = input("Enter a key to be loaded: ")
        if key in data:
            clipboard.copy(data[key])
            print(f"'{key}' value copied to clipboard!")
        else:
            print("Key does not exist!")

    elif _command == "all" or _command == "a" or _command == "list":
        if len(data.keys()) < 1:
            print("No values available to list!")
        else:
            print(f"\n{tabulated_data(data)}\n")

    elif _command == "delete" or _command == "d":
        key = input("Enter a key to be deleted: ")
        print(f"Deleting '{key}' from persistent clipboard...")
        data.pop(key)
        save_data(SAVED_DATA, data)
        print(f"'{key}' deleted successfully!")

    elif _command == "wipe" or _command == "w":
        print("Are you sure you like to clear all stored values?")
        key = input("Y/N |> ")
        if key.casefold() == "y":
            print("Clearing stored items...")
            data.clear()
            print("Stored items cleared successfully!")
            save_data(SAVED_DATA, data)
        else:
            print("Retaining currently stored items...")

    elif _command == "":
        print("Please provide a command, or type 'help' or '?' for a list of commands.")

    elif _command == "help" or _command == "?":
        help_text()

    else:
        print("Unknown command!")


def clear_on_exit():
    print("Would you like to clear stored values before exiting?")
    confirmation = input("Y/N |> ")

    if confirmation.casefold() == "y":
        print(f"Deleting {SAVED_DATA}...")
        os.remove(SAVED_DATA)
        print(f"Values stored in {SAVED_DATA} deleted successfully!")
    else:
        print("Retaining stored values...")


blurb()

print("Please enter a command: ")
while True:
    user_command = input("|> ").casefold()
    if user_command == "q" or user_command == "quit":
        clear_on_exit()
        print("Quitting application...")
        time.sleep(1)
        break
    else:
        data = load_data(SAVED_DATA)
        main(user_command)
