#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from .counter import Counter


class CycleCounter(Counter):
    """Counter class."""

    _POSITIVE = 1
    _NEGATIVE = -1

    # def __init__(self, count_from: float, count_to: float, count_speed: float, step_function: callable,
    #              resolve_function: callable, count_int: bool = False, count_speed_power: float = 1.0,
    #              count_repeat: int = 1, maintain_count_speed: bool = True):
    def __init__(self, *args, maintain_count_speed: bool = True, **kwargs):
        """
        Constructor.
        """
        self._maintain_count_speed = maintain_count_speed
        # super().__init__(count_from, count_to, count_speed, step_function, resolve_function,
        #                  count_int, count_speed_power, count_repeat)
        super().__init__(*args, **kwargs)
        self._count_speed_func = self._pow_n_func
        self._direction = CycleCounter._POSITIVE

    def start(self) -> None:
        """Override."""
        self._count_speed_func = self._pow_n_func
        self._direction = CycleCounter._POSITIVE
        super().start()
        return None

    def _count_next(self) -> float or None:
        """Override."""
        if self._done:
            return None
        ret_val = self._current

        next_val = self._current + self._count_speed * self._direction
        if next_val >= self._count_to and self._direction == CycleCounter._POSITIVE:
            # direction change
            self._direction = CycleCounter._NEGATIVE
            self._count_speed_func = self._root_n_func if self._maintain_count_speed else self._count_speed_func
            self._current += (self._count_speed * self._direction)
        elif next_val < self._count_from and self._direction == CycleCounter._NEGATIVE:
            # cycle end
            self._done = True
        else:
            self._current = next_val

        self._count_speed = self._count_speed_func(self._count_speed)
        return ret_val
