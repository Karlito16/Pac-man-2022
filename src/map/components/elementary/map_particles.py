#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from src.utils import Directions, Particle, ParticleContainer, Neighbours, MAP_GRID_SLOT_NODE_SIZE_RELATION


class MapParticles:
    """Map particles class container."""

    class Node(Particle):
        """Node class."""

        def __init__(self, i, j, size, type_):
            """
            Cnstructor.
            """
            super().__init__(i=i, j=j, size=size, type_=type_)
            self._grid_slots = ParticleContainer(particle_instance=MapParticles.GridSlot)
            self._grid_slot_size = self.size / MAP_GRID_SLOT_NODE_SIZE_RELATION.value

        @property
        def grid_slots(self):
            """Getter."""
            return self._grid_slots

        @property
        def x(self):
            """Gets horizontal position in pixels."""
            return self.i * self._grid_slot_size

        @property
        def y(self):
            """Gets vertical position in pixels."""
            return self.j * self._grid_slot_size

        @property
        def pos_xy(self):
            """Returns position in pixels."""
            return self.x, self.y

        def check_for_possible_neighbours(self):
            """Node itself checks for all of the four possible neighbours."""
            possible_neighbours = dict()
            for grid_slot in self.grid_slots:
                grid_slot_other_nodes = grid_slot.nodes
                grid_slot_other_nodes.remove(self)
                for node in grid_slot_other_nodes:
                    if node in possible_neighbours.keys():
                        possible_neighbours[node] += 1
                    else:
                        possible_neighbours[node] = 1
            # two nodes are neighbours if they share two and only two grid slots
            neighbours = [node for node in possible_neighbours if possible_neighbours[node] == 2]
            return neighbours

    class GridSlot(Particle):
        """Grid slot class."""

        def __init__(self, i, j, size, type_):
            """
            Constructor.
            """
            super().__init__(i=i, j=j, size=size, type_=type_)
            self._nodes = ParticleContainer(particle_instance=MapParticles.Node)

        @property
        def nodes(self):
            """Getter."""
            return self._nodes

    class BigNode(Node):
        """BigNode class."""

        def __init__(self, i, j, size, type_):
            """
            Constructor.
            :param i:
            :param j:
            :param type_:
            """
            super().__init__(i=i, j=j, size=size, type_=type_)
            self._big_neighbours = Neighbours()

        @property
        def big_neighbours(self):
            """Getter."""
            return self._big_neighbours

        def add_big_neighbour(self, direction, neighbour):
            """Adds the big neighbour."""
            if self != neighbour and isinstance(neighbour, self.__class__):
                return self._big_neighbours.add_new(direction=direction, neighbour=neighbour)
            return False

        @classmethod
        def big_connect(cls, big_node_1, big_node_2, direction=None):   # TODO: implement this method with already existing connect method
            """Connects the two big nodes."""
            direction = direction if direction is not None else Particle.get_direction(
                    particle1=big_node_1,
                    particle2=big_node_2
                )
            if isinstance(big_node_1, cls) and isinstance(big_node_2, cls):
                big_node_1.add_big_neighbour(direction=direction, neighbour=big_node_2)
                big_node_2.add_big_neighbour(direction=Directions.get_opposite(direction=direction), neighbour=big_node_1)
                return True
            return False
