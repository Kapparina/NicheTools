# Built-in library packages:
import os

# External library packages:
from selenium.webdriver.edge.webdriver import WebDriver as EdgeDriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Project-specific library packages:
from SharePointListExporter.Dependencies.FileOperations import create_directory


def create_service(root_directory: str) -> EdgeService:
    """Installs an Edge WebDriver executable file and returns a Service to be used by an Edge WebDriver."""
    root: str = str(create_directory(root_directory))

    os.environ['WDM_PROGRESS_BAR']: str = str(0)  # Disabling the progress bar during driver installation.

    driver_path: str = EdgeChromiumDriverManager(path=root).install()
    service: EdgeService = EdgeService(executable_path=driver_path)

    return service


def create_options(*args) -> EdgeOptions:
    """Creates an instance of EdgeOptions for use by an Edge WebDriver."""
    options: EdgeOptions = EdgeOptions()

    for arg in args:
        options.add_argument(argument=arg)

    return options


def create_driver(options: EdgeOptions,
                  service: EdgeService) -> EdgeDriver:
    """Creates a Selenium-based Edge WebDriver."""
    driver: EdgeDriver = EdgeDriver(
        options=options,
        service=service)

    return driver


def find_element_name(driver: EdgeDriver,
                      element: str) -> WebElement:
    found_element: WebElement = driver.find_element(
        by=By.NAME,
        value=element)

    return found_element


def wait_element_clickable(driver: EdgeDriver,
                           element_name: str) -> None:
    WebDriverWait(
        driver=driver,
        timeout=10).until(
            ec.element_to_be_clickable(
                mark=(
                    By.NAME,
                    element_name)))
