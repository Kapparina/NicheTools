# Built-in library packages:
import os

# External library packages:
from selenium import webdriver as wd
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Project-specific library packages:
from .FileOperations import create_directory


def create_service(root_directory: str) -> EdgeService:
    """Installs an Edge WebDriver executable file and returns a Service to be used by an Edge WebDriver."""
    root: str = str(create_directory(path=root_directory))

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
                  service: EdgeService) -> wd.Edge:
    """Creates a Selenium-based Edge WebDriver."""
    driver: wd.Edge = wd.Edge(options=options,
                              service=service)

    return driver
