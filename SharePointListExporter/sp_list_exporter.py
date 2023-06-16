# Standard library packages:
import os
import shutil
import time
from pathlib import Path

# Project-specific/local library packages:
import SharePointListExporter.startup as startup
import SharePointListExporter.Dependencies.FileOperations as Fops
import SharePointListExporter.Dependencies.Selenium as Selene
import SharePointListExporter.Dependencies.DataFrameCheck as DFCheck


# Constants:
DL_DIR: str = "C:/temp/SeleneDownloads"
ARCHIVE_DIR: str = f"{DL_DIR}/Archive"
DRIVER_DIR: str = "C:/temp/SeleneEdge"
USER_DOWNLOADS: Path = Path(f"{os.getenv('USERPROFILE')}", "Downloads")

# Variables:
sp_list_url: str = "https://linkhub.sharepoint.com/sites/RPARC/PROD/s290/Lists/s290/AllItems.aspx?env=WebViewList"


def move_from_downloads(file: Path) -> Path:
    """Moves a file from a directory to this application's working directory."""
    shutil.move(src=file,
                dst=Path(DL_DIR))
    moved_file: Path = Path(DL_DIR, file.name)

    return moved_file


def latest_csv() -> None | str | bool:
    return Fops.get_latest_csv(directory=str(USER_DOWNLOADS))


# -------------- Startup Function --------------
def initialize() -> None:
    """Prepares directories for later functions."""
    Fops.create_directory(DL_DIR, ARCHIVE_DIR, DRIVER_DIR)
    startup.archive_old(working_directory=DL_DIR,
                        archive_directory=ARCHIVE_DIR)  # Archive old files in this tool's working directory.

    while latest_csv() is not None:
        time.sleep(5)


# -------------- Browser Operations --------------
def browser_actions() -> None:
    """Prepares and performs actions using a Selenium-based Edge WebDriver."""
    browser_service: Selene.EdgeService = Selene.create_service(root_directory=DRIVER_DIR)
    browser_options: Selene.EdgeOptions = Selene.create_options(f"user-data-dir={os.getenv('TEMP')}")
    browser: Selene.EdgeDriver = Selene.create_driver(options=browser_options,
                                                      service=browser_service)
    # TODO: List of downloaded files.
    # TODO: While loop using list of downloaded files, crosschecking old files.
    browser.get(sp_list_url)
    Selene.wait_element_clickable(driver=browser,
                                  element_name="Export")
    Selene.find_element_name(driver=browser,
                             element="Export").click()
    Selene.wait_element_clickable(driver=browser,
                                  element_name="Export to CSV")
    Selene.find_element_name(driver=browser,
                             element="Export to CSV").click()
    # TODO: Delete downloaded files until only the most recent is the sole file created in last minute?
    while latest_csv() is None:
        time.sleep(1)
        counter: int = 0
        counter += 1

        if counter == 20:
            break
        else:
            continue


# -------------- Main Function --------------
def main():
    initialize()
    browser_actions()

    if type(file := latest_csv()) is not str:
        time.sleep(10)
        browser_actions()
        # TODO: See TODO in browser_actions().
    else:
        timestamped_file: Path = Fops.rename_timestamp(file=file)
        working_file: Path = move_from_downloads(file=timestamped_file)
        row_count: int = DFCheck.csv_row_count(file=working_file)
        print(f"Current item count: {row_count}")


if __name__ == '__main__':
    main()
