#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from abc import ABC, abstractmethod
from enum import Enum


class FoodType(Enum):
    """Food types."""

    COIN = 0
    SUPER_COIN = 1
    CHERRY = 2
    ENEMY = 3
    NONE = 4


class Food(ABC):
    """Food class."""

    def __init__(self, food_type):
        """
        Constructor.
        """
        self._type = FoodType.NONE
        if Food._check_instance(food_type):
            self._type = food_type

    @staticmethod
    def _check_instance(instance):
        """Checks given instance."""
        if isinstance(instance, FoodType):
            return True
        raise TypeError(f"food_type attribute must be instance of {type(FoodType)}, got {type(instance)} instead")

    @property
    def type(self):
        """Getter."""
        return self._type

    @type.setter
    def type(self, value):
        """Setter"""
        if Food._check_instance(value):
            self._type = value

    @abstractmethod
    def value(self):
        """
        Abstract method.
        Returns the value (that is, score) when it's collected.
        """
        pass
