import os
import json
from pathlib import Path

from SharePointListExporter.Dependencies import FileOperator
from SharePointListExporter.Dependencies import SeleniumEdge as Selene


def archive_all(file_manager: FileOperator) -> int:
    """Moves files from a FileOperator's working directory to an archive directory."""
    archive_count: int = file_manager.archive_working_directory()

    return archive_count


def create_directories(file_manager: FileOperator,
                       directories: dict) -> None:

    """Creates directories using a FileOperator."""
    for key, value in directories.items():
        file_manager.create_directories(value)


def load_json(file: str | Path) -> dict:
    """Loads a JSON file and returns it."""
    with open(file=file,
              mode="r") as f:
        data: dict = json.load(f)

    return data


def browser_startup(driver_root: str | Path,
                    download_path: str | Path) -> Selene.Browser:

    """Configures and instantiates a Browser"""
    _driver_root: str = str(driver_root)
    _download_path: str = str(download_path)

    browser: Selene.Browser = Selene.Browser()
    browser.add_service(directory=_driver_root)

    browser.add_options(
        f"user-data-dir={os.getenv('TEMP')}",
        "headless=new",
        "disable-gpu",
        "window-size=1920,1080")

    browser.Options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": _download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True
        })

    browser.add_driver()

    return browser
