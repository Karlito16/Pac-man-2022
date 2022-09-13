#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from .food_ import Food
from .food_type import FoodType
from ..elementary import MapParticles
import src.utils as utils


class Cherry(Food):
    """Cherry class."""

    def __init__(self, node: MapParticles.Node):
        """
        Constructor
        """
        super().__init__(node=node)

    @property
    def type(self) -> FoodType:
        """Getter."""
        return FoodType.CHERRY

    @property
    def value(self) -> int:
        """Returns the value (that is, score) when it's collected."""
        return self.type.value

    @property
    def relevant_size(self) -> float:
        return utils.FOOD_CHERRY_RELEVANT_SIZE_PERCENTAGE.value
