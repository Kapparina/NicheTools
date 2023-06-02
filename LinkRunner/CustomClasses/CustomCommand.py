from dataclasses import dataclass


@dataclass
class Command:
    cmd_list: iter
