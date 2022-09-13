#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from .food_ import Food
from .food_type import FoodType
from ..elementary import MapParticles
import src.utils as utils


class SuperCoin(Food):
    """SuperCoin class."""

    def __init__(self, node: MapParticles.Node):
        """
        Constructor
        """
        super().__init__(node=node)

    @property
    def type(self) -> FoodType:
        """Getter."""
        return FoodType.SUPER_COIN

    @property
    def value(self) -> int:
        """Returns the value (that is, score) when it's collected."""
        return self.type.value

    @property
    def relevant_size(self) -> float:
        """Returns the relevant size of the food object."""
        return self.node.size * utils.FOOD_SUPER_COIN_RELEVANT_SIZE_PERCENTAGE.value
