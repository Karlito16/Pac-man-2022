#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from .pacman_constant import PacmanConstant


# WINDOW AND SCREEN PARAMETERS
WIN_WIDTH = PacmanConstant(1000)    # px
WIN_HEIGHT = PacmanConstant(700)    # px
WIN_SIZE = PacmanConstant((WIN_WIDTH.value, WIN_HEIGHT.value))
FPS_RATE = PacmanConstant(60)   # frames per seconds

# SCREEN NAMES
GAME_SCREEN = PacmanConstant("app-screen")
MAIN_MENU_SCREEN = PacmanConstant("main-menu-screen")

# SCREEN PROPS
GAME_SCREEN_FONT_PERCENTAGE = PacmanConstant(0.6)
