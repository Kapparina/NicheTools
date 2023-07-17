from pathlib import Path
from typing import Iterable
import json
import string

import textual.css.query
from textual import events, on
from textual.app import App, ComposeResult, RenderResult
from textual.containers import ScrollableContainer, Horizontal, Vertical, Grid
from textual.reactive import reactive
from textual.screen import Screen, ModalScreen
from textual.validation import Validator, ValidationResult, Function
from textual.widgets import Static, Button, Header, Footer, Label, Input, Welcome, Pretty, DirectoryTree


class ValidPath(Validator):
    def validate(self, value: str) -> ValidationResult:
        if Path(value).is_dir():
            return self.success()
        else:
            return self.failure("No such directory exists!")


class ValidName(Validator):
    valid: reactive[bool] = False

    def validate(self, value: str) -> ValidationResult:
        if len(value) < 1:
            return self.failure("Enter a value!")
        elif value.startswith(tuple(string.digits)):
            return self.failure("The name cannot start with a number!")
        else:
            return self.success()


class Count(Static):
    count: reactive[int] = reactive(0)

    def on_mount(self) -> None:
        pass

    def watch_count(self, count: int) -> None:
        self.update(f"{count:^}")

    def previous_number(self) -> None:
        self.count -= 1

    def next_number(self) -> None:
        self.count += 1


class Counter(Static):
    name_value: str
    new_name: str
    start_count: int
    final_count: int

    def compose(self) -> ComposeResult:
        self.name_value = self.name

        if "^" in self.name:
            self.new_name, self.start_count = self.name.split(sep="^")
        else:
            self.new_name, self.start_count = (self.name, 0)

        self.border_title = self.new_name

        with Horizontal():
            with Vertical(id="left_column"):
                yield Button(
                    label="-1",
                    id="minus",
                    variant="error")

            with Vertical(id="middle_column"):
                new_count: Count = Count(
                    id="count",
                    name=self.new_name)
                new_count.count = self.start_count
                yield new_count

            with Vertical(id="right_column"):
                yield Button(
                    label="+1",
                    id="plus",
                    variant="success")

    @on(Button.Pressed)
    def plus_minus(self, event: Button.Pressed) -> None:
        button_id: event = event.button.id
        count: Count = self.query_one(Count)

        if button_id == "minus":
            count.previous_number()
        elif button_id == "plus":
            count.next_number()


class StartupScreen(ModalScreen[bool]):
    def compose(self) -> ComposeResult:
        with Grid(id="startup_prompt"):
            yield Label(
                renderable="Would you like to load data from a JSON file?",
                id="question")

            yield Button(
                label="Yes",
                id="load",
                variant="primary")

            yield Button(
                label="No",
                id="new")

    @on(Button.Pressed)
    def load_prompt(self, event: Button.Pressed) -> None:
        if event.button.id == "load":
            self.dismiss(True)
        else:
            self.dismiss(False)


class FileScreen(Screen[Path]):
    BINDINGS = [
        ("escape", "cancel", "Cancel")
    ]

    def action_cancel(self) -> None:
        self.dismiss(None)

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
        if event.path.is_file() and event.path.suffix == ".json":
            self.dismiss(event.path)
        else:
            pass


class CounterScreen(Screen):
    BINDINGS = [
        ("n", "add_counter", "Add New Counter")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

        with ScrollableContainer(id="counters"):
            pass


class CounterNameScreen(ModalScreen[str]):
    BINDINGS = [
        ("escape", "cancel", "Cancel")
    ]

    def action_cancel(self) -> None:
        self.dismiss(None)

    def compose(self) -> ComposeResult:
        with Grid(id="name_dialogue"):
            yield Label(
                renderable="Please name your counter:",
                id="name_prompt")

            yield Input(
                placeholder="Name, e.g. My_Counter_1",
                validators=[
                    ValidName(),
                    Function(self.no_counter_exists)],
                id="name_input")

            yield Pretty(
                object=["Enter something..."],
                id="name_validation")

    @on(Input.Changed)
    def show_invalid_reasons(self, event: Input.Changed) -> None:
        if not event.validation_result.is_valid:
            self.query_one(Pretty).update(event.validation_result.failure_descriptions)
        else:
            self.query_one(Pretty).update(["This name is valid!"])

    @on(Input.Submitted)
    def create_timer(self, event: Input.Submitted) -> None:
        if not event.validation_result.is_valid:
            self.query_one(Pretty).update(event.validation_result.failure_descriptions)
        else:
            self.dismiss(event.value)

    def no_counter_exists(self, value: str) -> bool:
        if len(value) >= 1:
            try:
                self.query_one(f"#{value}", Counter)
                return False
            except (textual.css.query.InvalidQueryFormat, StopIteration):
                pass
            except textual.css.query.NoMatches:
                return True
        else:
            pass


class CounterApp(App):
    CSS_PATH = "./counter.css"
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

    async def load_file(self, file: Path) -> None:
        if file is not None:
            with open(file=file) as f:
                self.tallies = json.load(f)

            await self.push_screen(CounterScreen())
            self.load_counters()
        else:
            pass

    def load_counters(self) -> None:
        for tally_name, tally_value in self.tallies.items():
            new_counter: Counter = Counter(name=f"{tally_name}^{tally_value}")
            self.query_one("#counters").mount(new_counter)

    def action_add_counter(self) -> None:
        def response(name: str | None) -> None:
            if name is not None:
                new_counter: Counter = Counter(
                    name=name,
                    id=name)
                self.query_one("#counters").mount(new_counter)
                new_counter.scroll_visible()
            else:
                pass

        self.push_screen(CounterNameScreen(), response)


if __name__ == '__main__':
    app = CounterApp()
    app.run()
