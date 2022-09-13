#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević

from .character import Character
from .character_type import CharacterType
import src.utils as utils


class Pacman(Character):
    """Pacman class."""

    def __init__(self, starting_node):
        """Constructor."""
        super().__init__(starting_node=starting_node, character_type=CharacterType.PACMAN, moving_speed=utils.CHARACTER_MOVING_SPEED.value)

