import enum


Direction = tuple[int, int]  # Typalias für Tupel mit zwei int-Werten

RIGHT: Direction = (1, 0)
LEFT: Direction = (-1, 0)
UP: Direction = (0, -1)
DOWN: Direction = (0, 1)


# Command class as enum
class Command(enum.Enum):
    UP = UP
    DOWN = DOWN
    LEFT = LEFT
    RIGHT = RIGHT
    EXIT = enum.auto()
