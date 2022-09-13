#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević

from src.map.components.characters.character_type import CharacterType
from src.map.components.elementary import MapParticles
from abc import ABC
import src.utils as utils

from typing import Any
import pygame


class Character(pygame.sprite.Sprite, ABC):
    """Character class."""

    def __init__(self, starting_node: MapParticles.BigNode, character_type: CharacterType, moving_speed: float):
        """Construcotr."""
        self._starting_node = starting_node
        self._character_type = character_type
        self._moving_speed = moving_speed
        super().__init__()

        self._relevant_size = self._starting_node.size * utils.CHARACTER_RELEVANT_SIZE_PERCENTAGE.value
        # imports the assets for walking and for dying
        for side_name in [key.name.lower() for key in utils.Directions if key != utils.Directions.UNDEFINED] + ["death"]:
            utils.import_assets(
                instance=self,
                attr_name=f"{utils.CHARACTER_ANIMATION_ATTRIBUTE_BASE_NAME.value}{side_name}",
                directory=f"{utils.CHARACHERS_DIR.value}\\{self._character_type.name}",
                relevant_size=self._relevant_size,
                directory_constraints=[side_name, "full"],
                wshadow=True
            )

        self._moving_direction = utils.CHARACTER_DEFAULT_DIRECTION.value
        self._moving = True
        self._current_animation_index = 0
        self._x, self._y = self._starting_node.pos_xy
        self.image = getattr(self, self._current_animation_assets_attr_name)[self._current_animation_index]
        self.rect = self.image.get_rect(center=(self._x, self._y))

        # animations
        self._moving_animation = utils.Counter(
            count_from=0,
            count_to=len(getattr(self, self._current_animation_assets_attr_name)),
            count_speed=utils.CHARACTER_MOVING_ANIMATION_SPEED.value,
            step_function=self._set_current_image_index,
            resolve_function=lambda: self._set_current_image_index(index=0),
            count_int=True,
            count_repeat=-1     # infinity
        )
        self._moving_animation.start()

    @property
    def moving_direction(self) -> utils.Directions:
        """Getter."""
        return self._moving_direction

    @moving_direction.setter
    def moving_direction(self, other: utils.Directions) -> None:
        if other != utils.Directions.UNDEFINED:
            self._moving_direction = other

    @property
    def moving(self) -> bool:
        """Getter."""
        return self._moving

    @moving.setter
    def moving(self, other: bool) -> None:
        """Setter."""
        self._moving = other

    @property
    def _current_animation_assets_attr_name(self) -> str:
        """Returns the attribute name."""
        return f"{utils.CHARACTER_ANIMATION_ATTRIBUTE_BASE_NAME.value}{self._moving_direction.name.lower()}"

    def get_image(self) -> pygame.Surface:
        """Returns the new image object."""
        return getattr(self, self._current_animation_assets_attr_name)[self._current_image_index]

    def move(self) -> None:
        """Moves the character."""
        self._x, self._y = (
            i + j * self._moving_speed for i, j in zip(
                (self._x, self._y), utils.DIRECTIONS_COORDINATES_DIFFERENCE.value[self._moving_direction]
            )
        )
        return None

    def _set_current_image_index(self, index: int) -> None:
        """Callback function."""
        self._current_image_index = index
        return None

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Method updates food object."""
        # animations
        self._moving_animation.next()

        # movement
        if self.moving:
            self.move()

        self.image = self.get_image()
        self.rect = self.image.get_rect(center=(self._x, self._y))
