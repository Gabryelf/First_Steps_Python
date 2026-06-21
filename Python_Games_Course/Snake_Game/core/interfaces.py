from abc import ABC, abstractmethod
import pygame


class Renderable(ABC):

    @abstractmethod
    def draw(self, surface: pygame.Surface):
        pass


class Updatable(ABC):

    @abstractmethod
    def update(self):
        pass


class Positionable(ABC):

    @abstractmethod
    def get_position(self) -> tuple:
        pass