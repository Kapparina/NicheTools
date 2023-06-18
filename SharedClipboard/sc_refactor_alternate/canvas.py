import pyperclip as clipboard
from tabulate import tabulate
import json
import textwrap
import os
import sys
import time
import shutil
from SharedClipboard.sc_refactor_alternate.ControllerClasses import Command, Display, Help, Index, Jason, Key
from SharedClipboard.sc_refactor_alternate.Dependencies import DisplayCLI

tabulate.PRESERVE_WHITESPACE = True

SAVED_DATA: Jason = Jason(path=r"C:/temp", file="clipboard.json")
COMMAND: Command = Command(commands={
    "help": ["help", "?"],
    "save": ["save", "s"],
    "load": ["load", "l"],
    "view": ["all", "a"],
    "delete": ["delete", "del", "d"],
    "wipe": ["wipe", "w", "clear"],
    "quit": ["quit", "q"],
})
DATA: dict = SAVED_DATA.load_file()






def view_all():
    if len(DATA.keys()) > 0:
        print(DisplayCLI.tabulate_data(data=DATA))
    else:
        print("No keys found!")


