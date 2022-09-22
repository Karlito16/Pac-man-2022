#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from __future__ import annotations

from .character import Character
from .character_type import CharacterType
from src.map.components.elementary import MapParticles
import src.utils as utils

from typing import Any


class Pacman(Character):
    """Pacman class."""

    def __init__(self, starting_node):
        """Constructor."""
        super().__init__(
            starting_node=starting_node,
            character_type=CharacterType.PACMAN,
            moving_speed_percentage=utils.CHARACTER_MOVING_SPEED_PERCENTAGE.value
        )
        self._future_big_node = None
        self._future_moving_direction = utils.Directions.UNDEFINED

    def has_future_move(self) -> bool:
        """Method returns if character is about to change it's direction."""
        return self._future_big_node and self._future_moving_direction != utils.Directions.UNDEFINED

    def _set_future_move(self, future_move: utils.Directions = None) -> None:
        """Method sets the future move for the character."""
        self._future_big_node = self._look_for_future_big_node(future_move=future_move) if future_move else None
        self._future_moving_direction = future_move if self._future_big_node else utils.Directions.UNDEFINED
        return None

    def _look_for_future_big_node(self, future_move: utils.Directions) -> MapParticles.BigNode | None:
        """Looks for the future big node in the near environment."""
        node = self.current_node
        for _ in range(utils.CHARACTER_LOOK_FOR_BIG_NODE_TRESHOLD.value):
            next_node = node.neighbours.get(direction=self.moving_direction)
            if next_node is None:
                break
            if isinstance(next_node, MapParticles.BigNode) and next_node.neighbours.get(direction=future_move):
                return next_node
            node = next_node
        return None

    @property
    def moving_direction(self) -> utils.Directions:
        """Getter."""
        return super().moving_direction

    @moving_direction.setter
    def moving_direction(self, other: utils.Directions) -> None:
        """Setter."""
        if utils.Directions.get_opposite(direction=other) == self.moving_direction or not self.moving:
            self._set_future_move()     # resets
            super(Pacman, self.__class__).moving_direction.fset(self, other)
        else:
            self._set_future_move(future_move=other)

    def move(self) -> None:
        """Overrides the method in Character class."""
        super().move()
        if self.current_node == self._future_big_node:
            super(Pacman, self.__class__).moving_direction.fset(self, self._future_moving_direction)
            self._set_future_move()     # resets
        return None

    def eat(self) -> None:
        """Eating."""
        if hasattr(self.current_node, utils.FOOD_COLLECT_FOOD_CALLBACK_ATTR_NAME.value):
            score = getattr(self.current_node, utils.FOOD_COLLECT_FOOD_CALLBACK_ATTR_NAME.value)()

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Overrides the method from the Character class."""
        super().update(args, kwargs)
        self.eat()
