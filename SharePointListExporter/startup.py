import shutil
from pathlib import Path
import json

import SharePointListExporter.Dependencies.FileOperations as Fops


def archive_old(working_directory: str,
                archive_directory: str) -> int:
    """Moves files currently in this application's working directory to an archive directory."""
    item_count: int = 0

    for item in Path(working_directory).iterdir():
        if item.is_file():
            shutil.move(
                src=item,
                dst=Path(archive_directory))
            item_count += 1

    return item_count


def load_json(file: str | Path) -> dict:
    with open(file=file,
              mode="r") as f:
        data: dict = json.load(f)

    return data
