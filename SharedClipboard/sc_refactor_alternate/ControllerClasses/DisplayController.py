import shutil


class Display:
    """Controller class responsible for displaying data."""

    def __init__(self, environment: str = "cli"):
        self.environment = environment
        if environment == "cli":
            self.width: float = self.cli_size()[0]
            self.height: float = self.cli_size()[1]
        else:
            pass

    def cli_size(self):
        """Returns the height and width of the active terminal window."""
        self.width, self.height = shutil.get_terminal_size()
        return self.width, self.height
