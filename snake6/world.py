from random import randint
from typing import Optional

from interfaces import SnakeWorld
from constants import Command


#### MODEL ###########################################################
class World(SnakeWorld):
    def __init__(self, height: int, width: int):
        self.height: int = height
        self.width: int = width
        self.score = 0
        self.snake: list = [[8, 5], [7, 5], [6, 5]]
        self.food: list[int] = [25, 10]
        self.last_command: Command = Command.RIGHT
        self.game_over: bool = False

    def is_game_over(self) -> bool:
        return self.game_over

    def snake_eats_food(self) -> bool:
        return self.snake[0] == self.food

    def crossed_boundary(self) -> bool:
        headx, heady = self.snake[0]
        hit_wall = (
            headx == 0
            or headx == self.width - 1
            or heady == 0
            or heady == self.height - 1
        )
        if hit_wall:
            print("Die Schlange ist in die Wand gekracht!")
            self.game_over = True
        return hit_wall

    def has_eaten_itself(self) -> bool:
        hit_body = self.snake[0] in self.snake[1:]
        if hit_body:
            print("Die Schlange hat sich selbst gefressen!")
            self.game_over = True
        return hit_body

    def generate_new_food_position(self):
        while True:
            self.food = [randint(1, self.width - 2), randint(1, self.height - 2)]
            if self.food in self.snake:
                continue
            return

    def move_snake(self, command: Command) -> None:
        hx, hy = self.snake[0]
        dx, dy = command.value
        self.snake.insert(0, [hx + dx, hy + dy])

    def compute_timeout(self) -> int:
        return 140 - (len(self.snake) // 5 + len(self.snake) // 10) % 120
        # return 1000 - 100 * len(self.snake)

    def update(self, command: Command) -> bool:
        if command.is_opposite(self.last_command):
            command = self.last_command  # Ignoriere diesen Befehl
        self.last_command = command
        self.move_snake(command)
        if self.crossed_boundary() or self.has_eaten_itself():
            return False
        if self.snake_eats_food():
            self.score += 1
            self.generate_new_food_position()
        else:
            _ = self.snake.pop()
        return True
