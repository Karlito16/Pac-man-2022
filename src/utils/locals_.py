#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from .directions import Directions
from typing import Any
import os
import pygame


class PacmanConstant(object):
    """Pacman constants."""

    def __init__(self, value: Any):
        """
        Constructor
        :param value: any type
        """
        self._value = value

    @property
    def value(self) -> Any:
        """Getter."""
        return self._value


# WINDOW AND SCREEN PARAMETERS
WIN_WIDTH = PacmanConstant(1000)    # px
WIN_HEIGHT = PacmanConstant(700)    # px
FPS_RATE = PacmanConstant(60)   # frames per seconds

# DIRECTORIES
PROJECT_DIR = PacmanConstant(os.getcwd())
MAPS_DIR = PacmanConstant(f"{PROJECT_DIR.value}\\assets\\maps\\testing")
FOOD_DIR = PacmanConstant(f"{PROJECT_DIR.value}\\assets\\food")
CHARACHERS_DIR = PacmanConstant(f"{PROJECT_DIR.value}\\assets\\characters")

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
MAP_WALL_SIZE = PacmanConstant(9)   # keep this value odd!
MAP_WALL_COLOR = PacmanConstant("#010759")
MAP_WALL_RADIUS = PacmanConstant(1)
MAP_MARGIN_TOP_PERCENTAGE = PacmanConstant(0.2)     # 20% of the total win height
MAP_MARGIN_BOTTOM_PERCENTAGE = PacmanConstant(0.1)     # 10% of the total win height
MAP_BACKGROUND_COLOR = PacmanConstant("Black")

# DIRECTIONS
DIRECTIONS_COORDINATES_DIFFERENCE = PacmanConstant({
    Directions.TOP: (0, -1),  # top
    Directions.RIGHT: (1, 0),  # right
    Directions.BOTTOM: (0, 1),  # bottom
    Directions.LEFT: (-1, 0),  # left
    Directions.UNDEFINED: (0, 0)
})

# ANIMATIONS PARAMETERS
MINIMAL_REQUIRED_ANIMATION_IMAGES = PacmanConstant(2)

# FOOD
FOOD_FLASH_ANIMATION_RANDOM_START_RANGE = PacmanConstant([0, 1000])   # miliseconds
FOOD_FLASH_ANIMATION_INTERVAL = PacmanConstant(100)    # miliseconds
FOOD_FLASH_ANIMATION_SPEED = PacmanConstant(0.2)
FOOD_PERCENTAGE_OF_FLASHING_OBJECTS_AT_ONCE = PacmanConstant(0.50)   # 50% randomly selected food object will do flash at one animation cycle
FOOD_COLLECTING_ANIMATION_MAX_SIZE_PERCENTAGE = PacmanConstant(1.5)
FOOD_COLLECTING_ANIMATION_SPEED = PacmanConstant(0.075)
FOOD_FADE_ANIMATION_SPEED = PacmanConstant(6)
FOOD_COIN_RELEVANT_SIZE_PERCENTAGE = PacmanConstant(0.15)     # relative from node size
FOOD_SUPER_COIN_RELEVANT_SIZE_PERCENTAGE = PacmanConstant(0.25)      # relative from node size
FOOD_CHERRY_RELEVANT_SIZE_PERCENTAGE = PacmanConstant(0.3)      # relative from node size
FOOD_COLLECT_FOOD_CALLBACK_ATTR_NAME = PacmanConstant("collect_food")

# CHARACTERS
CHARACTER_RELEVANT_SIZE_PERCENTAGE = PacmanConstant(0.6)    # relative from node size
CHARACTER_DEFAULT_DIRECTION = PacmanConstant(Directions.LEFT)
CHARACTER_ANIMATION_ATTRIBUTE_BASE_NAME = PacmanConstant("_animation_images_")
CHARACTER_MOVING_SPEED_PERCENTAGE = PacmanConstant(0.05)     # moves n% of node size by frame
CHARACTER_CHECKING_POSITION_AXES_THRESHOLD = PacmanConstant(0.025)
assert CHARACTER_MOVING_SPEED_PERCENTAGE.value > CHARACTER_CHECKING_POSITION_AXES_THRESHOLD.value,\
    "Checking position axes threshold percentage must be lower than moving speed percentage!"
CHARACTER_MOVING_ANIMATION_SPEED = PacmanConstant(0.2)
CHARACTER_MOVING_KEYS = PacmanConstant([pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT])
CHARACTER_LOOK_FOR_BIG_NODE_TRESHOLD = PacmanConstant(3)   # must be maximum 4 nodes distanced from the big node in order to apply direction change

# OTHER
COLORS_ALPHA_MIN = PacmanConstant(255)
COLORS_ALPHA_MAX = PacmanConstant(0)
