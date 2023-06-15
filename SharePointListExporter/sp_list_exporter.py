# Standard library packages:
import os
import shutil
import time
from pathlib import Path

# External library packages:
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# Project-specific/local library packages:
import SharePointListExporter.Dependencies.FileOperations as Fops
import SharePointListExporter.Dependencies.Selenium as Selene


# Constants:
DL_DIR: str = "C:/temp/SeleneDownloads"
ARCHIVE_DIR: str = f"{DL_DIR}/Archive"
DRIVER_DIR: str = "C:/temp/SeleneEdge"
URL: str = "https://linkhub.sharepoint.com/sites/RPARC/PROD/s290/Lists/s290/AllItems.aspx?env=WebViewList"
USER_DOWNLOADS: Path = Path(f"{os.getenv('USERPROFILE')}", "Downloads")


# -------------- File Operations --------------
def archive_old() -> int:
    """Moves files currently in this application's working directory to an archive directory."""
    item_count: int = 0

    for item in Path(DL_DIR).iterdir():
        if item.is_file():
            shutil.move(src=item,
                        dst=Path(ARCHIVE_DIR))
            item_count += 1

    return item_count


def move_from_downloads(file: str) -> bool:
    """Moves a file from a directory to this application's working directory."""
    shutil.move(src=file,
                dst=Path(DL_DIR))
    return True


def latest_csv() -> None | str | bool:
    return Fops.get_latest_csv(directory=str(USER_DOWNLOADS))


# -------------- Startup Function --------------
def startup() -> None:
    """Prepares directories for later functions."""
    for d in [DL_DIR, ARCHIVE_DIR, DRIVER_DIR]:
        Fops.create_directory(path=d)

    archive_old()  # Archive old files in this tool's working directory.

    if latest_csv() is not None:
        time.sleep(60)
    else:
        pass


# -------------- Browser Operations --------------
def browser_actions() -> None:
    """Prepares and performs actions using a Selenium-based Edge WebDriver."""
    browser_service: Selene.EdgeService = Selene.create_service(root_directory=DRIVER_DIR)
    browser_options: Selene.EdgeOptions = Selene.create_options(f"user-data-dir={os.getenv('TEMP')}")
    browser: Selene.wd.Edge = Selene.create_driver(options=browser_options,
                                                   service=browser_service)

    browser.get(URL)
    WebDriverWait(driver=browser,
                  timeout=10
                  ).until(ec.element_to_be_clickable(mark=(By.NAME,
                                                           "Export")))
    browser.find_element(by=By.NAME,
                         value="Export").click()
    WebDriverWait(driver=browser,
                  timeout=10
                  ).until(ec.element_to_be_clickable(mark=(By.NAME,
                                                           "Export to CSV")))
    browser.find_element(by=By.NAME,
                         value="Export to CSV").click()

    time.sleep(5)


# -------------- Main Function --------------
def main():
    startup()
    browser_actions()

    if type(file := latest_csv()) is not str:
        time.sleep(10)
    else:
        timestamped_file = Fops.rename_timestamp(file)
        move_from_downloads(file=str(timestamped_file))


if __name__ == '__main__':
    main()
