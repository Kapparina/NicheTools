import time
import glob
from pathlib import Path
from collections import namedtuple
from datetime import datetime


def modified_recently(file: str):
    """Checks if a file or files have been modified within the last 60 seconds."""
    delta = time.time() - Path(file).stat().st_mtime
    if delta < 60:
        return True
    else:
        return False


def rename_timestamp(file: str) -> Path:
    """Takes a file and renames it, appending a timestamp."""
    name_timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")
    _file = Path(file)
    renamed_file = _file.rename(_file.with_stem(f"{_file.stem}_{name_timestamp}"))

    return renamed_file


def create_directory(*paths: str) -> Path:
    """Creates a chosen directory."""
    for path in paths:
        directory: Path = Path(path)

        if not directory.is_dir():
            directory.mkdir(parents=True)

        return directory


def count_recent_csv(directory: str) -> namedtuple:
    """Counts recently modified CSV files in a given directory."""
    csv_files: list = [file for file
                       in glob.glob(pathname=f"{directory}/*.csv")
                       if modified_recently(file)]

    ResultCount: namedtuple = namedtuple(typename="FileCount",
                                         field_names=["total", "files"])

    return ResultCount(total=len(csv_files), files=csv_files)


def get_latest_csv(directory: str) -> None | str | bool:
    """Used to retrieve the most recently modified CSV file in a directory."""
    latest_count, latest_files = count_recent_csv(directory=directory)

    if latest_count == 0:
        return None
    elif latest_count == 1:
        return latest_files[0]
    elif latest_count >= 2:
        return False
