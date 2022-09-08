#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from enum import Enum, unique


@unique
class NodeType(Enum):
    """Node types."""

    EMPTY = 0
    REGULAR = 1
    SUPER = 2
    ENEMY_OUT = 3
    ENEMY_IN = 4
    GATE = 5
    PACMAN = 6
