#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from .food_ import Food
from .food_type import FoodType


class Cherry(Food):
    """Cherry class."""

    def __init__(self, node):
        """
        Constructor
        """
        super().__init__(node=node)

    @property
    def type(self):
        """Getter."""
        return FoodType.CHERRY

    @property
    def value(self):
        """Returns the value (that is, score) when it's collected."""
        return self.type.value
