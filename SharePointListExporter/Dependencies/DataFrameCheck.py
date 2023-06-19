import pandas as pd
from pathlib import Path


def dataframe_csv(csv_file: str | Path) -> pd.DataFrame:
    """Creates a pandas DataFrame from a given CSV file."""
    df = pd.read_csv(csv_file)

    return df


def count_rows(dataframe: pd.DataFrame) -> int:
    """Counts the rows in a given pandas DataFrame."""
    row_count: int = len(dataframe.index)

    return row_count


def csv_row_count(file: str | Path) -> int:
    """A wrapper function, creating a pandas DataFrame from a CSV file and counting the rows in that DataFrame."""
    df: pd.DataFrame = dataframe_csv(csv_file=file)
    row_count: int = count_rows(dataframe=df)

    return row_count
