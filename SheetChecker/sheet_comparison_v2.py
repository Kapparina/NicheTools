import pandas as pd
from pathlib import Path
import sys
import time
import shutil
import webbrowser

import pandas.errors
from prettytable import PrettyTable, SINGLE_BORDER

BLANK: str = str()


def directory_handler(_directory_count: int = 3) -> Path:
    if _directory_count == 0:
        print("\nWhere does the first spreadsheet live?")
    elif _directory_count == 1:
        print("\nWhere does the second spreadsheet live?\n"
              "(If it's in the same place as the first, say nothing.)\n")
    elif _directory_count == 2:
        print("\nWhere does a spreadsheet live?\n")
    else:
        _directory_count = 0
        print("\nWhere would you like to store the file?")

    _directory: str | Path | bool = request_file_path(_directory_count)
    while True:
        if _directory is False:
            _directory = request_file_path(_directory_count)
        else:
            return _directory


def request_file_path(_directory_count: int) -> str | Path:
    while True:
        _user_filepath = input("Provide a directory:\n")

        if len(_user_filepath) < 1 and _directory_count == 0:
            print("A directory must be provided!")
        elif len(_user_filepath) < 1 and _directory_count == 1:
            return BLANK
        else:
            return directory_check(Path(_user_filepath).resolve())


def directory_check(_filepath) -> Path | bool:
    if _filepath.is_dir():
        return _filepath
    else:
        print("This is not a valid file path!")
        return False


def spreadsheet_counter(_filepath) -> dict:
    spreadsheet_count: int = 0
    spreadsheet_list: list = []
    suffix_list: list = [".csv", ".xlsx", ".xl", ".xlsm"]

    for file in _filepath.iterdir():
        if file.is_file() and file.suffix in suffix_list:
            spreadsheet_list.append(str(file.name))
            spreadsheet_count += 1

    spreadsheet_dict = dict(enumerate(spreadsheet_list, 1))
    print(f"Spreadsheet count: {spreadsheet_count}\n")
    return spreadsheet_dict


def view_spreadsheets(_files: dict) -> dict:
    index_column_width = shutil.get_terminal_size()[1] * 0.05
    filename_column_width = shutil.get_terminal_size()[0] * 0.75
    file_table = PrettyTable()
    file_table.add_column("INDEX", [key for key in _files.keys()], align="r")
    file_table.add_column("FILE NAME", [file for file in _files.values()], align="l")
    file_table._max_width = {"INDEX": int(index_column_width), "FILE NAME": int(filename_column_width)}
    file_table.set_style(SINGLE_BORDER)
    print(file_table)
    return _files


def select_spreadsheet(_spreadsheets: dict) -> tuple[dict, str]:
    while True:
        _user_selection = input("Provide a spreadsheet index or name:\n")

        if _user_selection.isdigit():
            key = int(_user_selection)
        else:
            key = next((key for key, value in _spreadsheets.items() if value == _user_selection), None)

        if key in _spreadsheets.keys():
            print(f"'{_spreadsheets[key]}' selected!\n")
            _selected_sheet: str = _spreadsheets[key]
            _spreadsheets.pop(key)
            break
        else:
            print("Try again!")

    return _spreadsheets, _selected_sheet


def create_dataframe(_path: Path) -> pd.DataFrame:
    if _path.suffix != ".csv":
        _dataframe = pd.read_excel(str(_path), index_col=False)
    else:
        _dataframe = pd.read_csv(str(_path), index_col=False, skip_blank_lines=False)
    return _dataframe


# TODO: Comparison parameters function (column selection, etc.).


def compare_spreadsheets(_directories: list[Path], _sheets: list[str]):
    query_matches = r"_merge == 'MATCH'"
    query_differences = r"_merge != 'MATCH'"

    dataframe_1 = create_dataframe(Path(_directories[0], _sheets[0])).astype(str)
    dataframe_2 = create_dataframe(Path(_directories[1], _sheets[1])).astype(str)
    try:
        resulting_dataframe = pd.merge(dataframe_1, dataframe_2,
                                       indicator=True,
                                       how="outer",)
        dataframe_names = {"left_only": _sheets[0], "right_only": _sheets[1], "both": "MATCH"}
        resulting_dataframe["_merge"] = resulting_dataframe["_merge"].map(dataframe_names)
        if resulting_dataframe.query(query_differences).empty:
            print("These spreadsheets are identical!")
        else:
            print(resulting_dataframe.query(query_differences).to_string())

        output_choice = input("Would you like to export the results? (Y/N): ")
        if output_choice.lower() == "y":
            spreadsheet_output(resulting_dataframe)
    except pandas.errors.MergeError:
        print("These spreadsheets' columns are dissimilar!\n"
              "Presently, this tool can only be used to compare spreadsheets sharing the same layout.\n"
              "\n(Both spreadsheets must share column names.)\n")


def spreadsheet_output(_dataframe: pd.DataFrame, *_queries):
    output_path = directory_handler()
    output_format = input("Would you like the data in '.xlsx' format? (Y/N): ")
    if output_format.lower() == "y":
        _dataframe.to_excel(f"{output_path}/comparison_output.xlsx", index=False)
    else:
        _dataframe.to_csv(f"{output_path}/comparison_output.csv", index=False)

    print("\nData exported successfully!")


def open_directory(_filepath) -> None:
    print(f"Specified directory: {_filepath}")
    _answer = input("Open specified directory? (Y/N): ")

    if _answer.lower() == "y":
        webbrowser.open(str(_filepath))
    else:
        print("OK!")


def run_script() -> None:
    directory_count: int = 0
    directory_list: list = []
    comparison_sheets: list = []

    while directory_count < 2:
        directory = directory_handler(directory_count)
        if directory == BLANK:
            directory = directory_list[0]

        if len(available_spreadsheets := spreadsheet_counter(directory)) >= 1:
            directory_list.append(directory)
            directory_count += 1
            view_spreadsheets(available_spreadsheets)
            comparison_sheets.append(select_spreadsheet(available_spreadsheets)[1])
        else:
            print(f"'{directory}' contains zero spreadsheets!")

    compare_spreadsheets(directory_list, comparison_sheets)


def main():
    while True:
        run_script()
        user_repeat = input("Compare more spreadsheets? (Y/N): ")
        if user_repeat.lower() == "y":
            run_script()
        else:
            print("Alright, quitting...")
            time.sleep(1)
            sys.exit()


print("This script allows comparison of two spreadsheets.")

if __name__ == "__main__":
    main()
