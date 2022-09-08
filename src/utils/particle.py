#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević

import math
from .neighbours import Neighbours
from .directions import Directions


class Particle(object):
    """Particle class."""

    def __init__(self, i, j, type_):
        """
        Constructor.
        :param i:
        :param j:
        :param type_:
        """
        self._i = i
        self._j = j
        self._type = type_
        self._neighbours = Neighbours()

    def __str__(self):
        """To string method."""
        output = f"""{str(self.__class__).split('.')[-1].strip("'>")}(i={self.i},j={self.j},type={self.type})"""
        return output

    def __repr__(self):
        """How the class object should be displayed."""
        return self.__str__()

    def __eq__(self, other):
        """Checks if two particles are equal."""
        if isinstance(other, self.__class__):
            return self.i == other.i and self.j == other.j
        return False

    def __hash__(self):
        """Hashable type method."""
        return f"{self.i}{self.j}".__hash__()

    def __sub__(self, other):
        """Returns the distance between two particles."""
        if isinstance(self, Particle) and isinstance(other, Particle):
            return math.sqrt(math.pow(self.i - other.i, 2) + math.pow(self.j - other.j, 2))
        return None

    def __del__(self):
        """Destructor method."""
        del self._i
        del self._j
        del self._type
        del self._neighbours

    @property
    def i(self):
        """Getter."""
        return self._i

    @property
    def j(self):
        """Getter."""
        return self._j

    @property
    def pos(self):
        """Returns the (i,j) position."""
        return self.i, self.j

    @property
    def type(self):
        """Getter."""
        return self._type

    @type.setter
    def type(self, value):
        """Setter."""
        if isinstance(value, self._type.__class__):
            self._type = value

    @property
    def neighbours(self):
        """Getter."""
        return self._neighbours

    def add_neighbour(self, neighbour, direction=None):
        """Syntatic sugar method."""
        if isinstance(neighbour, Particle):
            direction = Particle.get_direction(particle1=self, particle2=neighbour) if direction is None else direction
            return self._neighbours.add_new(direction=direction, neighbour=neighbour)

    @classmethod
    def get_direction(cls, particle1, particle2):
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
    def connect(cls, particle_1, particle_2, direction_1_2=None):
        """Connects the two particles."""
        direction_1_2 = direction_1_2 if direction_1_2 is not None else Particle.get_direction(
            particle1=particle_1,
            particle2=particle_2
        )
        if isinstance(particle_1, cls) and isinstance(particle_2, cls) and \
                (isinstance(particle_1, particle_2.__class__) or isinstance(particle_2, particle_1.__class__)):
            particle_1.add_neighbour(direction=direction_1_2, neighbour=particle_2)
            particle_2.add_neighbour(direction=Directions.get_opposite(direction=direction_1_2), neighbour=particle_1)
            return True
        return False
