#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from __future__ import annotations

from copy import copy

from .character_type import CharacterType
from src.map.components.elementary import NodeType
from abc import ABC, abstractmethod
import src.utils as utils
import src.utils.animations as animations

from typing import Any, TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from src.map.components.elementary import MapParticles


class Character(pygame.sprite.Sprite, ABC):
    """Character class."""

    def __init__(self, name: str, starting_node: MapParticles.BigNode, character_type: CharacterType, moving_speed_percentage: float, body_assets_dir: str):
        """Construcotr."""
        self._name = name
        self._starting_node = starting_node
        self._character_type = character_type
        self._moving_speed_percentage = moving_speed_percentage
        self._moving_speed = self._starting_node.size * self._moving_speed_percentage
        super().__init__()

        self._relevant_size = self._starting_node.size * utils.CHARACTER_RELEVANT_SIZE_PERCENTAGE.value
        # import character's body
        utils.import_assets(
            instance=self,
            attr_name=utils.CHARACTER_BODY_ASSETS_ATTR_NAME.value,
            directory=body_assets_dir,
            relevant_size=self._relevant_size,
            smoothscale=True
        )

        self._reinit()

        # animations
        self._moving_animation = animations.MovingAnimation(instance=self)
        self._moving_animation.start()

        # body color
        self._body_color_surface = pygame.Surface(self.image.get_size()).convert_alpha()

    def _reinit(self) -> None:
        """Reinits the character, usually after respawning."""
        self._moving_direction = utils.CHARACTER_DEFAULT_DIRECTION.value
        self._on_intersection = False
        self._previous_node = None
        self._current_node = self._starting_node
        self._moving, self._future_node = None, None
        self.set_future_node()
        self._on_bridge = False
        self._freezed = False
        self._hidden = False
        self._x, self._y = self._starting_node.pos_xy
        return None

    @property
    def moving_speed(self) -> float:
        """Getter."""
        return self._moving_speed

    @property
    def moving_speed_percentage(self) -> float:
        """Getter."""
        return self._moving_speed_percentage

    @moving_speed_percentage.setter
    def moving_speed_percentage(self, other: float) -> None:
        """Setter."""
        self._moving_speed_percentage = other
        self._moving_speed = self._starting_node.size * self._moving_speed_percentage

    @property
    def moving_direction(self) -> utils.Directions:
        """Getter."""
        return self._moving_direction

    @moving_direction.setter
    def moving_direction(self, other: utils.Directions) -> None:
        if other != utils.Directions.UNDEFINED and self.current_node.type != NodeType.BRIDGE and not self._freezed:
            self._moving_direction = other
            self._current_animation_assets_attr_name = utils.CHARACTER_ANIMATION_IMAGES_ATTR_NAMES.value[self._moving_direction.name.lower()]
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
    def relevant_size(self) -> float:
        """Getter."""
        return self._relevant_size

    @property
    def on_intersection(self) -> bool:
        """Getter."""
        return self._on_intersection

    def is_on_intersection(self) -> bool:
        """Getter."""
        return self.current_node.is_big_node()

    @abstractmethod
    def intersection(self) -> None:
        """Method is called when character is on the intersection for the first time. Must be overrided."""
        pass

    @property
    def position(self) -> tuple[float, float]:
        """Getter."""
        return self._x, self._y

    @property
    def previous_node(self) -> MapParticles.BigNode:
        """Getter."""
        return self._previous_node

    @property
    def current_node(self) -> MapParticles.BigNode:
        """Getter."""
        return self._current_node

    @property
    def future_node(self) -> MapParticles.BigNode:
        """Getter."""
        return self._future_node

    @property
    def freezed(self) -> bool:
        """Getter."""
        return self._freezed

    @freezed.setter
    def freezed(self, other: bool) -> None:
        """
        Freezes the character.
        Moving and direction changes are disabled.
        Moving animations will be finished.
        """
        self._freezed = other
        if self._freezed:
            self._moving_animation.finish()
        else:
            self._moving_animation.start()

    @property
    def hidden(self) -> bool:
        """Getter."""
        return self._hidden

    @hidden.setter
    def hidden(self, other: bool) -> None:
        """Setter."""
        self._hidden = other

    def get_character_body_assets(self) -> list[pygame.image] | None:
        """Derived class returns a list with character's body assets."""
        if hasattr(self, utils.CHARACTER_BODY_ASSETS_ATTR_NAME.value):
            return getattr(self, utils.CHARACTER_BODY_ASSETS_ATTR_NAME.value)
        return None

    def respawn(self) -> None:
        """Respawns the character."""
        self._reinit()
        # self._moving_animation.start()
        return None

    def set_current_node(self) -> None:
        """Setter. Syntatic sugar method."""
        self._previous_node = self._current_node
        self._current_node = self._future_node
        self._x, self._y = self._current_node.pos_xy
        self._on_intersection = False
        return None

    def set_future_node(self) -> None:
        """Setter."""
        self._future_node = self._current_node.neighbours.get(direction=self._moving_direction)
        self.moving = self._future_node is not None
        return None

    def check_current_node(self) -> bool:
        """Method checks if character is still over the current node, or not."""
        check_func = lambda c1, c2: abs(c1 - c2) <= self._future_node.size * utils.CHARACTER_CHECKING_POSITION_AXES_THRESHOLD.value
        if self._future_node and all(check_func(c1=cord_1, c2=cord_2) for cord_1, cord_2 in zip(self.position, self._future_node.pos_xy)):
            return True
        return False

    def _cross_map(self) -> bool:
        """Method checks if character is about to pass the map from the one side to the another."""
        if self.current_node.type == NodeType.BRIDGE:
            if not self._on_bridge:
                self._on_bridge = True
                return True
            return False
        else:
            self._on_bridge = False
            return False

    def _move_position(self) -> None:
        """Moves the x and y coordinates."""
        self._x, self._y = (
            i + j * self._moving_speed for i, j in zip(
                (self._x, self._y), utils.DIRECTIONS_COORDINATES_DIFFERENCE.value[self._moving_direction]
            )
        )
        return None

    def move(self) -> None:
        """Moves the character."""
        if self.is_on_intersection() and not self._on_intersection:
            self._on_intersection = True
            self.intersection()

        if self.moving:
            if self._cross_map():
                self.set_current_node()
                self.set_future_node()
            else:
                self._move_position()
                if self.check_current_node():
                    self.set_current_node()
                    self.set_future_node()
        return None

    @abstractmethod
    def die(self, *args, **kwargs) -> None:
        """Method is called when character dies."""
        pass

    @property
    @abstractmethod
    def body_color(self) -> tuple:
        """Returns the character's body color."""
        pass

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Method updates food object."""
        # movement
        if not self._freezed:
            self.move()

        # animations
        self._moving_animation.update()

        # update body color
        self.image = self.update_body_color()
        return None

    def update_body_color(self) -> pygame.Surface:
        """Method updates the character's body color."""
        # update the copy - because of layers and transparency!
        image_cpy = copy(self.image)
        self._body_color_surface.fill(self.body_color)
        image_cpy.blit(self._body_color_surface, self._body_color_surface.get_rect(), special_flags=pygame.BLEND_RGBA_ADD)
        return image_cpy
