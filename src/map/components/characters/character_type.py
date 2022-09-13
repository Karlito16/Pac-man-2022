#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from enum import Enum, unique


@unique
class CharacterType(Enum):
    """Character type."""

    PACMAN = "pacman"
    ENEMY = "enemy"
