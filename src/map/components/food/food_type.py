#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from enum import Enum, unique


@unique
class FoodType(Enum):
    """Food type enum."""

    COIN = 50
    SUPER_COIN = 100
    CHERRY = 500
    ENEMY = 200
