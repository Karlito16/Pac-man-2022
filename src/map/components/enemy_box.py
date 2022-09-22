#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.map.components.elementary import MapParticles, Nodes


class EnemyBox(list):
    """Enemy box class."""

    def __init__(self, enemy_in_nodes: Nodes):
        """
        Constructor
        """
        super().__init__(enemy_in_nodes.get_big_nodes())
        self._index = 0
        self._size = len(self)

    def get_next_room(self) -> MapParticles.Node:
        """Getter."""
        if self._index >= self._size:
            raise StopIteration()
        room = self[self._index]
        self._index += 1
        return room
