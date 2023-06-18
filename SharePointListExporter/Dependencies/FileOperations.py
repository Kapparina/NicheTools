import time
import glob
import shutil
from pathlib import Path
from collections import namedtuple
from datetime import datetime
import winreg
from typing import Any


class FileOperator:
    _archive: Path
    _downloads: Path
    _recent_seconds: float
    _working_directory: Path

    def __init__(self, recent_seconds=60,
                 archive=None, working_directory=None) -> None:
        self._archive = archive
        self._downloads = self.get_downloads_directory()
        self._recent_seconds = recent_seconds
        self._working_directory = working_directory

    @property
    def archive(self) -> Path:
        return self._archive

    @archive.setter
    def archive(self, directory: str | Path) -> None:
        self._archive = Path(directory)

    @property
    def recent_seconds(self) -> float:
        return self._recent_seconds

    @recent_seconds.setter
    def recent_seconds(self, num_seconds: float) -> None:
        self._recent_seconds = num_seconds

    @property
    def downloads(self) -> Path:
        return self._downloads

    @property
    def working_directory(self) -> Path:
        return self._working_directory

    @working_directory.setter
    def working_directory(self, directory) -> None:
        self._working_directory = Path(directory)

    @staticmethod
    def _create_directory(to_create: str | Path) -> Path | None:
        directory: Path = Path(to_create)

        if not directory.is_dir():
            directory.mkdir(parents=True)
            return directory
        else:
            return None

    @staticmethod
    def get_downloads_directory() -> Path:
        with winreg.OpenKey(
                key=winreg.HKEY_CURRENT_USER,
                sub_key=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders") as key:
            downloads: Path = Path(
                winreg.QueryValueEx(key, "{374DE290-123F-4565-9164-39C4925E467B}")[0])

            return downloads

    @staticmethod
    def add_timestamp(file: str | Path) -> Path:
        _file: Path = Path(file)
        timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")
        renamed_file: Path = _file.rename(_file.with_stem(f"{_file.stem}_{timestamp}"))

        return renamed_file

    def archive_working_directory(self) -> int:
        archived_count: int = 0

        for item in self.working_directory.iterdir():
            if item.is_file():
                shutil.move(
                    src=item,
                    dst=self.archive)
                archived_count += 1
            else:
                pass

        return archived_count

    def count_recently_created(self, directory: str | Path) -> int:
        _directory: Path = Path(directory)
        files: list = []

        for item in _directory.iterdir():
            if item.is_file() and self.recently_created(file=item):
                files.append(item)

        recent_file_count: int = len(files)

        return recent_file_count

    def recently_created(self, file: str | Path) -> bool:
        delta = time.time() - Path(file).stat().st_ctime

        if delta < self.recent_seconds:
            return True
        else:
            return False

    def create_directories(self, *dirs_to_create) -> list[Path]:
        created_directories: list[Path] = []

        for directory in dirs_to_create:
            new_dir: Path | None = self._create_directory(to_create=directory)
            created_directories.append(new_dir)

        return created_directories


def get_downloads_folder():
    with winreg.OpenKey(
            key=winreg.HKEY_CURRENT_USER,
            sub_key=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders") as key:

        downloads: Any = winreg.QueryValueEx(key, "{374DE290-123F-4565-9164-39C4925E467B}")[0]

        return downloads


# def modified_recently(file: str):
#     """Checks if a file or files have been modified within the last 60 seconds."""
#     delta = time.time() - Path(file).stat().st_mtime
#     if delta < 60:
#         return True
#     else:
#         return False


# def count_recent_csv(directory: str) -> namedtuple:
#     """Counts recently modified CSV files in a given directory."""
#     csv_files: list = [file for file
#                        in glob.glob(pathname=f"{directory}/*.csv")
#                        if modified_recently(file)]
#
#     ResultCount: namedtuple = namedtuple(
#         typename="FileCount",
#         field_names=["total", "files"])
#
#     return ResultCount(
#         total=len(csv_files),
#         files=csv_files)
#
#
# def get_latest_csv(directory: str) -> None | str | bool:
#     """Used to retrieve the most recently modified CSV file in a directory."""
#     latest_count, latest_files = count_recent_csv(directory=directory)
#
#     if latest_count == 0:
#         return None
#     elif latest_count == 1:
#         return latest_files[0]
#     elif latest_count >= 2:
#         return False
