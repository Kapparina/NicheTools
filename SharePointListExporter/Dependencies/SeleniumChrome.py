import os

from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement

from SharePointListExporter.Dependencies.FileOperations import create_directory


def create_service(root_directory: str) -> ChromeService:
    """Installs a Chrome WebDriver executable file and returns a Service to be used by an Chrome WebDriver."""
    root: str = str(create_directory(root_directory))

    os.environ['WDM_PROGRESS_BAR']: str = str(0)  # Disabling the progress bar during driver installation.

    driver_path: str = ChromeDriverManager(path=root).install()
    service: ChromeService = ChromeService(executable_path=driver_path)

    return service


def create_options(*args) -> ChromeOptions:
    """Creates an instance of ChromeOptions for use by an Chrome WebDriver."""
    options: ChromeOptions = ChromeOptions()

    for arg in args:
        options.add_argument(argument=arg)

    return options


def create_driver(options: ChromeOptions,
                  service: ChromeService) -> ChromeDriver:
    """Creates a Selenium-based Chrome WebDriver."""
    driver: ChromeDriver = ChromeDriver(options=options,
                                        service=service)

    return driver
