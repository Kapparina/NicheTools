from time import monotonic

from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.reactive import reactive
from textual.timer import Timer
from textual.widgets import Button, Header, Footer, Static


class TimeDisplay(Static):

    update_timer: Timer
    start_time = reactive(monotonic)
    time = reactive(0.0)
    total = reactive(0.0)

    def on_mount(self) -> None:
        self.update_timer: Timer = self.set_interval(1 / 60, self.update_time, pause=True)

    def update_time(self) -> None:
        self.time: float = self.total + (monotonic() - self.start_time)

    def watch_time(self, time: float) -> None:
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{hours:02,.0f}:{minutes:02.0f}:{seconds:05.2f}")

    def start(self) -> None:
        self.start_time: float = monotonic()
        self.update_timer.resume()

    def stop(self) -> None:
        self.update_timer.pause()
        self.total += monotonic() - self.start_time
        self.time: float = self.total

    def reset(self) -> None:
        self.total: float = 0
        self.time: float = 0


class Stopwatch(Static):

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id: event = event.button.id
        time_display: TimeDisplay = self.query_one(TimeDisplay)
        if event.button.id == "start":
            time_display.start()
            self.add_class("started")
        elif event.button.id == "stop":
            time_display.stop()
            self.remove_class("started")
        elif event.button.id == "reset":
            time_display.reset()

    def compose(self) -> ComposeResult:
        yield Button("Start", id="start", variant="success")
        yield Button("Stop", id="stop", variant="error")
        yield Button("Reset", id="reset")
        yield TimeDisplay("00:00:00.00")


class StopwatchApp(App):

    CSS_PATH = "stopwatch.css"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("a", "add_stopwatch", "Add"),
        ("r", "remove_stopwatch", "Remove"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield ScrollableContainer(Stopwatch(), Stopwatch(), Stopwatch(), id="timers")

    def action_toggle_dark(self) -> None:
        self.dark: bool = not self.dark

    def action_add_stopwatch(self) -> None:
        new_stopwatch: Stopwatch = Stopwatch()
        self.query_one("#timers").mount(new_stopwatch)
        new_stopwatch.scroll_visible()

    def action_remove_stopwatch(self) -> None:
        timers = self.query("Stopwatch")
        if timers:
            timers.last().remove()


if __name__ == "__main__":
    app = StopwatchApp()
    app.run()
