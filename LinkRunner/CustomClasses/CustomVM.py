from dataclasses import dataclass
from rich.console import Console, ConsoleOptions, RenderResult
from rich.table import Table


@dataclass
class VirtualMachine:
    environment: str
    location: str
    name: str
    type: str
    comment: str

    def __post_init__(self):
        self.alias = self.name

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        yield f"[b]Machine:[/b] #{self.name}"
        table = Table("Environment", "Location", "Name", "Type", "Comment")
        table.add_row(self.environment, self.location, self.name, self.type, self.comment)
        yield table

