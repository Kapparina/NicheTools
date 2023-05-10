import pandas as pd
from pathlib import Path


def user_filepath():
    _user_path = input("Specify a file path: \n")
    if Path(_user_path).is_dir():
        return _user_path
    else:
        print("Invalid file path!")
        user_filepath()


def user_spreadsheet(_filepath: str):
    _user_sheet = input("Specify a spreadsheet to compare: \n")
    if Path(_filepath, _user_sheet).is_file():
        spreadsheet = str(Path(_filepath, _user_sheet))
        print(spreadsheet)
        return spreadsheet
    else:
        print("No such file exists!")
        user_spreadsheet(_filepath)


def user_dataframe(_spreadsheet: str):
    if Path(_spreadsheet).suffix.startswith(".xl"):
        _dataframe = pd.read_excel(str(_spreadsheet), header=1, index_col=False, skiprows=False)
    else:
        _dataframe = pd.read_csv(str(_spreadsheet), header=1, skip_blank_lines=True)
    return _dataframe


dataframe_1 = user_dataframe(spreadsheet_1 := user_spreadsheet(filepath_1 := user_filepath()))
dataframe_2 = user_dataframe(spreadsheet_2 := user_spreadsheet(filepath_2 := user_filepath()))

print(f"{filepath_1}"
      f"{spreadsheet_1}"
      f"{filepath_2}"
      f"{spreadsheet_2}")

resulting_dataframe = pd.merge(dataframe_1, dataframe_2, indicator=True)
print(resulting_dataframe)
