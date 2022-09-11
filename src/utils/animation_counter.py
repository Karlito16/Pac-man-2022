#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


class AnimationCounter(object):
    """Animation counter."""

    def __init__(self, count_from: int, count_to: int, step: float):
        """Constructor."""
        self._count_from = count_from
        self._count_to = count_to
        self._step = step
        self._step_original = self._step
        self._current = self._count_from
        self._counting = False

    def start(self):
        """Starts the counting."""
        self._current = self._count_from
        self._step = self._step_original
        self._counting = True

    @property
    def counting(self):
        """Getter."""
        return self._counting

    def _next_unlimited(self):
        """Returns the next count for counter that counts forever."""
        self._current += self._step
        return self._current - self._step

    def _next_limited(self):
        """Returns the next count for counter that does not count forever."""
        if not self._counting:
            raise IndexError("Counter is not counting!")
        if self._current + self._step >= self._count_to and self._step > 0:
            self._step *= (-1)
        self._current += self._step
        if self._current - self._step <= self._count_from and self._step < 0:
            self._counting = False
        # this return format will always return the lowest given value
        return self._current - self._step if self._counting else self._count_from

    def next(self):
        """Gets the next count."""
        return self._next_unlimited() if self._count_to == -1 else self._next_limited()

    def next_int(self):
        """Same as next, only it returns the integer value."""
        return int(self.next())
