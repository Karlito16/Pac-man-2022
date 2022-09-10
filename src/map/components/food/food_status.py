#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from enum import Enum, unique, auto


@unique
class FoodStatus(Enum):
    """Food status enum."""

    UNCOLLECTED = auto()
    COLLECTING = auto()
    COLLECTED = auto()
