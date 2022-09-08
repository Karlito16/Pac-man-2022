#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from .map_particles import MapParticles
from src.utils import ParticleContainer


class Nodes(dict):
    """Nodes class."""

    def __init__(self):
        """
        Constructor.
        """
        # super().__init__(particle_instance=MapParticles.Node)
        super().__init__()

    @staticmethod
    def is_node(node):
        """Checks if given parameter is a Nodes.Node class instance."""
        return isinstance(node, MapParticles.Node)

    def add_node(self, node):
        """Adds the node."""
        if node.j not in self.keys():
            self[node.j] = ParticleContainer(particle_instance=MapParticles.Node)
        self[node.j].add(node)

        # return super().add(node)

    def add_nodes(self, node, *args):
        """Adds multiple nodes in the node array."""
        for node_ in [node] + list(args):
            self.add_node(node=node_)
        # return super().add(node, *args)

    def node_exists(self, node):
        """Checks if given node already exists."""
        if node.j in self.keys() and Nodes.is_node(node=node):
            return self[node.j].__contains__(particle=node)
        return False

    def get_node(self, i, j):
        """Returns the node with given i and j indexes."""
        if j in self.keys():
            for node in self[j]:
                if node.i == i:
                    return node
        return None

    @staticmethod
    def neighbourhood(*args, direction=None):
        """
        Creates the 'neighbourhood' between the given nodes.
        Two nodes that are next to the each other becomes a neighbours.
        """
        num_of_nodes = len(args)
        if num_of_nodes < 2:
            return False

        for node_index in range(num_of_nodes - 1):
            MapParticles.Node.connect(
                particle_1=args[node_index],
                particle_2=args[node_index + 1],
                direction_1_2=direction
            )
        return True
