#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from .pacman_constant import PacmanConstant


# FOOD
FOOD_FLASH_ANIMATION_RANDOM_START_RANGE = PacmanConstant([0, 1000])   # miliseconds
FOOD_FLASH_ANIMATION_INTERVAL = PacmanConstant(250)    # miliseconds
FOOD_FLASH_ANIMATION_SPEED = PacmanConstant(0.1)
FOOD_PERCENTAGE_OF_FLASHING_OBJECTS_AT_ONCE = PacmanConstant(0.05)   # 50% randomly selected food object will do flash at one animation cycle
FOOD_COLLECTING_ANIMATION_MAX_SIZE_PERCENTAGE = PacmanConstant(1.5)
FOOD_COLLECTING_ANIMATION_SPEED = PacmanConstant(0.075)
FOOD_FADE_ANIMATION_SPEED = PacmanConstant(6)
FOOD_COIN_RELEVANT_SIZE_PERCENTAGE = PacmanConstant(0.15)     # relative from node size
FOOD_SUPER_COIN_RELEVANT_SIZE_PERCENTAGE = PacmanConstant(0.25)      # relative from node size
FOOD_CHERRY_RELEVANT_SIZE_PERCENTAGE = PacmanConstant(0.3)      # relative from node size
FOOD_COLLECT_FOOD_CALLBACK_ATTR_NAME = PacmanConstant("collect_food")
