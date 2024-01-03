# 3. Refactoring des Snake-Spiels von
# https://github.com/Carla-Codes/simple-snake-game-python/blob/main/snake.py

# Anpassungen:
# - Wir vollziehen die Trennung von Modell und View. Deshalb:
# - Wechsel zu einer objektorientierten Lösung!
# - Klasse TextUI kapselt die curses-Funktionen
# - Klasse World kapselt die Spielwelt, d.h. das Modell
# - Veränderung der Welt wurde aus dem game loop in die Methode update()
#   der Klasse World ausgelagert
# Ansonsten ist diese Version bewusst noch sehr ähnlich zu snake2.py
# Insb. gibt es noch keine Interfaces (oder abstrakte Basisklassen), so
# dass die Klassen TextUI und World noch sehr stark aneinander gekoppelt sind
# und nicht einfach durch andere (zB eine GUI) ersetzt werden können.

from __future__ import annotations

import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint


#### MODEL ###########################################################
class World:
    def __init__(self, height: int, width: int):
        self.height: int = height
        self.width: int = width
        self.score = 0
        self.snake: list = [[5, 8], [5, 7], [5, 6]]
        self.food: list[int] = [10, 25]

    def snake_eats_food(self) -> bool:
        return self.snake[0] == self.food

    def crossed_boundary(self) -> bool:
        return (
            self.snake[0][0] == 0
            or self.snake[0][0] == self.height - 1
            or self.snake[0][1] == 0
            or self.snake[0][1] == self.width - 1
        )

    def has_eaten_itself(self) -> bool:
        return self.snake[0] in self.snake[1:]

    def generate_new_food_position(self):
        while True:
            self.food = [randint(1, self.height - 2), randint(1, self.width - 2)]
            if self.food in self.snake:
                continue
            return

    def move_snake(self, key: int) -> None:
        hy, hx = self.snake[0]
        if key == KEY_DOWN:
            self.snake.insert(0, [hy + 1, hx])
        elif key == KEY_UP:
            self.snake.insert(0, [hy - 1, hx])
        elif key == KEY_LEFT:
            self.snake.insert(0, [hy, hx - 1])
        elif key == KEY_RIGHT:
            self.snake.insert(0, [hy, hx + 1])

    def compute_timeout(self) -> int:
        return 140 - (len(self.snake) // 5 + len(self.snake) // 10) % 120

    def update(self, key: int) -> bool:
        self.move_snake(key)
        if self.crossed_boundary() or self.has_eaten_itself():
            return False
        if self.snake_eats_food():
            self.score += 1
            self.generate_new_food_position()
        else:
            _ = self.snake.pop()
        return True


#### VIEW ############################################################
class TextUI:
    def __init__(self, world: World) -> None:
        self.window: curses.window = self.init_curses(world)
        self.key = KEY_RIGHT

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
        self.window.addch(world.food[0], world.food[1], "O")
        for y, x in world.snake:
            self.window.addch(y, x, "#")

    def refresh_and_get_key(self) -> int:
        # refreshes the screen and then waits for the user to hit a key
        # TODO: Trennung der Darstellung vom Abfragen der Events
        event = self.window.getch()
        self.key = self.key if event == -1 else event
        return self.key

    def timeout(self, new_timeout: int) -> None:
        self.window.timeout(new_timeout)

    def addch(self, y: int, x: int, char: str) -> None:
        self.window.addch(y, x, char)

    def game_aborted(self) -> bool:
        return self.key == 27

    def close(self) -> None:
        curses.endwin()


#### GAME LOOP = CONTROL #############################################
def play_game(world: World, ui: TextUI) -> int:
    while True:
        if ui.game_aborted():
            break
        ui.draw(world)
        new_timeout = world.compute_timeout()
        ui.timeout(new_timeout)
        key = ui.refresh_and_get_key()
        game_running = world.update(key)
        if not game_running:
            break
    return world.score


#### MAIN ############################################################
def main() -> None:
    world: World = World(30, 60)
    ui = TextUI(world)
    score = play_game(world, ui)
    ui.close()
    print("\nScore: " + str(score))


if __name__ == "__main__":
    main()
