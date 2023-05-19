import sys
import time
import shutil
import webbrowser
from pathlib import Path
from prettytable import PrettyTable, SINGLE_BORDER


def request_file_path():
    _user_filepath = input("Provide a directory: ")
    if len(_user_filepath) < 1:
        print("A directory must be provided!")
        _user_filepath = input("Please provide a directory: \n")
    else:
        return _user_filepath


def directory_check(_filepath):
    if _filepath.is_dir():
        file_counter(_filepath)
    else:
        print("This is not a valid file path!")


def file_counter(_filepath):
    file_count: int = 0
    file_list: list = []

    for file in _filepath.iterdir():
        if file.is_file():
            file_list.append(str(file.name))
            file_count += 1
    print(f"File count: {file_count}\n")
    _view_query = input("View a list of files? (Y/N): ")

    if _view_query.lower() == "y":
        view_files(file_list)
    else:
        print("Continuing...")


def view_files(_file_list):
    index_column_width = shutil.get_terminal_size()[1] * 0.05
    file_column_width = shutil.get_terminal_size()[0] * 0.75
    file_table = PrettyTable()
    file_table.add_column("INDEX", [index for index, file in enumerate(_file_list, 1)], align="r")
    file_table.add_column("FILE NAME", _file_list, align="l")
    file_table._max_width = {"INDEX": int(index_column_width), "FILE NAME": int(file_column_width)}
    file_table.set_style(SINGLE_BORDER)
    print(file_table)


def open_directory(_filepath):
    print(f"Specified directory: {_filepath}")
    _answer = input("Open specified directory? (Y/N): ")

    if _answer.lower() == "y":
        webbrowser.open(str(_filepath))
    else:
        print("OK!")


def run_script():
    filepath = Path(request_file_path()).resolve()
    directory_check(filepath)
    open_directory(filepath)


def main():
    while True:
        run_script()
        user_repeat = input("Check another directory? (Y/N): ")
        if user_repeat.lower() == "y":
            run_script()
        else:
            print("Alright, quitting...")
            time.sleep(1)
            sys.exit()


print("This script will check and count the files in given directory.")

if __name__ == "__main__":
    main()
