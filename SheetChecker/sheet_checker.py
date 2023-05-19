import pandas as pd
from pathlib import Path
from pandas.testing import assert_frame_equal


def user_filepath():
    _user_path = input("Specify a file path: \n")
    while True:
        if Path(_user_path).is_dir() is False:
            print("Invalid file path!")
            _user_path = input("Specify a valid file path: \n")
        else:
            return _user_path


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
        _dataframe = pd.read_excel(str(_spreadsheet), index_col=False, skiprows=False)
    else:
        _dataframe = pd.read_csv(str(_spreadsheet), skip_blank_lines=False)
    return _dataframe


dataframe_1 = user_dataframe(spreadsheet_1 := user_spreadsheet(filepath_1 := user_filepath())).astype(str)
dataframe_2 = user_dataframe(spreadsheet_2 := user_spreadsheet(filepath_2 := user_filepath())).astype(str)

print(f"{Path(spreadsheet_1).name}")

resulting_dataframe = pd.merge(dataframe_1, dataframe_2,
                               indicator=True,
                               how="outer")
query_1 = r"_merge == 'both'"
query_2 = r"_merge != 'both'"
print(resulting_dataframe.query(query_1).to_string())
print(resulting_dataframe.query(query_2).to_string())
print(f"Left row count: {len(dataframe_1.index)}\n"
      f"Right row count: {len(dataframe_2.index)}\n"
      f"Merged row count: {len(resulting_dataframe.index)}\n"
      f"Total items post-merge in both: {len(resulting_dataframe.query(query_1))}\n"
      f"Total items post-merge not in both: {len(resulting_dataframe.query(query_2))}")
# resulting_dataframe.to_csv("C:/temp/returned_mail_merge.csv")
# assert_frame_equal(dataframe_1, dataframe_2, check_dtype=False)



