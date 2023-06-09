import pyperclip as clipboard
from tabulate import tabulate
import json
import textwrap
import os
import sys
import time
import shutil

tabulate.PRESERVE_WHITESPACE = True

SAVED_DATA = f"{os.getcwd()}/clipboard.json"

ALL_COMMANDS = {"help": ["help", "?"],
                "save": ["save", "s"],
                "load": ["load", "l"],
                "view": ["all", "a"],
                "delete": ["delete", "del", "d"],
                "wipe": ["wipe", "w", "clear"],
                "quit": ["quit", "q"],
                }


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


def terminal_dimensions():
    terminal_width = shutil.get_terminal_size()[0]
    return terminal_width


def tabulated_data(_data):
    formatted_data = {"KEY": [key for key in _data.keys()],
                      "VALUE": [value for value in _data.values()]}
    key_width = terminal_dimensions() * 0.10
    value_width = terminal_dimensions() * 0.70
    data_table = tabulate(formatted_data, headers=["KEYS", "VALUES"],
                          tablefmt="grid", maxcolwidths=[2, key_width, value_width],
                          showindex=[index for index, key in enumerate(data, 1)])
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


def save_validation(_key):
    key = _key
    while key in data.keys():
        print(f"Key '{key}' already exists; overwrite it?")
        confirmation = input("Y/N |> ")

        if confirmation.lower() == "y":
            print(f"Key: '{key}' will be overwritten...")
            return key
        else:
            key = input("Enter a new key to save against: ")
    else:
        return key


def save(_parameter):
    if len(_parameter) > 0:
        key = _parameter
    else:
        key = input("Enter a key to save the value against: ")

    while True:
        if key.isdigit():
            print("The key cannot be a number!")
            key = input("Please name the key to be saved against: ")
        elif len(key.strip()) < 1:
            print("Blank keys are unacceptable!")
            key = input("Please provide a key to save against: ")
        else:
            break

    if key == "\\":
        print("Saving cancelled!")
        return

    if key in data.keys():
        key = save_validation(key)

    print("Storing value...")
    data[key] = clipboard.paste()
    save_data(SAVED_DATA, data)
    print(f"Value stored at key: '{key}' successfully!")


def load(_parameter):
    if len(_parameter) > 0:
        key = _parameter
    else:
        key = input("Enter a key to be loaded: ")

    if key.isdigit():
        try:
            key_digit = key
            key = next(key for index, key in enumerate(data, 1) if index == int(key_digit))
        except StopIteration:
            pass

    if key == "\\":
        print("Loading cancelled!")
        return

    if key in data:
        clipboard.copy(data[key])
        print(f"'{key}' value copied to clipboard!")
    else:
        print("No such key exists!")


def view_all():
    if len(data.keys()) > 0:
        print(f"\n{tabulated_data(data)}\n")
    else:
        print("No values available to list!")


def delete(_parameter):
    if len(_parameter) > 0:
        key = _parameter
    else:
        key = input("Enter a key to be deleted: ")

    if key.isdigit():
        try:
            key_digit = key
            key = next(key for index, key in enumerate(data, 1) if index == int(key_digit))
        except StopIteration:
            pass

    if key == "\\":
        print("Deletion cancelled!")
        return

    if key in data:
        print(f"Deleting '{key}' from persistent clipboard...")
        data.pop(key)
        save_data(SAVED_DATA, data)
        print(f"'{key}' deleted successfully!")
    else:
        print("No such key exists!")


def wipe():
    print("Are you sure you like to clear all stored values?")
    confirmation = input("Y/N |> ")

    if confirmation.lower() == "y":
        print("Clearing stored items...")
        data.clear()
        save_data(SAVED_DATA, data)
        print("Stored items cleared successfully!")
    else:
        print("Retaining currently stored items...")


def quit_cleanup():
    print("Would you like to clear stored values before exiting?")
    confirmation = input("Y/N |> ")

    if confirmation.lower() == "y":
        print(f"Deleting {SAVED_DATA}...")
        os.remove(SAVED_DATA)
        print(f"Values stored in {SAVED_DATA} deleted successfully!")
    else:
        print("Retaining stored values...")

    print("\nQuitting application...")
    time.sleep(1)
    sys.exit()


def main(_user_input: list):
    blank_string = str()
    try:
        user_command: str = _user_input[0].lower()
    except IndexError:
        user_command = blank_string
    try:
        user_parameter: str = _user_input[1]
    except IndexError:
        user_parameter = blank_string

    if any(user_command in available_command for available_command in ALL_COMMANDS.values()):
        user_command: list = [key for key, value in ALL_COMMANDS.items() if user_command in value]
        user_command: str = user_command[0]
        if user_command == "save":
            save(user_parameter)
        elif user_command == "load":
            load(user_parameter)
        elif user_command == "view":
            view_all()
        elif user_command == "delete":
            delete(user_parameter)
        elif user_command == "wipe":
            wipe()
        elif user_command == "quit":
            quit_cleanup()
        elif user_command == "help":
            help_text()
    elif user_command == str():
        print("\nPlease provide a command, or type 'help' or '?' for a list of commands.")
    else:
        print("\nUnknown command!")


blurb()

print("Please enter a command: ")
while True:
    user_input = list(input("|> ").split())
    data = load_data(SAVED_DATA)
    if len(user_input) <= 2:
        main(user_input)
    elif len(user_input) > 2:
        print("Too many parameters entered!")
