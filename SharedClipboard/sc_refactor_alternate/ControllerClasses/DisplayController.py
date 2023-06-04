import shutil


class Display:
    """Controller class responsible for displaying data."""

    def __init__(self, environment: str = "cli"):
        self._environment: str = environment
        if environment == "cli":
            self._width: float = self.cli_size()[0]
            self._height: float = self.cli_size()[1]
        else:
            self._width = 0
            self._height = 0

# ------------ Properties: ------------

    @property
    def environment(self) -> str:
        """Environment property."""
        return self._environment

    @environment.setter
    def environment(self, value: str) -> None:
        self._environment = value

    @environment.deleter
    def environment(self) -> None:
        del self._environment

    @property
    def width(self) -> float:
        """Width property."""
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        self._width = value

    @width.deleter
    def width(self) -> None:
        del self._width

    @property
    def height(self) -> float:
        """Height property."""
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        self._height = value

    @height.deleter
    def height(self) -> None:
        del self._height

    @staticmethod
    def cli_size() -> tuple:
        """Returns the height and width of the active terminal window."""
        return shutil.get_terminal_size()
