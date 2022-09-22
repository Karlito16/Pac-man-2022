#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from enum import Enum, unique


@unique
class EnemyType(Enum):
    """Enemy type."""

    SHADOW = "Blinky"   # follows the pacman
    SPEEDY = "Pinky"    # stops in front of the pacman
    BASHFUL = "Inky"    # stops in front of the pacman
    POKEY = "Clyde"     # random
