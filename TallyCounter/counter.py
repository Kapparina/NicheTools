from pathlib import Path
from typing import Iterable
import tomlkit as tomk
import tomllib as toml

from textual import events, on
from textual.app import App, ComposeResult, RenderResult
from textual.containers import ScrollableContainer, Horizontal, Vertical, Grid
from textual.reactive import reactive
from textual.screen import Screen, ModalScreen
from textual.validation import Validator, ValidationResult
from textual.widgets import Static, Button, Header, Footer, Label, Input, Welcome, Pretty, DirectoryTree

# TODO: REMOVE THIS!
class Tally:
    name = str
    total: int

    def __init__(self, name: str) -> None:
        self._name = name
        self._total = 0

    @property
    def total(self) -> int:
        return self._total

    @total.setter
    def total(self, value: int) -> None:
        self._total = value

    def minus_one(self) -> None:
        self._total -= 1

    def plus_one(self) -> None:
        self._total += 1


class ValidPath(Validator):
    def validate(self, value: str) -> ValidationResult:
        if Path(value).is_dir():
            return self.success()
        else:
            return self.failure("No such directory exists!")


class Count(Static):
    count_name: str
    count: reactive[int] = reactive(0)

    def on_mount(self) -> None:
        self.count_name = self.name
        self.count = int(self.classes)
        # TODO: FIX THIS.

    def watch_count(self, count: int) -> None:
        self.update(f"{count:^}")

    def previous_number(self) -> None:
        self.count -= 1

    def next_number(self) -> None:
        self.count += 1


class Counter(Static):
    @on(Button.Pressed)
    def plus_minus(self, event: Button.Pressed) -> None:
        button_id: event = event.button.id
        count: Count = self.query_one(Count)

        if button_id == "minus":
            count.previous_number()
        elif button_id == "plus":
            count.next_number()

    def compose(self) -> ComposeResult:
        self.border_title = "test"

        with Horizontal():
            with Vertical(id="left_column"):
                yield Button(
                    label="-1",
                    id="minus",
                    variant="error")

            with Vertical(id="middle_column"):
                yield Count(id="count", name="bob")
                # TODO: FINISH THIS!

            with Vertical(id="right_column"):
                yield Button(
                    label="+1",
                    id="plus",
                    variant="success")


class StartupScreen(ModalScreen[bool]):
    def compose(self) -> ComposeResult:
        # yield Input(placeholder="Tally Name")
        with Grid(id="startup_prompt"):
            yield Label(
                renderable="Would you like to load data from a TXT file?",
                id="question")

            yield Button(
                label="Yes",
                id="load",
                variant="primary")

            yield Button(label="No", id="new", variant="default")

    @on(Button.Pressed)
    def load_prompt(self, event: Button.Pressed) -> None:
        if event.button.id == "load":
            self.dismiss(True)
        else:
            self.dismiss(False)


class FileScreen(Screen[Path]):
    def compose(self) -> ComposeResult:
        with Vertical(id="file_search"):
            yield Label(
                renderable="Provide a file path:",
                id="file_screen_label")

            yield Input(
                placeholder="e.g. C:\\Users\\John\\tallies.toml",
                validators=ValidPath(),
                id="dir_search_input")

            yield Pretty(
                object=["Nothing entered..."],
                id="dir_search_result")

            with ScrollableContainer(id="file_tree"):
                yield DirectoryTree(path=f"{Path().cwd()}")

    @on(Input.Changed)
    def show_invalid_reasons(self, event: Input.Changed) -> None:
        if not event.validation_result.is_valid:
            self.query_one(Pretty).update(event.validation_result.failure_descriptions)
        else:
            self.query_one(Pretty).update(["This directory exists!"])
            self.query_one(DirectoryTree).path = event.value

    @on(DirectoryTree.FileSelected)
    def show_valid_files(self, event: DirectoryTree.FileSelected) -> None:
        if event.path.is_file() and event.path.suffix == ".toml":
            self.dismiss(event.path)
        else:
            pass


class CounterScreen(Screen):
    def compose(self) -> ComposeResult:
        with ScrollableContainer(id="counters"):
            yield Header()
            yield Footer()
            yield Counter()


class CounterApp(App):
    CSS_PATH = "./counter.css"
    BINDINGS = [
        ("n", "add_counter", "Add Counter")
    ]
    tallies: dict

    def on_mount(self) -> None:
        self.startup_prompt()

    def startup_prompt(self) -> None:
        def response(load: bool) -> None:
            if load:
                self.push_screen(FileScreen(), self.load_file)
            else:
                self.push_screen(CounterScreen())

        self.push_screen(StartupScreen(), response)

    def load_file(self, file: Path) -> None:
        with open(
                file=file,
                mode="rb") as f:

            try:
                self.tallies: dict = toml.load(f)

                if len(self.tallies) < 1:
                    self.tallies: dict = {}

            except toml.TOMLDecodeError:
                self.tallies: dict = {}


if __name__ == '__main__':
    app = CounterApp()
    app.run()
