#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević

from __future__ import annotations
from .counter import Counter
from typing import Any, Callable


class ConditionalCounter(Counter):
    """Counter class."""

    def __init__(self, condition_function: Callable, count_from: float, *args: Any, **kwargs: Any):
        """
        Constructor.
        """
        self._condition_function = condition_function
        super().__init__(count_from, 0, *args, **kwargs)

    def _count_next(self) -> float | None:
        """Override."""
        if self._done:
            return None

        ret_val = self._current
        self._current += self._count_speed

        if self._condition_function():
            self._done = True

        self._count_speed = self._pow_n_func(self._count_speed)
        return ret_val
