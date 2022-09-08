#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević
# filename: game.py
# created: 2022-09-04 23:52


import abc
import pygame
import sys


class Game(abc.ABC):
    """
    Abstract game class.
    """

    def __init__(self, screen, clock):
        """
        Constructor.
        :param screen:
        """
        self._screen = screen
        self._clock = clock

    @property
    def screen(self):
        """Getter."""
        return self._screen

    @property
    def clock(self):
        """Returns the clock attribute."""
        return self._clock

    @abc.abstractmethod
    def mainloop(self):
        """Main game loop. Must be implemented in the child class."""
        pass

    @staticmethod
    def terminate():
        """Terminates the game."""
        pygame.quit()
        sys.exit()
