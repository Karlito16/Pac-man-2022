#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from typing import Any


class PacmanConstant(object):
    """Pacman constants."""

    def __init__(self, value: Any):
        """
        Constructor
        :param value: any type
        """
        self._value = value

    @property
    def value(self) -> Any:
        """Getter."""
        return self._value
