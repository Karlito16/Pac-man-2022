#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from __future__ import annotations
from enum import Enum, unique


@unique
class Directions(Enum):
    """All possible directions."""

    TOP = 2
    RIGHT = 1
    BOTTOM = -2
    LEFT = -1
    UNDEFINED = 0

    @staticmethod
    def get_opposite(direction: Directions) -> Directions:
        """Returns the opposite direction."""
        if isinstance(direction, Directions):
            return Directions(-1 * direction.value)
        return Directions.UNDEFINED
