#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević
# filename: game.py
# created: 2022-09-04 23:52


from abc import ABC, abstractmethod
import pygame
import sys


class Game(ABC):
    """
    Abstract game class.
    """

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        """
        Constructor.
        :param screen:
        """
        self._screen = screen
        self._clock = clock
        self._game_running = False

    @property
    def screen(self) -> pygame.Surface:
        """Getter."""
        return self._screen

    @property
    def clock(self) -> pygame.time.Clock:
        """Returns the clock attribute."""
        return self._clock

    @property
    def game_running(self) -> bool:
        """Getter."""
        return self._game_running

    @game_running.setter
    def game_running(self, other: bool) -> None:
        """Setter."""
        self._game_running = other

    @abstractmethod
    def mainloop(self) -> None:
        """Main game loop. Must be implemented in the child class."""
        pass

    @staticmethod
    def terminate() -> None:
        """Terminates the game."""
        pygame.quit()
        sys.exit()
