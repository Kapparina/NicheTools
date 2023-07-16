import textual.containers
from textual.app import App, ComposeResult, RenderResult
from textual.containers import ScrollableContainer, HorizontalScroll, VerticalScroll
from textual.reactive import reactive
from textual.screen import Screen
from textual.timer import Timer
from textual.widget import Widget
from textual.widgets import Button, Static, Select, Placeholder
from datetime import datetime, timedelta
import random


CURRENT_DATETIME: str = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
DATETIME_FORMAT: str = "%d/%m/%Y - %H:%M:%S"
DELTA: timedelta = timedelta(seconds=300)


class Header(Placeholder):
    DEFAULT_CSS = """
    Header {
        height: 3;
        dock: top;
    }
    """


class Footer(Placeholder):
    DEFAULT_CSS = """
    Footer {
        height: 3;
        dock: bottom;
    }
    """


class PreviousRun(Static):
    def on_mount(self) -> None:
        self.update("Last run:\nNothing to report...")

    def refresh_time(self) -> None:
        self.update(f"Last run:\n{datetime.now().strftime(DATETIME_FORMAT)}")


class NextRun(Static):
    def on_mount(self) -> None:
        self.refresh_time()

    def refresh_time(self) -> None:
        self.update(f"Next run:\n{(datetime.now() + DELTA).strftime(DATETIME_FORMAT)}")


class Job(Placeholder):
    # TODO give the jobs a name when they're instantiated - likely from the config or something.
    pass


class JobListing(Static):
    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id: event = event.button.id
        previous_run: PreviousRun = self.query_one(PreviousRun)
        next_run: NextRun = self.query_one(NextRun)

        if button_id == "run":
            previous_run.refresh_time()
            next_run.refresh_time()

    def compose(self) -> ComposeResult:
        yield Job(
            label=f"Job",
            id=f"job")
        yield Button(
            label="Run Now",
            id="run",
            variant="success")
        yield PreviousRun(id="previous")
        yield NextRun(id="next")


class SchedulerScreen(Screen):

    CSS_PATH = "./scheduler.css"
    BINDINGS = [
        ("a", "add_job", "Add New Job")
    ]

    def compose(self) -> ComposeResult:
        yield Header(id="Header")
        yield Footer(id="Footer")
        with ScrollableContainer(id="jobs"):
            yield JobListing()
            yield JobListing()
            yield JobListing()


class SchedulerApp(App):
    def on_mount(self) -> None:
        self.push_screen(SchedulerScreen())

    def action_add_job(self) -> None:
        new_job_listing: JobListing = JobListing()
        self.query_one("#jobs").mount(new_job_listing)
        new_job_listing.scroll_visible()


if __name__ == '__main__':
    app = SchedulerApp()
    app.run()
