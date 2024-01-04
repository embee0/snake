import curses
from random import randint

from world import World

from constants import Command

key2command = {
    curses.KEY_UP: Command.UP,
    curses.KEY_DOWN: Command.DOWN,
    curses.KEY_LEFT: Command.LEFT,
    curses.KEY_RIGHT: Command.RIGHT,
    27: Command.EXIT,  # ESC-Taste
}


#### VIEW ############################################################
class TextUI:
    def __init__(self, world: World) -> None:
        self.window: curses.window = self.init_curses(world)
        self.command = Command.RIGHT

    def init_curses(self, world: World) -> curses.window:
        curses.initscr()  # initialize
        window = curses.newwin(world.height, world.width, 0, 0)
        window.keypad(True)  # enable keypad
        curses.noecho()  # turn off automatic echoing of keys to the screen
        curses.curs_set(0)  # hide the cursor
        window.nodelay(True)  # makes it possible to not wait for the user input
        return window

    def draw(self, world: World) -> None:
        self.window.clear()  # NEU (evtl ineffizienter als die vorige Version)
        self.window.border(0)
        self.window.addstr(0, 2, "Score: " + str(world.score) + " ")
        self.window.addstr(0, 27, " SNAKE! ")
        food_x, food_y = world.food
        self.window.addch(food_y, food_x, "O")
        for x, y in world.snake:
            self.window.addch(y, x, "#")

    def refresh_and_get_command(self) -> Command:
        # refreshes the screen and then waits for the user to hit a key
        # TODO: Trennung der Darstellung vom Abfragen der Events
        key = self.window.getch()
        self.command = key2command.get(key, self.command)
        return self.command

    def timeout(self, new_timeout: int) -> None:
        self.window.timeout(new_timeout)

    def addch(self, y: int, x: int, char: str) -> None:
        self.window.addch(y, x, char)

    def game_aborted(self) -> bool:
        return self.command == Command.EXIT

    def close(self) -> None:
        curses.endwin()
