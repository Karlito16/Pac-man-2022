#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević

from __future__ import annotations
from .counter import Counter
from typing import Any


class CycleCounter(Counter):
    """Counter class."""

    _POSITIVE = 1
    _NEGATIVE = -1
    _INT_INTERVAL = 1

    def __init__(self, *args: Any, maintain_count_speed: bool = True, **kwargs: Any):
        """
        Constructor.
        """
        self._maintain_count_speed = maintain_count_speed
        super().__init__(*args, **kwargs)
        self._count_speed_func = self._pow_n_func
        self._direction = CycleCounter._POSITIVE

    def start(self) -> None:
        """Override."""
        self._count_speed_func = self._pow_n_func
        self._direction = CycleCounter._POSITIVE
        super().start()
        return None

    @classmethod
    def _max_sum(cls, speed: float) -> float:
        """Max sum of speeds which sum does not go over int interval (1)."""
        s = 0
        while s < CycleCounter._INT_INTERVAL:
            s += speed
        return s - speed

    def _count_next(self) -> float | None:
        """Override."""
        if self._done:
            return None
        ret_val = self._current

        next_val = self._current + self._count_speed * self._direction
        if next_val >= self._count_to and self._direction == CycleCounter._POSITIVE:
            # direction change
            self._direction = CycleCounter._NEGATIVE
            self._count_speed_func = self._root_n_func if self._maintain_count_speed else self._count_speed_func
            self._count_speed = self._count_speed_func(self._count_speed)
            self._current = self._current + (self._count_speed * self._direction) \
                if not self._count_int \
                else self._current + CycleCounter._max_sum(speed=self._count_speed) * self._direction
        elif next_val < self._count_from and self._direction == CycleCounter._NEGATIVE:
            # cycle end
            self._done = True
        else:
            self._current = next_val

        self._count_speed = self._count_speed_func(self._count_speed)
        return ret_val
