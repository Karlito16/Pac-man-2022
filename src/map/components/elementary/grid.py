#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


import itertools
from .grid_slot_type import GridSlotType
from .map_particles import MapParticles
from .node_type import NodeType
from src.utils import Directions, ParticleContainer, DIRECTIONS_COORDINATES_DIFFERENCE


class Grid(dict):
    """Grid class."""

    GRID_SLOTS_NODE_RELATIVE_POSITIONS = [(0, 0), (0, -1), (-1, 0), (-1, -1)]

    def __init__(self, size):
        """
        Constructor.
        """
        self._size = size
        self._cols, self._rows = self._size
        super().__init__()
        self._enable_editing = True
        self._init_grid()
        self._enable_editing = False
        self._init_neighbours()

    def __setitem__(self, key, value):
        """Disables any changes to the original grid."""
        if not self._enable_editing:
            raise PermissionError(f"you do not have permission to edit this object {self}")
        else:
            super().__setitem__(key, value)

    @property
    def size(self):
        """Getter."""
        return self._size

    @property
    def rows(self):
        """Getter."""
        return self._rows

    @property
    def cols(self):
        """Getter."""
        return self._cols

    def _init_grid(self):
        """Creates the grid with the grid slots."""
        for row in range(self.rows):
            row_container = ParticleContainer(particle_instance=MapParticles.GridSlot)
            for col in range(self.cols):
                row_container.add(MapParticles.GridSlot(i=col, j=row, type_=GridSlotType.WALL))
            self[row] = row_container
        return

    def _init_neighbours(self):
        """Sets the grids slot's neighbours."""
        for grid_slot in self.get_all():
            # try all 4 directions
            for direction, (i, j) in DIRECTIONS_COORDINATES_DIFFERENCE.value.items():
                grid_slot.add_neighbour(
                    neighbour=self.get_grid_slot(i=grid_slot.i + i, j=grid_slot.j + j),
                    direction=direction
                )
        return

    def get_all(self):
        """Returns all grid slots."""
        for grid_slot in itertools.chain(*self.values()):
            yield grid_slot

    def get_grid_slot(self, i, j):
        """Returns the grid slot at (i, j) position."""
        if i in range(0, self.cols) and j in range(0, self.rows):
            return self[j][i]
        return

    def define_grid_slots_for_node(self, node):
        """Method defines 4 grid slots that together creates one node."""
        if isinstance(node, MapParticles.Node):
            for relative_i, relative_j in Grid.GRID_SLOTS_NODE_RELATIVE_POSITIONS:
                grid_slot = self.get_grid_slot(i=node.i + relative_i, j=node.j + relative_j)
                if grid_slot:
                    grid_slot.type = GridSlotType.PATH
                    grid_slot.nodes.add(node)  # specific grid slot is part of the one node
                    node.grid_slots.add(grid_slot)  # one of the four grid slots becomes a part of the one node
        return

    def create_node(self, i, j, type_):
        """Converts grid slots into a node."""
        node = MapParticles.Node(i=i, j=j, type_=type_)
        self.define_grid_slots_for_node(node=node)
        return node

    def create_big_node(self, i, j, type_):
        """Converts grid slots into a big node."""
        big_node = MapParticles.BigNode(i=i, j=j, type_=type_)
        self.define_grid_slots_for_node(node=big_node)
        return big_node

    @staticmethod
    def _get_sub_nodes_type(from_node_type, to_node_type):
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
                (
                        NodeType.ENEMY_OUT.value in types or NodeType.ENEMY_IN.value in types or NodeType.PACMAN.value in types):
            type_ = NodeType.GATE
        else:
            raise TypeError(f"invalid type rande: {from_node_type} - {to_node_type}")
        return type_

    def create_sub_nodes(self, from_node, to_node, direction=None):
        """Creates sub nodes between two big nodes, with appropriate node type."""
        direction = direction if direction is not None else MapParticles.Node.get_direction(
            particle1=from_node,
            particle2=to_node
        )
        if direction != Directions.UNDEFINED and \
                isinstance(from_node, MapParticles.BigNode) and \
                isinstance(to_node, MapParticles.BigNode):

            diff_i, diff_j = DIRECTIONS_COORDINATES_DIFFERENCE.value[direction]
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

    def get_all_walls(self):
        """Returns a list with all grid slotss that remained walls."""
        for grid_slot in self.get_all():
            if grid_slot.type == GridSlotType.WALL:
                yield grid_slot
