#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević

from __future__ import annotations

from .grid_slot_type import GridSlotType
from .node_type import NodeType
import src.utils as utils


class MapParticles(object):
    """Map particles class container."""

    class Node(utils.Particle):
        """Node class."""

        def __init__(self, i: int, j: int, size: int, type_: NodeType, big_nodes: tuple[MapParticles.BigNode, MapParticles.BigNode] | None):
            """
            Cnstructor.
            """
            self._big_nodes = big_nodes
            super().__init__(i=i, j=j, size=size, type_=type_)
            self._grid_slots = utils.ParticleContainer(particle_instance=MapParticles.GridSlot)
            self._grid_slot_size = self.size / utils.MAP_GRID_SLOT_NODE_SIZE_RELATION.value

        @property
        def big_nodes(self) -> tuple[MapParticles.BigNode, MapParticles.BigNode] | None:
            """Getter."""
            return self._big_nodes

        @property
        def grid_slots(self) -> utils.ParticleContainer:
            """Getter."""
            return self._grid_slots

        @property
        def x(self) -> int:
            """Gets horizontal position in pixels."""
            return self.i * self._grid_slot_size

        @property
        def y(self) -> int:
            """Gets vertical position in pixels."""
            return self.j * self._grid_slot_size

        @property
        def pos_xy(self) -> tuple[int, int]:
            """Returns position in pixels."""
            return self.x, self.y

        def is_big_node(self) -> bool:
            """Returns if node is instance of MapParticles.BigNode."""
            return isinstance(self, MapParticles.BigNode)

        def check_for_possible_neighbours(self) -> list:
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

    class GridSlot(utils.Particle):
        """Grid slot class."""

        def __init__(self, i: int, j: int, size: int, type_: GridSlotType):
            """
            Constructor.
            """
            super().__init__(i=i, j=j, size=size, type_=type_)
            self._nodes = utils.ParticleContainer(particle_instance=MapParticles.Node)

        @property
        def nodes(self) -> utils.ParticleContainer:
            """Getter."""
            return self._nodes

        def is_wall(self) -> bool:
            """Getter."""
            return self.type == GridSlotType.WALL

        def is_path(self) -> bool:
            """Getter."""
            return self.type == GridSlotType.PATH

    class BigNode(Node):
        """BigNode class."""

        def __init__(self, i: int, j: int, size: int, type_: NodeType, *args, **kwargs):
            """
            Constructor.
            :param i:
            :param j:
            :param type_:
            """
            super().__init__(i=i, j=j, size=size, type_=type_, big_nodes=None)
            self._big_neighbours = utils.Neighbours()

        @property
        def big_neighbours(self) -> utils.Neighbours:
            """Getter."""
            return self._big_neighbours

        def add_big_neighbour(self, direction: utils.Directions, neighbour: MapParticles.Node, distance: float) -> bool:
            """Adds the big neighbour."""
            if self != neighbour and isinstance(neighbour, self.__class__):
                return self._big_neighbours.add_new(direction=direction, neighbour=neighbour, distance=distance)
            return False

        @classmethod
        def big_connect(cls, big_node_1: __class__, big_node_2: __class__, direction: utils.Directions = None, distance: float = None) -> bool:
            """Connects the two big nodes."""
            # TODO: implement this method with already existing connect method
            direction = direction if direction is not None else utils.Particle.get_direction(
                    particle1=big_node_1,
                    particle2=big_node_2
                )
            distance = distance if distance is not None else abs(big_node_1 - big_node_2)
            if isinstance(big_node_1, cls) and isinstance(big_node_2, cls):
                big_node_1.add_big_neighbour(direction=direction, neighbour=big_node_2, distance=distance)
                big_node_2.add_big_neighbour(direction=utils.Directions.get_opposite(direction=direction), neighbour=big_node_1, distance=distance)
                return True
            return False
