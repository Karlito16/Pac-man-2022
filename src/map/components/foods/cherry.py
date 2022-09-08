#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from .food import Food, FoodType


class Cherry(Food):
    """Cherry class."""

    def __init__(self):
        """
        Constructor
        """
        super().__init__(food_type=FoodType.CHERRY)

    def value(self):
        """Returns the value (that is, score) when it's collected."""
        pass
