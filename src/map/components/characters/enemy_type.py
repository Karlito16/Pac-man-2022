#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from enum import Enum, unique
import src.utils as utils


ENEMIES_NAMES = [name for name in utils.CHARACTER_ENEMY_NAMES.value]


@unique
class EnemyType(Enum):
    """Enemy type."""

    SHADOW = ENEMIES_NAMES[0]   # follows the pacman
    SPEEDY = ENEMIES_NAMES[1]    # stops in front of the pacman
    BASHFUL = ENEMIES_NAMES[2]    # stops in front of the pacman
    POKEY = ENEMIES_NAMES[3]     # random
