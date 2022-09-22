#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from __future__ import annotations
from enum import Enum, unique
import pygame


@unique
class Directions(Enum):
    """All possible directions."""

    TOP = 2
    RIGHT = 1
    BOTTOM = -2
    LEFT = -1
    UNDEFINED = 0

    @classmethod
    def get_opposite(cls, direction: Directions) -> Directions:
        """Returns the opposite direction."""
        if isinstance(direction, cls):
            return cls(-1 * direction.value)
        return cls.UNDEFINED

    @staticmethod
    def get_direction_by_keypress(key: pygame.key) -> Directions:
        """Returns the direction."""
        if key == pygame.K_UP:
            return Directions.TOP
        elif key == pygame.K_RIGHT:
            return Directions.RIGHT
        elif key == pygame.K_DOWN:
            return Directions.BOTTOM
        elif key == pygame.K_LEFT:
            return Directions.LEFT
        return Directions.UNDEFINED
