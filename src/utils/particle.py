#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from __future__ import annotations

from .directions import Directions
from .neighbours import Neighbours

from typing import Hashable, TYPE_CHECKING
import math

if TYPE_CHECKING:
    from ..map.components.elementary import GridSlotType, NodeType


class Particle(object):
    """Particle class."""

    def __init__(self, i: int, j: int, size: int, type_: GridSlotType | NodeType):
        """
        Constructor.
        :param i:
        :param j:
        :param type_:
        """
        self._i = i
        self._j = j
        self._size = size
        self._type = type_
        self._neighbours = Neighbours()

    def __str__(self) -> str:
        """To string method."""
        output = f"""{str(self.__class__).split('.')[-1].strip("'>")}(i={self.i},j={self.j},type={self.type})"""
        return output

    def __repr__(self) -> str:
        """How the class object should be displayed."""
        return self.__str__()

    def __eq__(self, other: Particle) -> bool:
        """Checks if two particles are equal."""
        if isinstance(other, self.__class__):
            return self.i == other.i and self.j == other.j
        return False

    def __hash__(self) -> Hashable:
        """Hashable type method."""
        return f"{self.i}{self.j}".__hash__()

    def __sub__(self, other: Particle) -> float | None:
        """Returns the distance between two particles."""
        if isinstance(self, Particle) and isinstance(other, Particle):
            return math.sqrt(math.pow(self.i - other.i, 2) + math.pow(self.j - other.j, 2))
        return None

    # def __del__(self) -> None:
    #     """Destructor method."""
    #     del self._i
    #     del self._j
    #     del self._type
    #     del self._neighbours
    #     return None

    @property
    def i(self) -> int:
        """Getter."""
        return self._i

    @property
    def j(self) -> int:
        """Getter."""
        return self._j

    @property
    def pos(self) -> tuple[int, int]:
        """Returns the (i,j) position."""
        return self.i, self.j

    @property
    def size(self) -> int:
        """Getter."""
        return self._size

    @property
    def type(self) -> GridSlotType | NodeType:
        """Getter."""
        return self._type

    @type.setter
    def type(self, value: GridSlotType | NodeType) -> None:
        """Setter."""
        if isinstance(value, self._type.__class__):
            self._type = value

    @property
    def neighbours(self) -> Neighbours:
        """Getter."""
        return self._neighbours

    def add_neighbour(self, neighbour: Particle, direction: Directions = None, distance: float = None) -> bool:
        """Syntatic sugar method."""
        if isinstance(neighbour, Particle):
            direction = Particle.get_direction(particle1=self, particle2=neighbour) if direction is None else direction
            distance = distance if distance is not None else abs(self - neighbour)
            return self._neighbours.add_new(direction=direction, neighbour=neighbour, distance=distance)
        return False

    @classmethod
    def get_direction(cls, particle1: Particle, particle2: Particle) -> Directions:
        """Returns the direction from particle1 to the particle2."""
        if isinstance(particle1, cls) and isinstance(particle2, cls) and particle1 != particle2:
            # top or bottom
            if particle1.i == particle2.i:
                return Directions.TOP if particle1.j > particle2.j else Directions.BOTTOM
            # left or right
            elif particle1.j == particle2.j:
                return Directions.RIGHT if particle1.i < particle2.i else Directions.LEFT
            # diagonal?
        return Directions.UNDEFINED

    @classmethod
    def connect(cls, particle_1: Particle, particle_2: Particle, direction: Directions = None, distance: float = None) -> bool:
        """Connects the two particles."""
        direction = direction if direction is not None else Particle.get_direction(
            particle1=particle_1,
            particle2=particle_2
        )
        distance = distance if distance is not None else abs(particle_1 - particle_2)
        if isinstance(particle_1, cls) and isinstance(particle_2, cls) and \
                (isinstance(particle_1, particle_2.__class__) or isinstance(particle_2, particle_1.__class__)):
            particle_1.add_neighbour(direction=direction, neighbour=particle_2, distance=distance)
            particle_2.add_neighbour(direction=Directions.get_opposite(direction=direction), neighbour=particle_1, distance=distance)
            return True
        return False
