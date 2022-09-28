#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević
# filename: app.py
# created: 2022-09-04 23:52


from abc import ABC, abstractmethod
import pygame
import sys


class App(ABC):
    """
    Abstract app class.
    """

    def __init__(self, window: pygame.Surface, clock: pygame.time.Clock):
        """
        Constructor.
        :param screen:
        """
        self._window = window
        self._clock = clock
        self._app_running = False
        self._app_events = None

    @property
    def window(self) -> pygame.Surface:
        """Getter."""
        return self._window

    @property
    def clock(self) -> pygame.time.Clock:
        """Returns the clock attribute."""
        return self._clock

    @property
    def app_running(self) -> bool:
        """Getter."""
        return self._app_running

    @app_running.setter
    def app_running(self, other: bool) -> None:
        """Setter."""
        self._app_running = other

    @property
    def app_events(self) -> list[pygame.event.Event]:
        """Getter."""
        return self._app_events

    def catch_new_app_events(self) -> None:
        """Setter."""
        self._app_events = pygame.event.get()
        return None

    @abstractmethod
    def mainloop(self) -> None:
        """Main app loop. Must be implemented in the child class."""
        pass

    @staticmethod
    def terminate() -> None:
        """Terminates the app."""
        pygame.quit()
        sys.exit()
