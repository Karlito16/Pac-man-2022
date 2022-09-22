#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from __future__ import annotations

from src.map.components.elementary import MapParticles, Nodes, NodeType
import src.utils as utils


class Passages(dict):
    """Passages class."""

    class Passage(object):
        """Passage class."""

        def __init__(self, left_passage: MapParticles.BigNode, right_passage: MapParticles.BigNode):
            """Constructor."""
            self._left_passage = left_passage
            self._right_passage = right_passage
            self._left_bridge = self._create_bridge(i=self._left_passage.i - 2)
            self._right_bridge = self._create_bridge(i=self._right_passage.i + 2)

            for big_node_1, big_node_2, distance in (
                    (self._left_passage, self._left_bridge, 2),
                    (self._left_bridge, self._right_bridge, 1),
                    (self._right_bridge, self._right_passage, 2)
            ):
                MapParticles.BigNode.big_connect(
                    big_node_1=big_node_1,
                    big_node_2=big_node_2,
                    direction=utils.Directions.LEFT,
                    distance=distance
                )
                MapParticles.Node.connect(
                    particle_1=big_node_1,
                    particle_2=big_node_2,
                    direction=utils.Directions.LEFT,
                    distance=distance
                )

        def _create_bridge(self, i: int) -> MapParticles.Node:
            """Creates the bridge."""
            return MapParticles.BigNode(
                i=i,
                j=self._left_passage.j,
                size=self._left_passage.size,
                type_=NodeType.BRIDGE
            )

        @property
        def bridges(self):
            """getter."""
            return self._left_bridge, self._right_bridge

    def __init__(self, passage_nodes: Nodes, all_nodes: Nodes):
        """Constructor."""
        self._passage_nodes = passage_nodes
        super().__init__()

        for key in passage_nodes.keys():
            passages = passage_nodes[key]
            if len(passages) != 2:
                raise ValueError("Number of passages for one passage must be exclusively 2!")
            passage = Passages.Passage(*passages)
            self[key] = passage
            all_nodes.add_nodes(*passage.bridges)
