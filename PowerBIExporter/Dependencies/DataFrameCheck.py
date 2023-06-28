import pandas as pd
from pathlib import Path


# region Functions
def df_spreadsheet(spreadsheet: str | Path) -> pd.DataFrame:
    """Creates a pandas DataFrame from a given CSV file."""
    _spreadsheet: Path = Path(spreadsheet).resolve()

    if _spreadsheet.suffix == ".csv":
        df = pd.read_csv(spreadsheet)
    else:
        df = pd.read_excel(spreadsheet)

    return df


def count_rows(dataframe: pd.DataFrame) -> int:
    """Counts the rows in a given pandas DataFrame."""
    row_count: int = len(dataframe.index)

    return row_count


def df_row_count(file: str | Path) -> int:
    """A wrapper function, creating a pandas DataFrame from a CSV file and counting the rows in that DataFrame."""
    df: pd.DataFrame = df_spreadsheet(spreadsheet=file)
    row_count: int = count_rows(dataframe=df)

    return row_count
# endregion Functions
