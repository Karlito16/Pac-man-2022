#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from enum import Enum, auto, unique


@unique
class GridSlotType(Enum):
    """Grid slot types."""

    PATH = auto()
    WALL = auto()
