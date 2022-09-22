#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from __future__ import annotations

import src.utils as utils

from typing import Generator, Iterable, TYPE_CHECKING
if TYPE_CHECKING:
    from .particle import Particle


class Neighbours(dict):
    """Neighbours class."""

    class Neighbour(object):
        """Neighbour class."""

        def __init__(self, node: Particle, distance: float):
            self._node = node
            self._distance = distance

        @property
        def node(self) -> Particle:
            """Getter."""
            return self._node

        @property
        def distance(self) -> float:
            """Getter."""
            return self._distance

        @distance.setter
        def distance(self, other: float) -> None:
            """Setter."""
            self._distance = other

        def __str__(self):
            """To string."""
            return f"Neighbour(node:{self.node}, distance: {self.distance})"

        def __repr__(self):
            """Repr."""
            return self.__str__()

        def __lt__(self, other: Neighbours.Neighbour) -> bool:
            """Returns the closest neighbour."""
            return self.distance < other.distance

    def __init__(self):
        """Constructor."""
        super().__init__()
        for direction_value in utils.MAP_NEIGHBOURS_DIRECTIONS_VALUES.value:
            self[utils.Directions(direction_value)] = None

    def __str__(self) -> str:
        """To string method."""
        output = f"Neighbours:\n"
        for direction, neighbour in self.items():
            output += f"\t{direction}: {neighbour.__str__()}\n"
        return output

    def __repr__(self) -> str:
        """Representational method."""
        return self.__str__()

    def add_new(self, direction: utils.Directions, neighbour: Particle, distance: float) -> bool:
        """
        Adds a new neighbour to the given side.
        Side must be integer in range [0, 3] (Direction enum!).
        :param direction:
        :param neighbour:
        :param distance:
        :return:
        """
        if direction != utils.Directions.UNDEFINED:
            self[direction] = Neighbours.Neighbour(node=neighbour, distance=distance)
            return True
        return False

    def get(self, direction: utils.Directions) -> Particle | None:
        """Returns the neighbour node on the given direction."""
        neighbour = self[direction]
        if neighbour:
            return neighbour.node
        return None

    def get_with_distance(self, direction: utils.Directions) -> Neighbours.Neighbour | None:
        """Returns the neighbour on the given direction."""
        return self[direction]

    def get_all(self) -> Generator[Particle]:
        """Returns all neighbours's node."""
        return (neighbour.node for neighbour in self.values() if neighbour)

    def get_all_directions(self) -> Generator[utils.Directions]:
        """Returns all directions."""
        for direction in self:
            yield direction if self[direction] else None

    def get_all_with_distance(self) -> Iterable[Particle]:
        """Returns all neighbours."""
        return list(self.values())

    def get_all_existing(self) -> Generator[Particle]:
        """Returns all the existing neighbours."""
        for neighbour in self.get_all():
            if neighbour is not None:
                yield neighbour
