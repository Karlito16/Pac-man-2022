#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


import pygame


class CustomEvents(object):
    """User events class."""

    _NUM_OF_EVENTS = 0
    _EVENTS = dict()

    class Event(object):

        def __init__(self, interval: int, callback_function: callable):
            """Constructor."""
            self._interval = interval   # miliseconds
            self._callback_function = callback_function
            self._event_id = CustomEvents._NUM_OF_EVENTS + 1
            CustomEvents._NUM_OF_EVENTS += 1
            self._event = pygame.USEREVENT + self._event_id
            CustomEvents._EVENTS[self._event] = self
            pygame.time.set_timer(self._event, self._interval)

        def __del__(self):
            """Class destructor."""
            del CustomEvents._EVENTS[self._event]
            CustomEvents._NUM_OF_EVENTS -= 1

        def call(self):
            """Calls the callback function."""
            self._callback_function()

        @property
        def event(self):
            """Getter."""
            return self._event

    @classmethod
    def new(cls, interval: int, callback_function: callable):
        """Creates new Event object."""
        return cls.Event(interval=interval, callback_function=callback_function)

    @classmethod
    def events(cls):
        """Returns all the existing events."""
        return cls._EVENTS.keys()

    @classmethod
    def process(cls, event: Event):
        """Processes the given event."""
        cls._EVENTS[event].call()
