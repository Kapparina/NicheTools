import json
from pathlib import Path
from typing import Any


class Jason:
    """Template for IO Control."""
    def __init__(self, path: str | Path, file: str):
        self.path = path
        self.file = file
        self.filepath = Path(self.path, self.file).resolve()

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

