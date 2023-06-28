import time
import shutil
from pathlib import Path
from datetime import datetime
import winreg
from typing import Any


class FileOperator:
    _archive: Path
    _downloads: Path
    _recent_seconds: float
    _working_directory: Path

    def __init__(self, recent_seconds=60,
                 archive=None, working_directory=None,
                 downloads=None) -> None:

        self._archive = archive
        self._downloads = downloads
        self._recent_seconds = recent_seconds
        self._working_directory = working_directory

    # region Properties
    @property
    def archive(self) -> Path:
        return self._archive

    @archive.setter
    def archive(self, directory: str | Path) -> None:
        self._archive = Path(directory)

    @property
    def downloads(self) -> Path:
        return self._downloads

    @property
    def recent_seconds(self) -> float:
        return self._recent_seconds

    @recent_seconds.setter
    def recent_seconds(self, num_seconds: float) -> None:
        self._recent_seconds = num_seconds

    @property
    def working_directory(self) -> Path:
        return self._working_directory

    @working_directory.setter
    def working_directory(self, directory) -> None:
        self._working_directory = Path(directory)
    # endregion Properties

    # region Static Methods
    @staticmethod
    def _add_timestamp(file: str | Path) -> Path:
        """Renames a file, appending the current date and time."""
        _file: Path = Path(file)
        timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")

        renamed_file: Path = _file.rename(
            _file.with_stem(f"{_file.stem}_{timestamp}"))

        return renamed_file

    @staticmethod
    def _create_directory(to_create: str | Path) -> Path | None:
        """Creates a directory, including parent directories along the path."""
        directory: Path = Path(to_create)

        if not directory.is_dir():
            directory.mkdir(parents=True)
            return directory
        else:
            return None

    @staticmethod
    def check_extension(file: str | Path, extension: str) -> bool:
        _file: Path = Path(file)

        if _file.suffix == extension:
            return True
        else:
            return False

    @staticmethod
    def get_downloads_directory() -> Path:
        """Checks the Windows Registry for the current user's Downloads directory."""
        with winreg.OpenKey(
                key=winreg.HKEY_CURRENT_USER,
                sub_key=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders") as key:

            downloads: Path = Path(
                winreg.QueryValueEx(key, "{374DE290-123F-4565-9164-39C4925E467B}")[0])

            return downloads

    @staticmethod
    def remove_directory(to_remove: str | Path) -> Path | None:
        directory: Path = Path(to_remove)

        if directory.is_dir():
            directory.rmdir()
            return directory
        else:
            return None

    @staticmethod
    def rename_with_timestamp(file: str | Path, new_name: str) -> Path:
        """Renames a given file using a specified name, appending the current date and time."""
        _file: Path = Path(file)
        timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")

        renamed_file: Path = _file.rename(
            _file.with_stem(f"{new_name}_{timestamp}"))

        return renamed_file
    # endregion Static Methods

    # region Instance Methods
    def archive_working_directory(self) -> int:
        """Moves files from the FileOperator's working directory to the archive directory."""
        archived_count: int = 0

        for item in self.downloads.iterdir():
            if item.is_file():
                shutil.move(
                    src=item,
                    dst=self.archive)
                archived_count += 1
            else:
                pass

        return archived_count

    def count_recently_created(self, directory: str | Path) -> int:
        """Counts recently created files; the definition of 'recently created' can be adjusted using the property."""
        _directory: Path = Path(directory)
        files: list = []

        for item in _directory.iterdir():
            if item.is_file() and self.recently_created(file=item):
                files.append(item)

        recent_file_count: int = len(files)

        return recent_file_count

    def create_directories(self, *dirs_to_create) -> list[Path]:
        """Creates a number of directories."""
        created_directories: list[Path] = []

        for directory in dirs_to_create:
            new_dir: Path | None = self._create_directory(to_create=directory)
            created_directories.append(new_dir)

        return created_directories

    def remove_working_directory(self) -> Path | None:
        if self.working_directory.is_dir():
            self.working_directory.rmdir()
            return self.working_directory
        else:
            return None

    def working_to_downloads(self) -> int:
        """Moves files from the FileOperator's working directory to the archive directory."""
        moved_count: int = 0

        for item in self.working_directory.iterdir():
            if item.is_file():
                shutil.move(
                    src=item,
                    dst=self.downloads)
                moved_count += 1
            else:
                pass

        return moved_count

    def recently_created(self, file: str | Path) -> bool:
        """Checks whether a file created fits within the definition of 'recently created'."""
        delta = time.time() - Path(file).stat().st_ctime

        if delta < self.recent_seconds:
            return True
        else:
            return False
    # endregion


# region Functions
def get_downloads_folder():
    """Checks the Windows Registry for the current user's Downloads directory."""
    with winreg.OpenKey(
            key=winreg.HKEY_CURRENT_USER,
            sub_key=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders") as key:

        downloads: Any = winreg.QueryValueEx(key, "{374DE290-123F-4565-9164-39C4925E467B}")[0]

        return downloads
# endregion functions
