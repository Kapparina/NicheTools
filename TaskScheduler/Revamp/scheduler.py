import schedule
from datetime import datetime, timedelta
import time
from pathlib import Path
from subprocess import Popen, CREATE_NO_WINDOW
import tomllib as toml
from dataclasses import dataclass, field


@dataclass
class Config:
    file: Path | str
    title: str = field(init=False)
    config: dict = field(init=False)

    def __post_init__(self) -> None:
        self.file = Path(self.file).resolve()
        self.config = self.load()
        self.title = self.config["title"]

    def load(self) -> dict:
        try:
            with open(
                    file=self.file,
                    mode="rb") as configuration:
                config: dict = toml.load(configuration)

            return config

        except toml.TOMLDecodeError:
            raise "Invalid TOML file - please provide a valid file!"


@dataclass
class Task:
    name: str
    frequency: str
    file: Path | str
    file_name: str = field(init=False)
    file_extension: str = field(init=False)

    def __post_init__(self) -> None:
        self.file = Path(self.file).resolve()
        self.file_name = self.file.name
        self.file_extension = self.file.suffix


class TaskHandler:
    handlers: dict = {
        "wscript": [".vbs", ".js"],
        "cmd /k": [".bat", ".cmd"],
        "powershell -ExecutionPolicy RemoteSigned": [".ps1"]}

    def select_application(self, task: Task):
        return next((k for k, v in self.handlers.items() if task.file_extension in v), None)

    def run(self, task: Task) -> None:
        application = self.select_application(task=task)
        Popen(
            f"{application} {task.file}",
            creationflags=CREATE_NO_WINDOW)



