#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević
import itertools

from .map_particles import MapParticles
from src.utils import ParticleContainer


def new_nodes(func):
    """Decorator that wraps function's result into a new Nodes object."""
    def wrapper(*args, **kwargs):
        nodes = Nodes()
        result = func(*args, **kwargs)
        nodes.add_nodes(*result)
        return nodes
    return wrapper


class Nodes(dict):
    """Nodes class."""

    def __init__(self):
        """
        Constructor.
        """
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

    def add_nodes(self, node, *args):
        """Adds multiple nodes in the node array."""
        for node_ in [node] + list(args):
            self.add_node(node=node_)

    def node_exists(self, node=None, i=None, j=None):
        """
        Checks if given node already exists.
        Node can be defined either as Node object, or simply with two coordinates.
        :param node: Node
        :param i: int
        :param j: int
        :return: bool
        """
        if i is not None and j is not None:
            return True if self.get_node(i=i, j=j) else False
        elif node and node.j in self.keys() and Nodes.is_node(node=node):
            return self[node.j].__contains__(particle=node)
        return False

    def get_node(self, i, j):
        """Returns the node with given i and j indexes."""
        if j in self.keys():
            for node in self[j]:
                if node.i == i:
                    return node
        return None

    def get_all(self):
        """Returns all nodes."""
        return itertools.chain(*self.values())

    @new_nodes
    def get_all_by_type(self, type_):
        """Returns all the nodes with given type."""
        for node in self.get_all():
            if node.type == type_:
                yield node

    @new_nodes
    def get_big_nodes(self):
        """Returns only big nodes."""
        for node in self.get_all():
            if isinstance(node, MapParticles.BigNode):
                yield node

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