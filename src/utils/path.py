#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from __future__ import annotations
from src.map.components.elementary import MapParticles
from typing import Iterable, TypeVar, TYPE_CHECKING
import copy
if TYPE_CHECKING:
    from src.map.components.elementary import MapParticles


class Path(object):
    """Path class."""

    NODE_T = TypeVar("NODE_T", bound=MapParticles.Node)
    INFINITY = float('inf')
    _distances = dict()
    _nodes = list()

    @classmethod
    def init_nodes(cls, nodes: Iterable[NODE_T]) -> None:
        """inits the graph."""
        for node in nodes:
            cls._nodes.append(copy.copy(node))
        return None

    @classmethod
    def _add_node_as_big_node(cls, node: MapParticles.Node, nodes: list[NODE_T]) -> MapParticles.BigNode:
        """Add."""
        node_big = MapParticles.BigNode(i=node.i, j=node.j, size=node.size, type_=node.type)
        for big_node in node.big_nodes:
            big_node_cpy = copy.copy(nodes.pop(nodes.index(big_node)))
            MapParticles.BigNode.big_connect(big_node_1=big_node_cpy, big_node_2=node_big)
            nodes.append(big_node_cpy)
        nodes.append(node_big)
        return node_big

    @classmethod
    def _setup_nodes(cls, from_node: NODE_T, to_node: NODE_T) -> tuple[NODE_T, NODE_T, list[NODE_T]]:
        """Setups the nodes for algorithm."""
        nodes = cls._nodes.copy()
        node_copies = {from_node: from_node, to_node: to_node}
        num_of_nodes = 0
        for node in (from_node, to_node):
            if not isinstance(node, MapParticles.BigNode):
                num_of_nodes += 1
                node_copies[node] = cls._add_node_as_big_node(node=node, nodes=nodes)
        if num_of_nodes == 2:
            if len(set(from_node.big_nodes).intersection(set(to_node.big_nodes))) == 2:
                return from_node, to_node, []
        return node_copies[from_node], node_copies[to_node], nodes

    @classmethod
    def _init_distances(cls, nodes: list[MapParticles.BigNode]) -> None:
        """inits the distances."""
        for node in nodes:
            cls._distances[node] = (cls.INFINITY, None)
        return None

    @classmethod
    def find_shortest(cls, from_node: NODE_T, to_node: NODE_T) -> list[MapParticles.BigNode]:
        """Dijkstra algorithm: finds the shortest path from from_node to to_node."""
        from_node_cpy, to_node_cpy, nodes = cls._setup_nodes(from_node=from_node, to_node=to_node)
        if not nodes:   # case when both nodes are within same "neighbourhood"
            return []

        cls._init_distances(nodes=nodes)
        cls._distances[from_node_cpy] = (0, None)

        visited_nodes = set()
        new_visited_node = from_node_cpy
        found_neighbours = set()
        while True:
            visited_nodes.add(new_visited_node)

            for neighbour in new_visited_node.big_neighbours.get_all_with_distance():
                if neighbour and neighbour.node not in visited_nodes:
                    old_distance = cls._distances[neighbour.node][0]
                    new_distance = cls._distances[new_visited_node][0] + neighbour.distance
                    distance = new_distance if new_distance < old_distance else old_distance
                    cls._distances[neighbour.node] = (
                        distance,
                        new_visited_node
                    )
                    neighbour_cpy = copy.copy(neighbour)
                    neighbour_cpy.distance = distance
                    found_neighbours.add(neighbour_cpy)

            if not found_neighbours and to_node_cpy in visited_nodes:
                break

            new_visited_node = min(found_neighbours)
            found_neighbours.remove(new_visited_node)
            new_visited_node = new_visited_node.node

        # for node in cls._distances:
        #     print(f"Node: {node}, Distance: {cls._distances[node][0]}, Via: {cls._distances[node][1]}")

        path = list()
        path.append(to_node)
        previous_node = cls._distances[to_node_cpy][1]
        while previous_node:
            path.insert(0, previous_node)
            previous_node = cls._distances[previous_node][1]
        path.pop(0)
        path.insert(0, from_node)
        return path
