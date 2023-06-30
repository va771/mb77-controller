import dataclasses
from enum import Enum


@dataclasses.dataclass
class _MB77Command:
    req: bytes
    ack: bytes


class MB77Command(Enum):
    POWER_ON = _MB77Command(b"1", b"49")
    POWER_OFF = _MB77Command(b"2", b"50")
    PROGRAMMING_MODE_ON = _MB77Command(b"3", b"51")
    PROGRAMMING_MODE_OFF = _MB77Command(b"4", b"52")
