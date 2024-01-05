import pygame

from interfaces import SnakeUI, SnakeWorld
from constants import Command


GRID = 20
CWALL = (255, 255, 255)
CFELD = (0, 0, 0)
CSNAKE = (0, 255, 0)
CFOOD = (255, 0, 0)


key2command = {
    pygame.K_UP: Command.UP,
    pygame.K_DOWN: Command.DOWN,
    pygame.K_LEFT: Command.LEFT,
    pygame.K_RIGHT: Command.RIGHT,
    pygame.K_ESCAPE: Command.EXIT,
}


# Klasse orientiert sich an TextUI, aber mit pygame statt curses
class PygameUI(SnakeUI):
    def __init__(self, world: SnakeWorld) -> None:
        self.world = world
        self.command = Command.RIGHT
        self.init_pygame(world)

    def init_pygame(self, world: SnakeWorld) -> None:
        pygame.init()
        self.window = pygame.display.set_mode((world.width * GRID, world.height * GRID))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()

    def draw(self, world: SnakeWorld) -> None:
        self.window.fill(CWALL)
        pygame.draw.rect(
            self.window,
            CFELD,
            (
                GRID,
                GRID,
                world.width * GRID - 2 * GRID,
                world.height * GRID - 2 * GRID,
            ),
        )
        # Schreibe den Score oben in die Mauer, passend zur Grid-Größe
        font = pygame.font.SysFont("Arial", GRID)
        text = font.render("Score: " + str(world.score), True, CFELD)
        self.window.blit(text, (GRID, 0))
        # Zeichne Futter und Schlange
        food_x, food_y = world.food
        pygame.draw.rect(
            self.window,
            CFOOD,
            (food_x * GRID, food_y * GRID, GRID, GRID),
        )
        for x, y in world.snake:
            pygame.draw.rect(
                self.window,
                CSNAKE,
                (x * GRID, y * GRID, GRID, GRID),
            )
        pygame.display.update()

    def refresh_and_get_command(self) -> Command:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.command = Command.EXIT
            elif event.type == pygame.KEYDOWN:
                self.command = key2command.get(event.key, self.command)
        return self.command

    def timeout(self, new_timeout: int) -> None:
        frame_rate = 1000 // new_timeout
        self.clock.tick(frame_rate)

    def game_aborted(self) -> bool:
        return self.command == Command.EXIT

    def close(self) -> None:
        pygame.quit()
