#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from .directory import MAPS_DIR
from .pacman_constant import PacmanConstant
import os


# MAP PARAMETERS
MAP_NAMES = PacmanConstant(os.listdir(MAPS_DIR.value))
# MAP_FILE_EXTENSION = PacmanConstant("mapfile")
MAP_FILE_ROW_DELIMITER = PacmanConstant(';')
MAP_FILE_DATA_DELIMITER = PacmanConstant('-')
MAP_GRID_SLOT_NODE_SIZE_RELATION = PacmanConstant(2)
MAP_NODE_SIZE = PacmanConstant(28)    # px
MAP_GRID_SLOT_SIZE = PacmanConstant(MAP_NODE_SIZE.value // MAP_GRID_SLOT_NODE_SIZE_RELATION.value)    # px
assert MAP_NODE_SIZE.value % MAP_GRID_SLOT_SIZE.value == 0, "map node size must be exactly 2 time bigger than grid slot size"
MAP_NEIGHBOURS_DIRECTIONS_VALUES = PacmanConstant([2, 1, -2, -1])
MAP_WALL_SIZE = PacmanConstant(5)   # keep this value odd!
MAP_WALL_INSIDE_COLOR = PacmanConstant("#0a0a0a")
MAP_WALL_BORDER_COLOR = PacmanConstant("#010759")
MAP_WALL_RADIUS = PacmanConstant(1)
MAP_MARGIN_TOP_PERCENTAGE = PacmanConstant(0.2)     # 20% of the total win height
MAP_MARGIN_BOTTOM_PERCENTAGE = PacmanConstant(0.1)     # 10% of the total win height
MAP_BACKGROUND_COLOR = PacmanConstant("Black")
