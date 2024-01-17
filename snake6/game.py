from interfaces import SnakeWorld, SnakeUI

# Man beachte: In dieser Datei kommen keine konkreten UI-Klassen vor, sondern nur die Interfaces.
# Der Code ist also vollkommen unabhängig von einer konkreten UI-Implementierung.


class SnakeGame:
    def __init__(self, world: SnakeWorld, ui: SnakeUI):
        self.world = world
        self.ui = ui

    def play(self) -> int:
        while not self.world.game_over:
            self.ui.draw(self.world)
            new_timeout = self.world.compute_timeout()
            self.ui.timeout(new_timeout)
            command = self.ui.get_command()
            if self.ui.game_aborted():
                break
            self.game_running = self.world.update(command)
        self.ui.close()
        return self.world.score
