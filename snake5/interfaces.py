from abc import ABC, abstractmethod

from constants import Command


class SnakeWorld(ABC):
    @abstractmethod
    def update(self, command: Command) -> bool:
        ...


class SnakeUI(ABC):
    @abstractmethod
    def draw(self, world: SnakeWorld) -> None:
        ...

    @abstractmethod
    def refresh_and_get_command(self) -> Command:
        ...

    @abstractmethod
    def game_aborted(self) -> bool:
        ...

    @abstractmethod
    def close(self) -> None:
        ...
