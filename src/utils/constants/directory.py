#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from .pacman_constant import PacmanConstant
import os


# DIRECTORIES
PROJECT_DIR = PacmanConstant(os.getcwd())
MAPS_DIR = PacmanConstant(f"{PROJECT_DIR.value}\\assets\\maps\\testing")
FOOD_DIR = PacmanConstant(f"{PROJECT_DIR.value}\\assets\\food")
CHARACTERS_DIR = PacmanConstant(f"{PROJECT_DIR.value}\\assets\\characters")
CHARACTERS_PACMAN_DIR = PacmanConstant(f"{CHARACTERS_DIR.value}\\pacman")
CHARACTERS_PACMAN_BODY_DIR = PacmanConstant(f"{CHARACTERS_PACMAN_DIR.value}\\moving")
CHARACTERS_PACMAN_DEATH_DIR = PacmanConstant(f"{CHARACTERS_PACMAN_DIR.value}\\death")
CHARACTERS_ENEMY_BODY_DIR = PacmanConstant(f"{CHARACTERS_DIR.value}\\enemy\\260\\body")
CHARACTERS_ENEMY_EYES_DIR = PacmanConstant(f"{CHARACTERS_DIR.value}\\enemy\\260\\eyes")
