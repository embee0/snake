# Viertes Refactoring des Snake-Spiels von
# https://github.com/Carla-Codes/simple-snake-game-python/blob/main/snake.py

# Anpassungen:
# - Aufteilung in mehrere Dateien
# - Konstanten in constants.py ausgelagert
# - Wechsel zu (x, y)-Koordinaten (statt (y, x) bei curses)
# - Statt Tasten-Codes werden nun Kommandos (UP, DOWN, LEFT, RIGHT, EXIT) verwendet
#   -> kann später leichter auf andere Eingabemethoden (zB Maus, Smartphone-Lagesensor)
#      umgestellt werden
# Aber wir verwenden immer noch keine Interfaces (oder abstrakte Basisklassen), so
# dass die Klassen TextUI und World noch sehr stark aneinander gekoppelt sind
# und nicht einfach durch andere (zB eine GUI) ersetzt werden können.


from __future__ import annotations

from world import World
from curses_TUI import TextUI


#### GAME LOOP = CONTROL #############################################
def play_game(world: World, ui: TextUI) -> int:
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
def main() -> None:
    world: World = World(30, 60)
    ui = TextUI(world)
    score = play_game(world, ui)
    ui.close()
    print("\nScore: " + str(score))


if __name__ == "__main__":
    main()
