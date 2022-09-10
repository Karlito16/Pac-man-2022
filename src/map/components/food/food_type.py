#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from enum import Enum, unique


@unique
class FoodType(Enum):
    """Food type enum."""

    COIN = "coin"
    SUPER_COIN = "super_coin"
    CHERRY = "cherry"
    ENEMY = "enemy"
