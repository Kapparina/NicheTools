import json
from pathlib import Path
from typing import Any


class Jason:
    """Template for IO Control."""
    def __init__(self, path: str | Path, file: str):
        self._path = path
        self._file = file
        # self._filepath = Path(self.path, self.file).resolve()  # Optional attribute, see filepath property.

# ------------ Properties: ------------

    @property
    def path(self) -> Path:
        """The path property"""
        return self._path

    @path.setter
    def path(self, new_path: str | Path) -> None:
        self._path = new_path

    @path.deleter
    def path(self) -> None:
        del self._path

    @property
    def file(self) -> str:
        """The file property"""
        return self._file

    @file.setter
    def file(self, new_file: str) -> None:
        self._file = new_file

    @file.deleter
    def file(self) -> None:
        del self._file

    @property
    def filepath(self) -> Path:
        """The filepath property"""
        return Path(self.path, self.file).resolve()

# ------------ Methods: ------------

    def save_file(self, working_data: Any = None) -> bool:
        """Saves dictionary to a JSON file."""
        with open(self.filepath, "w") as f:
            try:
                json.dump(working_data, f)
            except json.JSONDecodeError:
                if self.filepath.is_file():
                    self.filepath.rmdir()
        return True

    def load_file(self) -> dict:
        """Loads a dictionary from a JSON file."""
        try:
            with open(self.filepath, "r") as f:
                loaded_data = json.load(f)
                return loaded_data
        except FileNotFoundError:
            return {}

