# -------------- Standard library packages --------------
import os
import shutil
import time
from pathlib import Path
from datetime import datetime
import json

# -------------- Project-specific/local library packages --------------
import SharePointListExporter.startup as startup
import SharePointListExporter.Dependencies.FileOperations as Fops
import SharePointListExporter.Dependencies.SeleniumEdge as Selene
import SharePointListExporter.Dependencies.DataFrameCheck as DFCheck

# -------------- Constants --------------
ALL_DIRS: dict = startup.load_json(file=Path("./Data/working_directories.json").resolve())  # All directories.
ARCHIVE_DIR: Path = Path(ALL_DIRS["archive_directory"])  # Archive directory.
DRIVER_DIR: Path = Path(ALL_DIRS["driver_directory"])  # Driver directory.
NAME_TIMESTAMP: str = datetime.now().strftime("%Y%m%d_%H%M%S")  # Filename-formatted timestamp.
USER_DOWNLOADS: Path = Path(Fops.get_downloads_folder())  # Current user's 'Downloads' directory.
WORKING_DIR: Path = Path(ALL_DIRS["working_directory"])  # Working directory.

# -------------- Variables --------------
sp_lists: dict = startup.load_json(file=Path("./Data/test_lists.json").resolve())  # JSON file with SP list URLs.


# -------------- Startup Function --------------
def initialize() -> tuple[Fops.FileOperator, Selene.Browser]:
    """Prepares directories for later functions."""
    file_helper: Fops.FileOperator = Fops.FileOperator(
        archive=ARCHIVE_DIR,
        working_directory=WORKING_DIR)

    startup.create_directories(
        file_manager=file_helper,
        directories=ALL_DIRS)

    startup.archive_all(file_manager=file_helper)

    browser: Selene.Browser = startup.browser_startup(
        driver_root=DRIVER_DIR,
        download_path=WORKING_DIR)

    return file_helper, browser


# -------------- Browser Operations --------------
def browser_actions(browser: Selene.Browser,
                    url: str,
                    file_manager: Fops.FileOperator) -> bool:
    """Prepares and performs actions using a Selenium-based Edge WebDriver."""
    # TODO: List of downloaded files.
    # TODO: While loop using list of downloaded files, crosschecking old files.

    _browser: Selene.Browser = browser
    _browser.get_url(url=url)
    file_helper: Fops.FileOperator = file_manager

    time.sleep(3)

    _browser.take_screenshot(Path(
        DRIVER_DIR,
        f"screenshot_{NAME_TIMESTAMP}.png"))

    _browser.switch_last_frame()

    _browser.click_element_xpaths(
        "//span[contains(text(), 'Export')]",
        "//span[contains(text(), 'Export to CSV')]")

    # TODO: Delete downloaded files until only the most recent is the sole file created in last minute?
    sleep_counter: int = 0

    while file_helper.count_recently_created(directory=WORKING_DIR) < 1:
        time.sleep(1)
        sleep_counter += 1

        if sleep_counter == 20:
            break
        else:
            continue


# -------------- Main Function --------------
def main() -> None:
    file_helper, browser = initialize()
    list_summaries: dict = {}

    while True:
        try:
            for list_name, list_url in sp_lists.items():
                browser_actions(
                    browser=browser,
                    url=list_url,
                    file_manager=file_helper)

            break

        except Selene.TimeoutException:
            print("Whoops, I've failed! Trying again...")
            browser.restart()
            time.sleep(3)

    for file in WORKING_DIR.iterdir():
        if file.is_file():
            timestamped_file: Path = file_helper.add_timestamp(file=file)
            row_count: int = DFCheck.csv_row_count(file=timestamped_file)
            print(f"'{list_name}' item count: {row_count}")
            list_summaries[list_name] = row_count
            file_helper.archive_working_directory()

    with open(
            file=f"{WORKING_DIR}/Summary_{NAME_TIMESTAMP}.json",
            mode="w") as summary_json:

        json.dump(obj=list_summaries,
                  fp=summary_json)


if __name__ == '__main__':
    main()
