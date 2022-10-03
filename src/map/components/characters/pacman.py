#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from __future__ import annotations

from .character import Character
from .character_type import CharacterType
from src.map.components.elementary import MapParticles
from src.map.components.food import FoodType
import src.utils as utils
import src.utils.animations as animations

from typing import Any


class Pacman(Character):
    """Pacman class."""

    def __init__(self, starting_node):
        """Constructor."""
        super().__init__(
            starting_node=starting_node,
            character_type=CharacterType.PACMAN,
            moving_speed_percentage=utils.CHARACTER_PACMAN_MOVING_SPEED_PERCENTAGE.value
        )
        self._reinit()
        self._score = 0
        self._num_of_coins_collected = 0
        self._lives = utils.CHARACTER_PACMAN_LIVES.value
        self._boosted = False

    def _reinit(self) -> None:
        """Overrides in Character."""
        super()._reinit()
        self._future_big_node = None
        self._future_moving_direction = utils.Directions.UNDEFINED
        self._dying = False
        return None

    @property
    def score(self) -> int:
        """Getter."""
        return self._score

    @property
    def num_of_coins_collected(self) -> int:
        """Getter."""
        return self._num_of_coins_collected

    @property
    def lives(self) -> int:
        """Getter."""
        return self._lives

    @property
    def boosted(self) -> bool:
        """Getter."""
        return self._boosted

    @boosted.setter
    def boosted(self, other: bool) -> None:
        """Getter."""
        self._boosted = other

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

    def intersection(self) -> None:
        """Overrides in Character."""
        if self.current_node == self._future_big_node:
            super(Pacman, self.__class__).moving_direction.fset(self, self._future_moving_direction)
            self._set_future_move()     # resets
        return None

    def eat(self) -> None:
        """Eating."""
        if hasattr(self.current_node, utils.FOOD_COLLECT_FOOD_CALLBACK_ATTR_NAME.value):
            collect_function = getattr(self.current_node, utils.FOOD_COLLECT_FOOD_CALLBACK_ATTR_NAME.value)
            score = collect_function()
            self._score += score
            self._num_of_coins_collected += 1
            self._boosted = score == FoodType.SUPER_COIN.value
            delattr(self.current_node, utils.FOOD_COLLECT_FOOD_CALLBACK_ATTR_NAME.value)
        return None

    def eat_enemy(self) -> None:
        """Eats the enemy."""
        self._score += utils.CHARACTER_ENEMY_SCORE.value
        return None

    def die(self, *args, **kwargs) -> None:
        """Starts the pacman dying animation."""

        def callback_function() -> None:
            """Callable function after dying animation is over."""
            self._dying = False
            kwargs["callback_function"]()
            return None

        self._dying = True
        if kwargs["callback_function"]:
            self._dying_animation = animations.PacmanDyingAnimation(
                instance=self,
                callback_function=callback_function
            )
            self._dying_animation.start()
            self._lives -= 1
        return None

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Overrides the method from the Character class."""
        if self._dying:
            self._dying_animation.update()
        else:
            super().update(args, kwargs)
            self.eat()
