# Fünftes Refactoring des Snake-Spiels von
# https://github.com/Carla-Codes/simple-snake-game-python/blob/main/snake.py

# Anpassungen:
# - Interfaces (Python: abstract base class = ABC) eingeführt
# - Der Game Loop (play_game) ist nun unabhängig von der konkreten UI
# - Eine einfache graphische Oberfläche (mit Pygame) wurde hinzugefügt

# - TODO: Was noch gar nicht stimmt, ist der Umgang mit Zeit:
#   In den GUI-Versionen sollte die Bewegung der Schlange flüssiger
#   dargestellt werden, d.h. nicht nur "kästchenweise" wie in der Text-UI.
#   Dazu müsste die Schlange aber auch zwischen den Ticks der Game-Loop
#   weiterbewegt werden. Dafür muss aber das bisherige einfache Modell
#   mit timeouts aufgegeben werden.

from __future__ import annotations
import sys

from interfaces import SnakeWorld, SnakeUI

from world import World
from curses_TUI import TextUI
from pygame_GUI import PygameUI


#### GAME LOOP = CONTROL #############################################
def play_game(world: SnakeWorld, ui: SnakeUI) -> int:
    game_running = True
    while game_running:
        ui.draw(world)
        new_timeout = world.compute_timeout()
        ui.timeout(new_timeout)
        command = ui.refresh_and_get_command()
        if ui.game_aborted():
            break
        game_running = world.update(command)
    return world.score


#### MAIN ############################################################
def main(cmd_line_arg: str) -> None:
    world: SnakeWorld = None
    ui: SnakeUI = None
    if cmd_line_arg == "pygame":
        world = World(30, 30)
        ui = PygameUI(world)
    elif cmd_line_arg == "text":
        world = World(30, 60)
        ui = TextUI(world)
    score = play_game(world, ui)
    ui.close()
    print("\nScore: " + str(score))


if __name__ == "__main__":
    POSSIBLE_COMMAND_LINE_ARGS = ["text", "pygame"]
    cmd_line_arg = sys.argv[1] if len(sys.argv) > 1 else None
    if cmd_line_arg not in POSSIBLE_COMMAND_LINE_ARGS:
        print("Aufruf: python snake5.py text|pygame")
        sys.exit(1)
    main(cmd_line_arg)
