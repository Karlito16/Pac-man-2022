#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


class Counter(object):
    """Counter class."""

    def __init__(self, count_from: float, count_to: float, count_speed: float, step_function: callable,
                 resolve_function: callable, count_int: bool = False, count_speed_power: float = 1.0,
                 count_repeat: int = 1, round_on: int = 2):
        """
        Constructor.
        :param count_from:
        :param count_to:
        :param count_speed:
        :param step_function:
        :param resolve_function:
        :param count_int:
        :param count_speed_power:
        :param count_repeat:
        """
        self._count_from = count_from
        self._count_to = count_to
        self._count_speed = count_speed
        self._step_function = step_function
        self._resolve_function = resolve_function
        self._count_int = count_int
        self._count_speed_power = count_speed_power
        self._count_repeat = count_repeat
        self._round_on = round_on

        self._current = self._count_from
        self._current_repeat = 1
        self._count_speed_initial = self._count_speed
        self._counting = False
        self._done = False
        self._paused = False

        self._pow_n_func = lambda x: x ** self._count_speed_power
        self._root_n_func = lambda x: x ** (1 / self._count_speed_power)

    @property
    def counting(self) -> bool:
        """Getter."""
        return self._counting

    @property
    def paused(self) -> bool:
        """Getter."""
        return self._paused

    def _reinit(self):
        """Reinit."""
        self._current = self._count_from
        self._count_speed = self._count_speed_initial
        self._counting = True
        self._done = False
        self._paused = False

    def start(self) -> None:
        """Starts the counting."""
        self._reinit()
        self._current_repeat = 1
        return None

    def _repeat(self) -> None:
        """Repeats the count."""
        self._reinit()

    def pause(self) -> None:
        """Pauses the counting."""
        self._paused = True
        return None

    def unpause(self) -> None:
        """Unpause."""
        self._paused = False

    def end(self) -> None:
        """Ends the counting."""
        self._counting = False
        return None

    def _count_repeat_condition(self):
        """Count repeat condition."""
        return self._current_repeat <= self._count_repeat or self._count_repeat == -1

    def _count_next(self) -> float or None:
        """Next."""
        if self._done:
            return None

        ret_val = self._current
        self._current = self._current + self._count_speed

        if self._current >= self._count_to:
            self._done = True

        self._count_speed = self._pow_n_func(self._count_speed)
        return ret_val

    def next(self) -> None:
        """Next count (float)."""
        if self.counting and not self.paused and self._count_repeat_condition():
            next_count = self._count_next()
            if next_count is None:  # resolve function
                self._current_repeat += 1
                self._counting = self._count_repeat_condition()
                self._resolve_function()
                if self.counting:
                    self._repeat()
            else:
                self._step_function(int(next_count) if self._count_int else round(next_count, self._round_on))
        return None
