from __future__ import annotations

import enum

# from dataclasses import dataclass
# from types import NoneType
# from typing import ClassVar


Direction = tuple[int, int]  # Typalias für Tupel mit zwei int-Werten


# Command class as enum
class Command(enum.Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    EXIT = enum.auto()

    def is_opposite(self, other: Command) -> bool:
        return self.value[0] == -other.value[0] and self.value[1] == -other.value[1]


# @dataclass
# class Command:
#     value: Direction

#     UP: ClassVar[Direction] = (0, -1)
#     DOWN: ClassVar[Direction] = (0, 1)
#     LEFT: ClassVar[Direction] = (-1, 0)
#     RIGHT: ClassVar[Direction] = (1, 0)
#     EXIT: ClassVar[NoneType] = None
