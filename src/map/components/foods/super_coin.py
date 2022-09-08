#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from .food import Food, FoodType


class SuperCoin(Food):
    """SuperCoin class."""

    def __init__(self):
        """
        Constructor
        """
        super().__init__(food_type=FoodType.SUPER_COIN)

    def value(self):
        """Returns the value (that is, score) when it's collected."""
        pass