import pandas as pd
from pathlib import Path


def dataframe_csv(csv_file: str | Path) -> pd.DataFrame:
    df = pd.read_csv(csv_file)

    return df


def count_rows(dataframe: pd.DataFrame) -> int:
    row_count: int = len(dataframe.index)

    return row_count


def csv_row_count(file: str | Path) -> int:
    df: pd.DataFrame = dataframe_csv(csv_file=file)
    row_count: int = count_rows(dataframe=df)

    return row_count
