#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


import os
from .directions import Directions


class PacmanConstant(object):
    """Pacman constants."""

    def __init__(self, value):
        """
        Constructor
        :param value: any type
        """
        self._value = value

    @property
    def value(self):
        """Getter."""
        return self._value


WIN_WIDTH = PacmanConstant(1000)    # px
WIN_HEIGHT = PacmanConstant(700)    # px
FPS_RATE = PacmanConstant(60)   # frames per seconds

MAPS_DIR = PacmanConstant(f"{os.getcwd()}\\assets\\maps\\testing")
MAP_NAMES = PacmanConstant([f"map_{i}" for i in range(1, 2)])
MAP_FILE_EXTENSION = PacmanConstant("mapfile")
MAP_FILE_ROW_DELIMITER = PacmanConstant(';')
MAP_FILE_DATA_DELIMITER = PacmanConstant('-')
MAP_NODE_SIZE = PacmanConstant(130)    # px
MAP_NEIGHBOURS_DIRECTIONS_VALUES = PacmanConstant([-1, -2, 1, 2])

DIRECTIONS_COORDINATES_DIFFERENCE = PacmanConstant({
    Directions.TOP: (0, -1),  # top
    Directions.RIGHT: (1, 0),  # right
    Directions.BOTTOM: (0, 1),  # bottom
    Directions.LEFT: (-1, 0)  # left
})
