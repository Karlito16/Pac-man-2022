#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from __future__ import annotations

from .directions import Directions
import src.utils as utils

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .particle import Particle


class Neighbours(dict):
    """Neighbours class."""

    def __init__(self):
        """Constructor."""
        super().__init__()
        for direction_value in utils.MAP_NEIGHBOURS_DIRECTIONS_VALUES.value:
            self[Directions(direction_value)] = None

    def __str__(self) -> str:
        """To string method."""
        output = f"Neighbours:\n"
        for direction, neighbour in self.items():
            output += f"\t{direction}: {neighbour.__str__()}\n"
        return output

    def __repr__(self) -> str:
        """Representational method."""
        return self.__str__()

    def add_new(self, direction: Directions, neighbour: Particle) -> bool:
        """
        Adds a new neighbour to the given side.
        Side must be integer in range [0, 3] (Direction enum!).
        :param direction:
        :param neighbour:
        :return:
        """
        if direction != Directions.UNDEFINED:
            self[direction] = neighbour
            return True
        return False
