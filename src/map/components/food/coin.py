#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from .food_ import Food
from .food_type import FoodType
import src.utils as utils


class Coin(Food):
    """Coin class."""

    def __init__(self, node):
        """
        Constructor
        """
        super().__init__(node=node)

    @property
    def type(self):
        """Getter."""
        return FoodType.COIN

    @property
    def value(self):
        """Returns the value (that is, score) when it's collected."""
        return self.type.value

    @property
    def relevant_size(self):
        """Returns the relevant size of the food object."""
        return self.node.size * utils.FOOD_COIN_RELEVANT_SIZE_PERCENTAGE.value
