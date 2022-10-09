#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from __future__ import annotations

import pygame

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
            name=utils.CHARACTER_PACMAN_NAME.value,
            starting_node=starting_node,
            character_type=CharacterType.PACMAN,
            moving_speed_percentage=utils.CHARACTER_PACMAN_MOVING_SPEED_PERCENTAGE.value,
            body_assets_dir=utils.CHARACTERS_PACMAN_BODY_DIR.value
        )
        self._init_pacman_body_assets()
        self._reinit()
        self._score = 0
        self._num_of_coins_collected = 0
        self._lives = utils.CHARACTER_PACMAN_LIVES.value
        self._boosted = False
        self._body_color = utils.add_transparency(color=utils.color_hex_to_tuple(color_hex=utils.COLORS_PACMAN.value))

    def _init_pacman_body_assets(self) -> None:
        """Inits the pacman body assets, depending on possible moving direciton or death."""
        self._pacman_body_assets = dict()
        for direction, angle in utils.DIRECTION_ANGLE.value.items():
            self._pacman_body_assets[direction] = list(utils.rotate_images(*super().get_character_body_assets(), angle=angle, relevant_size=self.relevant_size))
        self._pacman_body_assets[utils.CHARACTER_DEATH_KEYWORD.value] = utils.import_assets(
            instance=self,
            directory=utils.CHARACTERS_PACMAN_DEATH_DIR.value,
            relevant_size=self.relevant_size,
        )
        return None

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

    @property
    def body_color(self) -> tuple:
        """Overrides in Character."""
        return self._body_color

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

    def get_character_body_assets(self) -> list[pygame.image] | None:
        """Overrides in Character."""
        try:
            key = utils.CHARACTER_DEATH_KEYWORD.value if self._dying else self.moving_direction
            return self._pacman_body_assets[key]
        except AttributeError:
            return super().get_character_body_assets()

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
            self.image = self.update_body_color()
        else:
            super().update(args, kwargs)
            self.eat()
        return None
