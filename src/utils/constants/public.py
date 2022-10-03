#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from .pacman_constant import PacmanConstant
from src.utils.directions import Directions


# ANIMATIONS PARAMETERS
MINIMAL_REQUIRED_ANIMATION_IMAGES = PacmanConstant(2)

# DIRECTIONS
DIRECTIONS_COORDINATES_DIFFERENCE = PacmanConstant({
    Directions.TOP: (0, -1),  # top
    Directions.RIGHT: (1, 0),  # right
    Directions.BOTTOM: (0, 1),  # bottom
    Directions.LEFT: (-1, 0),  # left
    Directions.UNDEFINED: (0, 0)
})

# OTHER
COLORS_ALPHA_MIN = PacmanConstant(255)
COLORS_ALPHA_MAX = PacmanConstant(0)
COLORS_PACMAN = PacmanConstant("FFD800")

RESUME_GAME_INTERVAL = PacmanConstant(2000)
ENDING_GAME_INTERVAL = PacmanConstant(3000)

FONT_STYLE = PacmanConstant("freesansbold.ttf")
