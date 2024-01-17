# Sechstes Refactoring des Snake-Spiels von
# https://github.com/Carla-Codes/simple-snake-game-python/blob/main/snake.py

# Anpassungen:
# - Neu: Kivy-GUI
# - MVC-Struktur vollständig in Klassen separiert:
#   Controller: Funktion play_game in controller.py
#   Model: SnakeWorld-Interface, implementiert von World
#   View: SnakeUI-Interface, implementiert von TextUI, PygameUI, KivyUI
# - Interfaces (Python: abstract base class = ABC) eingeführt
# - Der Game Loop (play_game) ist nun unabhängig von der konkreten UI
# - Eine einfache graphische Oberfläche (mit Pygame) wurde hinzugefügt

# - TODO: Was noch gar nicht stimmt, ist der Umgang mit Zeit:
#   In den GUI-Versionen sollte die Bewegung der Schlange flüssiger
#   dargestellt werden, d.h. nicht nur "kästchenweise" wie in der Text-UI.
#   Dazu müsste die Schlange aber auch zwischen den Ticks der Game-Loop
#   weiterbewegt werden. Dafür muss aber das bisherige einfache Modell
#   mit timeouts aufgegeben werden.

import sys
from typing import Optional

from interfaces import SnakeWorld, SnakeUI
from game import SnakeGame

from world import World


def create_text_game(width: int, height: int) -> SnakeGame:
    from curses_TUI import TextUI

    world = World(width, height)
    ui = TextUI(world)
    game = SnakeGame(world, ui)
    return game


def create_pygame(width: int, height: int) -> SnakeGame:
    from pygame_GUI import PygameUI

    world = World(width, height)
    ui = PygameUI(world)
    game = SnakeGame(world, ui)
    return game


def create_kivy_game(width: int, height: int) -> SnakeGame:
    from kivy_GUI import KivyUI

    world = World(width, height)
    ui = KivyUI(world)
    game = SnakeGame(world, ui)
    return game


def show_usage():
    print(f"Aufruf: python snake6.py {'|'.join(POSSIBLE_COMMAND_LINE_ARGS)}")
    sys.exit(1)


#### MAIN ############################################################
def main(cmd_line_arg: str) -> None:
    game: Optional[SnakeGame] = None
    if cmd_line_arg == "kivy":
        game = create_kivy_game(30, 30)
    elif cmd_line_arg == "pygame":
        game = create_pygame(30, 30)
    elif cmd_line_arg == "text":
        game = create_text_game(30, 60)
    else:
        show_usage()
    assert game is not None  # Damit wird der Typechecker zufrieden gestellt ;-)
    score = game.play()
    print("\nScore: " + str(score))


def gui_interaktiv_auswaehlen(possible_args):
    print("Mögliche GUIs: ")
    for i, arg in enumerate(possible_args):
        print(i + 1, arg)
    while True:
        try:
            auswahl = int(input("Bitte Nummer eingeben: ")) - 1
            if auswahl in range(len(possible_args)):
                break
        except ValueError:
            pass
        print("Ungültige Eingabe")
    return possible_args[auswahl]


if __name__ == "__main__":
    POSSIBLE_COMMAND_LINE_ARGS = ["text", "pygame", "kivy"]
    cmd_line_arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd_line_arg not in POSSIBLE_COMMAND_LINE_ARGS:
        # show_usage()
        cmd_line_arg = gui_interaktiv_auswaehlen(POSSIBLE_COMMAND_LINE_ARGS)
    main(cmd_line_arg)
