#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from .pacman_constant import PacmanConstant
from src.utils.directions import Directions
import pygame


# CHARACTER
CHARACTER_PACMAN_NAME = PacmanConstant("Pacman")
CHARACTER_ENEMY_NAMES = PacmanConstant({
    "Blinky": (255, 0, 0, 0),
    "Pinky": (72, 0, 255, 0),
    "Inky": (255, 216, 0, 0),
    "Clyde": (0, 255, 144, 0)
})
CHARACTER_NAME_FOLDER_NAME_RELATION = PacmanConstant(
    dict(
        [
            (ch_name, folder_name) for ch_name, folder_name in zip(
                [CHARACTER_PACMAN_NAME.value] + [key for key in CHARACTER_ENEMY_NAMES.value],
                ["pacman"] + [f"enemy_{i + 1}" for i in range(len(CHARACTER_ENEMY_NAMES.value.keys()))]
            )
        ]
    )
)
CHARACTER_BODY_ASSETS_ATTR_NAME = PacmanConstant("character_body_assets")
CHARACTER_RELEVANT_SIZE_PERCENTAGE = PacmanConstant(0.6)    # relative from node size
CHARACTER_DEFAULT_DIRECTION = PacmanConstant(Directions.LEFT)
CHARACTER_DEATH_KEYWORD = PacmanConstant("death")
CHARACTER_ANIMATION_ATTRIBUTE_BASE_NAME = PacmanConstant("_animation_images_")
CHARACTER_ANIMATION_IMAGES_ATTR_NAMES = PacmanConstant(
    dict(
        [(state, CHARACTER_ANIMATION_ATTRIBUTE_BASE_NAME.value + state) for state in ("top", "right", "bottom", "left", CHARACTER_DEATH_KEYWORD.value)]
    )
)
CHARACTER_PACMAN_MOVING_SPEED_PERCENTAGE = PacmanConstant(0.05)     # moves n% of node size by frame
CHARACTER_ENEMY_MOVING_SPEED_PERCENTAGE = PacmanConstant(0.054)     # moves n% of node size by frame
CHARACTER_ENEMY_AS_FOOD_MOVING_SPEED_PERCENTAGE = PacmanConstant(0.0251)     # moves n% of node size by frame
CHARACTER_ENEMY_RUNNING_MOVING_SPEED_PERCENTAGE = PacmanConstant(0.054)     # moves n% of node size by frame
CHARACTER_CHECKING_POSITION_AXES_THRESHOLD = PacmanConstant(0.06)
# assert min(
#     CHARACTER_PACMAN_MOVING_SPEED_PERCENTAGE.value,
#     CHARACTER_ENEMY_MOVING_SPEED_PERCENTAGE.value,
#     CHARACTER_ENEMY_AS_FOOD_MOVING_SPEED_PERCENTAGE.value
# ) > CHARACTER_CHECKING_POSITION_AXES_THRESHOLD.value, "Checking position axes threshold percentage must be lower than moving speed percentage!"
CHARACTER_MOVING_ANIMATION_SPEED = PacmanConstant(0.2)
CHARACTER_MOVING_KEYS = PacmanConstant([pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT])
CHARACTER_LOOK_FOR_BIG_NODE_TRESHOLD = PacmanConstant(2)   # must be maximum n nodes distanced from the big node in order to apply direction change
CHARACTER_NUM_OF_ENEMIES = PacmanConstant(len(CHARACTER_ENEMY_NAMES.value))
CHARACTER_ENEMY_START_MOVING_INTERVAL = PacmanConstant(2000)    # miliseconds
CHARACTER_DEATH_GAME_PAUSE_INTERVAL = PacmanConstant(1000)  # miliseconds
CHARACTER_PACMAN_LIVES = PacmanConstant(3)
CHARACTER_PACMAN_BOOST_MAIN_INTERVAL = PacmanConstant(8000)     # miliseconds
CHARACTER_PACMAN_BOOST_ENDING_INTERVAL = PacmanConstant(2000)   # miliseconds
CHARACTER_ENEMY_DEATH_PAUSE_INTERVAL = PacmanConstant(1000)     # miliseconds
CHARACTER_ENEMY_SCORE = PacmanConstant(200)
CHARACTER_DEATH_COLOR = PacmanConstant((33, 0, 127, 0))
