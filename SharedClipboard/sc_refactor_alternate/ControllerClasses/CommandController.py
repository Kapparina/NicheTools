class Command:
    def __init__(self, commands: iter):
        self._dict_flag: bool
        self._commands: dict = commands
        if type(commands) != dict:
            self._dict_flag = False
        else:
            self._dict_flag = True

# ------------ Properties: ------------

    @property
    def commands(self) -> dict:
        """The commands property."""
        if self._dict_flag is False:
            return {key: value for key, value in zip(
                [k for k, c in enumerate(self._commands, 1)],
                [c for c in self._commands])}
        else:
            return self._commands

    @commands.setter
    def commands(self, value: iter) -> None:
        if type(value) != dict:
            self._dict_flag = False
        else:
            self._dict_flag = True
        self._commands = value

    @commands.deleter
    def commands(self) -> None:
        del self._commands

# ------------ Methods: ------------

    def list_keys(self) -> list:
        return [*self.commands.keys()]

    def list_values(self) -> list:
        return [*self.commands.values()]
