#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from __future__ import annotations

from .character_type import CharacterType
from src.map.components.elementary import NodeType
from abc import ABC
import src.utils as utils

from typing import Any, TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from src.map.components.elementary import MapParticles


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
        self._current_node = self._starting_node
        self._future_node = self._current_node.neighbours.get(direction=self._moving_direction)
        self._on_bridge = False
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
        if other != utils.Directions.UNDEFINED and self.current_node.type != NodeType.BRIDGE:
            self._moving_direction = other
            self.set_future_node()

    @property
    def moving(self) -> bool:
        """Getter."""
        return self._moving

    @moving.setter
    def moving(self, other: bool) -> None:
        """Setter."""
        self._moving = other

    @property
    def position(self) -> tuple[float, float]:
        """Getter."""
        return self._x, self._y

    @property
    def current_node(self) -> MapParticles.BigNode:
        """Getter."""
        return self._current_node

    def set_current_node(self) -> None:
        """Setter. Syntatic sugar method."""
        self._current_node = self._future_node
        self._x, self._y = self._current_node.pos_xy
        return None

    def set_future_node(self) -> None:
        """Setter."""
        self._future_node = self._current_node.neighbours.get(direction=self._moving_direction)
        self.moving = self._future_node is not None
        return None

    @property
    def _current_animation_assets_attr_name(self) -> str:
        """Returns the attribute name."""
        return f"{utils.CHARACTER_ANIMATION_ATTRIBUTE_BASE_NAME.value}{self._moving_direction.name.lower()}"

    def get_image(self) -> pygame.Surface:
        """Returns the new image object."""
        return getattr(self, self._current_animation_assets_attr_name)[self._current_image_index]

    def _check_current_node(self) -> bool:
        """Method checks if character is still over the current node, or not."""
        check_func = lambda c1, c2: abs(c1 - c2) <= self._future_node.size * utils.CHARACTER_CHECKING_POSITION_AXES_THRESHOLD.value
        if all(check_func(c1=cord_1, c2=cord_2) for cord_1, cord_2 in zip(self.position, self._future_node.pos_xy)):
            self.set_current_node()
            self.set_future_node()
            return True
        return False

    def _check_passage(self) -> bool:
        """Method checks if character is about to pass the map from the one side to the another."""
        if self.current_node.type == NodeType.BRIDGE:
            if not self._on_bridge:
                self.set_current_node()
                self.set_future_node()
                self._on_bridge = True
        else:
            self._on_bridge = False
        return self._on_bridge

    def move(self) -> None:
        """Moves the character."""
        self._x, self._y = (
            i + j * self._moving_speed for i, j in zip(
                (self._x, self._y), utils.DIRECTIONS_COORDINATES_DIFFERENCE.value[self._moving_direction]
            )
        )
        self._check_current_node()
        self._check_passage()
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
