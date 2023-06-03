class Command:
    def __init__(self, commands: iter):
        if type(commands) == dict:
            self.cmd_keys: list = [key for key in commands.keys]
            self.cmd_alias: list = [value for value in commands.values()]
            self.commands: dict = commands
        else:
            self.cmd_keys: list = [key for key, cmd in enumerate(commands, 1)]
            self.cmd_alias: list = commands
            self.commands: dict = {key: value for key, value in zip([k for k, c in enumerate(commands, 1)],
                                                                    [c for c in commands])}
