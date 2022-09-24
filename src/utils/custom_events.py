#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from __future__ import annotations

from typing import Callable, Iterable
import pygame


class CustomEvents(object):
    """User events class."""

    _ID_GENERATOR = 0
    _EVENTS = dict()

    class Event(object):

        def __init__(self, interval: int, callback_function: Callable, event_type: int, event_id: int, loops: int = 0):
            """Constructor."""
            self._interval = interval   # miliseconds
            self._callback_function = callback_function
            self._event_type = event_type
            self._event_id = event_id
            self._loops = loops

            CustomEvents._EVENTS[self.event_type] = (self, self._loops)
            pygame.time.set_timer(self.event_type, self._interval, self._loops)

        def __str__(self):
            """To string."""
            return f"Event({self._event_id})"

        def __repr__(self):
            """Representational method."""
            return self.__str__()

        def __eq__(self, other: CustomEvents.Event) -> bool:
            """Equals method."""
            return self._event_id == other._event_id

        def __call__(self) -> None:
            """Calls the callback function."""
            self._callback_function()

        @property
        def event_id(self) -> int:
            """Getter."""
            return self._event_id

        @property
        def event_type(self) -> int:
            """Getter."""
            return self._event_type

    @classmethod
    def _generate_event_type(cls) -> int:
        """Generates first available event id."""
        increment = 1
        while True:
            event_type = pygame.USEREVENT + increment
            if event_type not in cls._EVENTS.keys():
                cls._EVENTS[event_type] = None
                return event_type
            increment += 1

    @classmethod
    def new(cls, interval: int, callback_function: Callable, loops: int = 0) -> Event:
        """Creates new Event object."""
        event_type = cls._generate_event_type()
        event_id = cls._ID_GENERATOR
        cls._ID_GENERATOR += 1
        return cls.Event(interval=interval, callback_function=callback_function, event_type=event_type, event_id=event_id, loops=loops)

    @classmethod
    def events(cls) -> Iterable[int, ]:
        """Returns all the existing events."""
        return cls._EVENTS.keys()

    @classmethod
    def process(cls, event_type: int) -> None:
        """Processes the given event."""
        event, loop = cls._EVENTS[event_type]
        event()
        if loop == 0:   # do not delete events that should run infinitly!
            return None
        loop -= 1
        if loop == 0:
            cls.delete(event=event)
        else:
            cls._EVENTS[event_type] = (event, loop)
        return None

    @classmethod
    def delete(cls, event: Event) -> None:
        """Deletes the event."""
        # must compare events because event types are reusable after deleting!
        if event.event_type in cls._EVENTS.keys() and cls._EVENTS[event.event_type][0] == event:
            del cls._EVENTS[event.event_type]
        return None
