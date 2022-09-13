#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from __future__ import annotations

from .grid_slot_type import GridSlotType
from .map_particles import MapParticles
from .node_type import NodeType
from .nodes import Nodes
import src.utils as utils

import itertools
from typing import Callable, Generator


class Grid(dict):
    """Grid class."""

    GRID_SLOTS_NODE_RELATIVE_POSITIONS = [(0, 0), (0, -1), (-1, 0), (-1, -1)]

    def __init__(self, size: tuple[int, int]):
        """
        Constructor.
        """
        self._size = size
        self._cols, self._rows = self._size
        *self._size_pixels, self._grid_slot_size = utils.calculate_grid_dimensions(grid_size=self._size)
        super().__init__()
        self._enable_editing = True
        self._init_grid()
        self._enable_editing = False
        self._init_neighbours()
        self._nodes = Nodes()

    def __setitem__(self, key: int, value: utils.ParticleContainer) -> None:
        """Disables any changes to the original grid."""
        if not self._enable_editing:
            raise PermissionError(f"you do not have permission to edit this object {self}")
        else:
            super().__setitem__(key, value)
            return None

    @property
    def size(self) -> tuple[int, int]:
        """Getter."""
        return self._size

    @property
    def rows(self) -> int:
        """Getter."""
        return self._rows

    @property
    def cols(self) -> int:
        """Getter."""
        return self._cols

    @property
    def full_size(self) -> tuple[int, int]:
        """Getter."""
        return self._size_pixels

    @property
    def grid_slot_size(self) -> int:
        """Getter."""
        return self._grid_slot_size

    @property
    def nodes(self) -> Nodes:
        """Getter."""
        return self._nodes

    def _init_grid(self) -> None:
        """Creates the grid with the grid slots."""
        for row in range(self.rows):
            row_container = utils.ParticleContainer(particle_instance=MapParticles.GridSlot)
            for col in range(self.cols):
                row_container.add(MapParticles.GridSlot(i=col, j=row, size=self._grid_slot_size, type_=GridSlotType.WALL))
            self[row] = row_container
        return None

    def _init_neighbours(self) -> None:
        """Sets the grids slot's neighbours."""
        for grid_slot in self.get_all():
            # try all 4 directions
            for direction, (i, j) in utils.DIRECTIONS_COORDINATES_DIFFERENCE.value.items():
                grid_slot.add_neighbour(
                    neighbour=self.get_grid_slot(i=grid_slot.i + i, j=grid_slot.j + j),
                    direction=direction
                )
        return None

    def get_all(self) -> Generator[MapParticles.GridSlot, ]:
        """Returns all grid slots."""
        for grid_slot in itertools.chain(*self.values()):
            yield grid_slot

    def get_all_walls(self) -> Generator[MapParticles.GridSlot]:
        """Returns a list with all grid slotss that remained walls."""
        for grid_slot in self.get_all():
            if grid_slot.type == GridSlotType.WALL:
                yield grid_slot

    def get_grid_slot(self, i: int, j: int) -> MapParticles.GridSlot | None:
        """Returns the grid slot at (i, j) position."""
        if i in range(0, self.cols) and j in range(0, self.rows):
            return self[j][i]
        return None

    def define_grid_slots_for_node(self, node: MapParticles.Node) -> bool:
        """Method defines 4 grid slots that together creates one node."""
        if isinstance(node, MapParticles.Node):
            for relative_i, relative_j in Grid.GRID_SLOTS_NODE_RELATIVE_POSITIONS:
                grid_slot = self.get_grid_slot(i=node.i + relative_i, j=node.j + relative_j)
                if grid_slot:
                    grid_slot.type = GridSlotType.PATH
                    grid_slot.nodes.add(node)  # specific grid slot is part of the one node
                    node.grid_slots.add(grid_slot)  # one of the four grid slots becomes a part of the one node
            return True
        return False

    def _create_node(self, i: int, j: int, type_: NodeType, class_: Callable) -> MapParticles.Node | MapParticles.BigNode:
        """Wrapper method for creating a node/big node."""
        node = self._nodes.get_node(i=i, j=j)
        if not node:
            node = class_(i=i, j=j, size=utils.MAP_GRID_SLOT_NODE_SIZE_RELATION.value * self._grid_slot_size, type_=type_)
            self.define_grid_slots_for_node(node=node)
            self._nodes.add_node(node=node)
        return node

    def create_node(self, i: int, j: int, type_: NodeType) -> MapParticles.Node:
        """Converts grid slots into a node."""
        return self._create_node(i=i, j=j, type_=type_, class_=MapParticles.Node)

    def create_big_node(self, i: int, j: int, type_: NodeType) -> MapParticles.BigNode:
        """Converts grid slots into a big node."""
        return self._create_node(i=i, j=j, type_=type_, class_=MapParticles.BigNode)

    @staticmethod
    def _get_sub_nodes_type(from_node_type: NodeType, to_node_type: NodeType) -> NodeType:
        """Gets the appropriate type for sub nodes that are between two given big nodes."""
        types = (from_node_type.value, to_node_type.value)
        if from_node_type == NodeType.EMPTY or to_node_type == NodeType.EMPTY or NodeType.PACMAN.value in types:
            type_ = NodeType.EMPTY
        elif (NodeType.REGULAR.value in types and NodeType.EMPTY.value not in types) or \
                (from_node_type == NodeType.SUPER and to_node_type == NodeType.SUPER):
            type_ = NodeType.REGULAR
        elif from_node_type == NodeType.ENEMY_IN and to_node_type == NodeType.ENEMY_IN:
            type_ = NodeType.ENEMY_IN
        elif NodeType.GATE.value in types and \
                (NodeType.ENEMY_OUT.value in types or NodeType.ENEMY_IN.value in types or NodeType.PACMAN.value in types):
            type_ = NodeType.GATE
        else:
            raise TypeError(f"invalid type range: {from_node_type} - {to_node_type}")
        return type_

    def create_sub_nodes(self, from_node: MapParticles.BigNode, to_node: MapParticles.BigNode, direction: utils.Directions = None) -> Generator[MapParticles.Node] | None:
        """Creates sub nodes between two big nodes, with appropriate node type."""
        direction = direction if direction is not None else MapParticles.Node.get_direction(
            particle1=from_node,
            particle2=to_node
        )
        if direction != utils.Directions.UNDEFINED and \
                isinstance(from_node, MapParticles.BigNode) and \
                isinstance(to_node, MapParticles.BigNode):

            diff_i, diff_j = utils.DIRECTIONS_COORDINATES_DIFFERENCE.value[direction]
            start_i, start_j = from_node.pos
            n = int(from_node - to_node) - 1  # number of sub nodes which will be created
            sub_nodes_type = Grid._get_sub_nodes_type(from_node_type=from_node.type, to_node_type=to_node.type)

            for node_index in range(1, n + 1):
                node = self.create_node(
                    i=start_i + node_index * diff_i,
                    j=start_j + node_index * diff_j,
                    type_=sub_nodes_type
                )
                yield node
        return None
