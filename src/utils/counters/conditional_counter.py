#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from .counter import Counter


class ConditionalCounter(Counter):
    """Counter class."""

    def __init__(self, condition_function: callable, count_from: float, *args, **kwargs):
        """
        Constructor.
        """
        self._condition_function = condition_function
        super().__init__(count_from, 0, *args, **kwargs)

    def _count_next(self) -> float or None:
        """Override."""
        if self._done:
            return None

        ret_val = self._current
        self._current += self._count_speed

        if self._condition_function():
            self._done = True

        self._count_speed = self._pow_n_func(self._count_speed)
        return ret_val
