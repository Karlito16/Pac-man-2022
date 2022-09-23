#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from .pacman_constant import PacmanConstant
import os


# DIRECTORIES
PROJECT_DIR = PacmanConstant(os.getcwd())
MAPS_DIR = PacmanConstant(f"{PROJECT_DIR.value}\\assets\\maps\\testing")
FOOD_DIR = PacmanConstant(f"{PROJECT_DIR.value}\\assets\\food")
CHARACHERS_DIR = PacmanConstant(f"{PROJECT_DIR.value}\\assets\\characters")
