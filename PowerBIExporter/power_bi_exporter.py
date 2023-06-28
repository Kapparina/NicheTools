import time
import warnings
from pathlib import Path
from datetime import datetime
import json

import PowerBIExporter.startup as startup
import PowerBIExporter.Dependencies.FileOperations as Fops
import PowerBIExporter.Dependencies.SeleniumEdge as Selene
import PowerBIExporter.Dependencies.DataFrameCheck as DFCheck


# region Constants
ALL_DIRS: dict = startup.load_json(file=Path("Data/working_directories.json").resolve())
ARCHIVE_DIR: Path = Path(ALL_DIRS["archive_directory"])
DRIVER_DIR: Path = Path(ALL_DIRS["driver_directory"])
FINAL_DIR: Path = Path(ALL_DIRS["final_directory"])
NAME_TIMESTAMP: str = datetime.now().strftime("%Y%m%d_%H%M%S")
SUMMARY_DIR: Path = Path(ALL_DIRS["summary_directory"])
USER_DOWNLOADS: Path = Path(Fops.get_downloads_folder())
WORKING_DIR: Path = Path(ALL_DIRS["working_directory"])
# endregion Constants

# region Variables
reports: dict = startup.load_json(file=Path("Data/reports.json").resolve())
longest_key: int = startup.length_check(strings=reports.keys())
config: dict = startup.load_json(file=Path("Data/config.json").resolve())
# endregion Variables


# region Startup
def initialize() -> tuple[Fops.FileOperator, Selene.Browser]:
    """Prepares directories for later functions."""
    if config["first_run"]:
        config["first_run"] = False
        config["headless"] = False

        with open(
                file=Path("Data/config.json"),
                mode="w") as config_json:
            json.dump(
                obj=config,
                fp=config_json,
                indent=4)

    else:
        pass

    file_helper: Fops.FileOperator = Fops.FileOperator(
        archive=ARCHIVE_DIR,
        working_directory=WORKING_DIR,
        downloads=FINAL_DIR)

    startup.create_directories(
        file_manager=file_helper,
        directories=ALL_DIRS)

    if config["commencement_archive"]:
        startup.archive_all(file_manager=file_helper)
    else:
        pass

    browser: Selene.Browser = startup.browser_startup(
        driver_root=DRIVER_DIR,
        download_path=WORKING_DIR,
        headless=config["headless"])

    return file_helper, browser
# endregion Startup


# region Browser Operations
def browser_actions(browser: Selene.Browser,
                    url: str) -> tuple:
    """Prepares and performs actions using a Selenium-based Edge WebDriver."""
    _browser: Selene.Browser = browser
    # file_helper: Fops.FileOperator = file_manager
    attempt_counter: int = 0
    click_attempt: bool = False

    while True:
        try:
            _browser.get_url(url=url)
            time.sleep(3)

            _browser.take_screenshot(Path(
                DRIVER_DIR,
                f"screenshot_{NAME_TIMESTAMP}.png"))

            # _browser.switch_last_frame()  # Uncomment this if SP has transitioned to hiding behind frames.

            _browser.click_element_xpaths(
                "//button[@class='vcMenuBtn']",
                "//button[@title='Export data']",
                "//span[contains(text(), 'Data with current layout')]",
                "//button[contains(text(), 'Export')]")

            click_attempt = True
            break

        except Selene.TimeoutException:
            browser.restart()
            time.sleep(3)

            if attempt_counter == 5:
                break
            else:
                attempt_counter += 1

    sleep_counter: int = 0

    if not str(config["extension"]).startswith("."):
        config["extension"] = f".{config['extension']}"
    else:
        pass

    while len([*WORKING_DIR.glob(f"*{config['extension']}")]) < 1:
        time.sleep(1)
        sleep_counter += 1

        if sleep_counter == 20:
            break
        else:
            continue

    return click_attempt, attempt_counter
# endregion Browser Operations


# region Main Function
def main() -> None:
    warnings.filterwarnings(
        action="ignore",
        category=UserWarning,
        module="openpyxl")

    file_helper, browser = initialize()
    list_summaries: dict = {}

    for list_name, list_url in sorted(reports.items()):
        success_flag, attempt_count = browser_actions(
            browser=browser,
            url=list_url)

        if success_flag is False:
            list_summaries[list_name] = f"Failed after {attempt_count}."
        else:
            for file in WORKING_DIR.iterdir():
                if file.is_file():

                    if config["timestamp"]:
                        file: Path = file_helper.rename_with_timestamp(
                            file=file,
                            new_name=list_name)
                    else:
                        pass

                    row_count: int = DFCheck.df_row_count(file=file)

                    print(f"{list_name:{longest_key}} {'|':^5} {row_count:,}")
                    list_summaries[list_name] = f"{row_count:04} - attempt #: {attempt_count}"

                    if config["completion_archive"]:
                        file_helper.archive_working_directory()
                    else:
                        file_helper.working_to_downloads()

    with open(
            file=f"{SUMMARY_DIR}/Summary_{NAME_TIMESTAMP}.json",
            mode="w") as summary_json:

        json.dump(
            obj=list_summaries,
            fp=summary_json,
            indent=4)

    file_helper.remove_working_directory()
# endregion Main Function


if __name__ == '__main__':
    main()
