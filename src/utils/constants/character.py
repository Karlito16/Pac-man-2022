#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from .pacman_constant import PacmanConstant
from src.utils.directions import Directions
import pygame


# CHARACTER
CHARACTER_RELEVANT_SIZE_PERCENTAGE = PacmanConstant(0.6)    # relative from node size
CHARACTER_DEFAULT_DIRECTION = PacmanConstant(Directions.LEFT)
CHARACTER_ANIMATION_ATTRIBUTE_BASE_NAME = PacmanConstant("_animation_images_")
CHARACTER_ANIMATION_IMAGES_ATTR_NAMES = PacmanConstant(
    dict(
        [(state, CHARACTER_ANIMATION_ATTRIBUTE_BASE_NAME.value + state) for state in ("top", "right", "bottom", "left", "death")]
    )
)
CHARACTER_MOVING_SPEED_PERCENTAGE = PacmanConstant(0.05)     # moves n% of node size by frame
CHARACTER_CHECKING_POSITION_AXES_THRESHOLD = PacmanConstant(0.025)
assert CHARACTER_MOVING_SPEED_PERCENTAGE.value > CHARACTER_CHECKING_POSITION_AXES_THRESHOLD.value,\
    "Checking position axes threshold percentage must be lower than moving speed percentage!"
CHARACTER_MOVING_ANIMATION_SPEED = PacmanConstant(0.2)
CHARACTER_MOVING_KEYS = PacmanConstant([pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT])
CHARACTER_LOOK_FOR_BIG_NODE_TRESHOLD = PacmanConstant(2)   # must be maximum n nodes distanced from the big node in order to apply direction change
CHARACTER_ENEMY_NAMES = PacmanConstant(["Name1", "Name2", "Name3", "Name4"])
CHARACTER_NUM_OF_ENEMIES = PacmanConstant(len(CHARACTER_ENEMY_NAMES.value))
CHARACTER_ENEMY_START_MOVING_INTERVAL = PacmanConstant(2000)    # miliseconds
