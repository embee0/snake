from abc import ABC, abstractmethod

from constants import Command


class SnakeWorld(ABC):
    @abstractmethod
    def update(self, command: Command) -> bool:
        pass


class SnakeUI(ABC):
    @abstractmethod
    def draw(self, world: SnakeWorld) -> None:
        """Stellt den aktuellen Zustand der Snake-Welt dar.
        (Abstrakte Methode, die von konkreten UI-Klassen implementiert werden muss.)"""
        pass

    @abstractmethod
    def timeout(self, new_timeout: int) -> None:
        """Setzt die Zeit in Millisekunden, die zwischen zwei Aktualisierungen
        der Snake-Welt vergehen soll."""
        pass

    @abstractmethod
    def get_command(self) -> Command:
        """Holt aus der UI die nächste Benutzereingabe
        (je nach UI: Tastendruck, Mausklick, Bewegungssensor, ...)"""
        pass

    @abstractmethod
    def game_aborted(self) -> bool:
        """Liefert True, wenn der Benutzer das Spiel abbrechen möchte.
        (Je nach UI: ESC-Taste, Mausklick auf "Quit", ...)"""
        pass

    @abstractmethod
    def close(self) -> None:
        """Schließt die UI, führt vorher je nach UI eventuelle Aufräumarbeiten durch."""
        pass
