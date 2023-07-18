from pathlib import Path
from urllib import request

import numpy as np
import textual.message
from rich.align import VerticalCenter

import requests
import pandas as pd
from io import StringIO

from rich.text import Text
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll, ScrollableContainer
from textual.widgets import Button, ContentSwitcher, DataTable, Markdown

LINK = "file://melcorpsmb.apac.linkgroup.corp/BluePrism/SmartAuto/Process%20On%20Demand/Data/RPAVMLinks.html"


def fix_link(url: str) -> Path:
    if url.startswith("file:"):
        return Path(request.url2pathname(url.removeprefix("file:")))
    else:
        return Path(request.url2pathname(url))


class LinkRunnerApp(App[None]):
    CSS_PATH = "./Dependencies/styles.css"
    DATAFRAME = pd.read_html(fix_link(url=LINK), extract_links="body")[0].astype(str)
    DATAFRAME.dropna(axis="rows", how="all", inplace=True)
    DATAFRAME.replace(to_replace=[np.nan, None], value=str(), inplace=True)
    cols = [(str(col) for col in DATAFRAME.columns)]

    def compose(self) -> ComposeResult:
        with Horizontal(id="buttons"):
            yield Button("DataTable", id="data-table")
            yield Button("Markdown", id="markdown")

        with ContentSwitcher(initial="data-table"):
            # with ScrollableContainer(id="table-viewer"):
            yield DataTable(id="data-table")
            with VerticalScroll(id="markdown"):
                yield Markdown(self.DATAFRAME.to_markdown())

    @on(Button.Pressed)
    def content_switch(self, event: Button.Pressed) -> None:
        self.query_one(ContentSwitcher).current = event.button.id

    @on(DataTable.HeaderSelected)
    def sort_rows(self, event: DataTable.HeaderSelected) -> None:
        self.query_one(DataTable).sort(event.column_key)


    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*self.DATAFRAME.columns)
        table.add_rows(*[self.DATAFRAME.itertuples(index=False, name=None)])


if __name__ == "__main__":
    LinkRunnerApp().run()
