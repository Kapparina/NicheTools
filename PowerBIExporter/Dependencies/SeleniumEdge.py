import os
from typing import Any

from selenium.webdriver.edge.webdriver import WebDriver as EdgeDriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.common.exceptions import TimeoutException


class Browser:
    Service: EdgeService
    Options: EdgeOptions
    Driver: EdgeDriver
    Wait: WebDriverWait

    def __init__(self):
        self.Service = EdgeService()
        self.Options = EdgeOptions()
        self.Options.add_argument("user-agent=Mozilla/5.0")

    # region Private Methods
    def _await_element_xpath(self, element: str) -> Any:
        """Returns whether a WebElement could be located via xpath."""
        return self.Wait.until(
            ec.presence_of_element_located((
                By.XPATH,
                element)))

    def _click_element_name(self, element: str) -> None:
        """Attempts to locate and click on an element using element name."""
        self.Wait.until(
            ec.element_to_be_clickable(mark=(
                By.NAME,
                element))).click()

    def _click_element_xpath(self, element: str) -> None:
        """Attempts to locate and click on an element using xpath."""
        self.Wait.until(
            ec.element_to_be_clickable(mark=(
                By.XPATH,
                element))).click()

    def _find_frame_xpath(self, frame: str) -> WebElement:
        """Attempts to locate a frame tag using xpath."""
        return self.Driver.find_element(
            by=By.XPATH,
            value=frame)
    # endregion Private Methods

    # region Instantiation Methods
    def add_service(self, directory: str) -> None:
        """Installs and adds a Selenium Edge WebDriver executable to the Browser."""
        os.environ["WDM_PROGRESS_BAR"]: str = str(0)
        service_path: str = EdgeChromiumDriverManager(path=directory).install()
        self.Service = EdgeService(executable_path=service_path)

    def add_options(self, *options) -> None:
        """Adds options to the Browser's Options attribute."""
        for option in options:
            self.Options.add_argument(argument=option)

    def add_driver(self) -> None:
        """Instantiates a Selenium Edge WebDriver."""
        self.Driver = EdgeDriver(
            options=self.Options,
            service=self.Service)

        self.Wait = WebDriverWait(
            driver=self.Driver,
            timeout=10)

        self.Driver.implicitly_wait(time_to_wait=2)
    # endregion Instantiation Methods

    # region Instance Methods
    def click_element_names(self, *elements) -> None:
        """Attempts to click on any number of parsed elements using element names."""
        for element in elements:
            self._click_element_name(element=element)

    def click_element_xpaths(self, *elements) -> None:
        """Attempts to click on any number of parsed elements using xpath."""
        for element in elements:
            self._click_element_xpath(element=element)

    def get_url(self, url: str) -> None:
        """Performs a HTTP request."""
        self.Driver.get(url=url)

    def restart(self) -> None:
        """Restarts the Browser's Driver."""
        self.Driver.close()
        self.add_driver()

    def switch_frame(self, frame: str) -> None:
        """Switches the Browser's Driver to a parsed frame."""
        found_frame: Any = self._await_element_xpath(element=frame)
        self.Wait.until(
            ec.frame_to_be_available_and_switch_to_it(found_frame))

    def switch_last_frame(self) -> None:
        """Switches the Browser's Driver to the last frame located using xpath."""
        last_frame: Any = self._await_element_xpath(element="(//iframe)[last()]")
        self.Wait.until(
            ec.frame_to_be_available_and_switch_to_it(last_frame))

    def take_screenshot(self, name: Any) -> None:
        """Takes a screenshot."""
        self.Driver.get_screenshot_as_file(filename=name)
    # endregion Instance Methods
