from dataclasses import dataclass


@dataclass
class VirtualMachine:
    Environment: str
    Location: str
    Name: str
    Type: str
    Comment: str


