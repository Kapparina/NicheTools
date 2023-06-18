# Standard library packages:
import os
import shutil
import time
from pathlib import Path
import psutil

# Project-specific/local library packages:
import SharePointListExporter.startup as startup
import SharePointListExporter.Dependencies.FileOperations as Fops
import SharePointListExporter.Dependencies.SeleniumEdge as Selene
import SharePointListExporter.Dependencies.DataFrameCheck as DFCheck

# Constants:
DL_DIR: str = "C:/temp/SeleneDownloads"
ARCHIVE_DIR: str = f"{DL_DIR}/Archive"
DRIVER_DIR: str = "C:/temp/SeleneEdge"
USER_DOWNLOADS: Path = Path(f"{os.getenv('USERPROFILE')}", "Downloads")

# Variables:
sp_lists: dict = startup.load_json(Path("./Data/lists.json").resolve())


def move_from_downloads(file: Path) -> Path:
    """Moves a file from a directory to this application's working directory."""
    shutil.move(
        src=file,
        dst=Path(DL_DIR))
    moved_file: Path = Path(DL_DIR, file.name)

    return moved_file


def latest_csv() -> None | str | bool:
    return Fops.get_latest_csv(directory=str(USER_DOWNLOADS))


# -------------- Startup Function --------------
def initialize() -> None:
    """Prepares directories for later functions."""
    Fops.create_directory(DL_DIR, ARCHIVE_DIR, DRIVER_DIR)

    startup.archive_old(
        working_directory=DL_DIR,
        archive_directory=ARCHIVE_DIR)  # Archive old files in this tool's working directory.

    while latest_csv() is not None:
        time.sleep(5)


# -------------- Browser Operations --------------
def browser_actions(url: str) -> None:
    """Prepares and performs actions using a Selenium-based Edge WebDriver."""
    browser_service: Selene.EdgeService = Selene.create_service(root_directory=DRIVER_DIR)

    browser_options: Selene.EdgeOptions = Selene.create_options(
        f"user-data-dir={os.getenv('TEMP')}",
        "headless=new",
        "disable-gpu",
        "window-size=1920,1080")

    browser: Selene.EdgeDriver = Selene.create_driver(
        options=browser_options,
        service=browser_service)

    # TODO: List of downloaded files.
    # TODO: While loop using list of downloaded files, crosschecking old files.

    browser.get(url=url)
    browser.get_screenshot_as_file(Path(DRIVER_DIR, "screenshot.png"))

    Selene.wait_element_clickable(
        driver=browser,
        element_name="Export")

    Selene.find_element_name(
        driver=browser,
        element="Export").click()

    Selene.wait_element_clickable(
        driver=browser,
        element_name="Export to CSV")

    Selene.find_element_name(
        driver=browser,
        element="Export to CSV").click()

    # TODO: Delete downloaded files until only the most recent is the sole file created in last minute?

    sleep_counter: int = 0

    while latest_csv() is None:
        time.sleep(1)
        sleep_counter += 1

        if sleep_counter == 20:
            break
        else:
            continue


# -------------- Main Function --------------
def main() -> None:
    for key, value in sp_lists.items():
        initialize()
        browser_actions(url=value)

        if type(file := latest_csv()) is not str:
            time.sleep(10)

            # TODO: See TODO in browser_actions().

        else:
            timestamped_file: Path = Fops.rename_timestamp(file=file)
            working_file: Path = move_from_downloads(file=timestamped_file)
            row_count: int = DFCheck.csv_row_count(file=working_file)
            print(f"{key.upper()} item count: {row_count}")


if __name__ == '__main__':
    main()
