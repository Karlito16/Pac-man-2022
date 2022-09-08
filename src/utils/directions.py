#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from enum import Enum, unique


@unique
class Directions(Enum):
    """All possible directions."""

    TOP = -1
    RIGHT = -2
    BOTTOM = 1
    LEFT = 2
    UNDEFINED = 0

    @staticmethod
    def get_opposite(direction):
        """Returns the opposite direction."""
        if isinstance(direction, Directions):
            return Directions(-1 * direction.value)
        return Directions.UNDEFINED
