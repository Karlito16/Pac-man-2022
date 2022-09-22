#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from typing import Callable, Iterable
import pygame


class CustomEvents(object):
    """User events class."""

    _NUM_OF_EVENTS = 0
    _EVENTS = dict()

    class Event(object):

        def __init__(self, interval: int, callback_function: Callable, loops: int = 0):
            """Constructor."""
            self._interval = interval   # miliseconds
            self._callback_function = callback_function
            self._loops = loops
            self._event_id = CustomEvents._NUM_OF_EVENTS + 1
            CustomEvents._NUM_OF_EVENTS += 1
            self._event = pygame.USEREVENT + self._event_id
            CustomEvents._EVENTS[self._event] = self
            pygame.time.set_timer(self._event, self._interval, self._loops)

        def __del__(self) -> None:
            """Class destructor."""
            del CustomEvents._EVENTS[self._event_id]
            CustomEvents._NUM_OF_EVENTS -= 1
            return None

        def __call__(self) -> None:
            """Calls the callback function."""
            self._callback_function()

        @property
        def event(self) -> int:
            """Getter."""
            return self._event

    @classmethod
    def new(cls, interval: int, callback_function: Callable, loops: int = 0) -> Event:
        """Creates new Event object."""
        return cls.Event(interval=interval, callback_function=callback_function, loops=loops)

    @classmethod
    def events(cls) -> Iterable[int, ]:
        """Returns all the existing events."""
        return cls._EVENTS.keys()

    @classmethod
    def process(cls, event: Event) -> None:
        """Processes the given event."""
        cls._EVENTS[event]()
        return None
