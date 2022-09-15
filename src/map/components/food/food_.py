#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević

from __future__ import annotations

from .food_status import FoodStatus
from .food_type import FoodType
from ..elementary import MapParticles
import src.utils as utils

from abc import ABC, abstractmethod
from typing import Any
import pygame


class Food(pygame.sprite.Sprite, ABC):
    """Food class."""

    def __init__(self, node: MapParticles.Node):
        """
        Constructor.
        """
        self._node = node
        super().__init__()

        setattr(self._node, utils.FOOD_COLLECT_FOOD_CALLBACK_ATTR_NAME.value, self.collect)

        utils.import_assets(
            instance=self,
            attr_name="_animation_images",
            directory=f"{utils.FOOD_DIR.value}\\{self.type.name}",
            relevant_size=self.relevant_size
        )

        self._current_image_index = 0
        self._alpha_value = 255
        self.image = self._animation_images[self._current_image_index]
        self.rect = self.image.get_rect(center=self._center())
        self._status = FoodStatus.UNCOLLECTED

        self._flashing_animation = utils.CycleCounter(
            count_from=0,
            count_to=len(self._animation_images),
            count_speed=utils.FOOD_FLASH_ANIMATION_SPEED.value,
            step_function=self._set_current_image_index,
            resolve_function=lambda: self._set_current_image_index(0),
            count_int=True
        )
        self._collect_animation = utils.CycleCounter(
            count_from=0,
            count_to=utils.FOOD_COLLECTING_ANIMATION_MAX_SIZE_PERCENTAGE.value,
            count_speed=utils.FOOD_COLLECTING_ANIMATION_SPEED.value,
            step_function=self._scale_images,
            resolve_function=self._end_collect_animation
        )
        self._fade_animation = utils.ConditionalCounter(
            condition_function=self._is_faded,
            count_from=utils.COLORS_ALPHA_MIN.value,
            count_speed=-utils.FOOD_FADE_ANIMATION_SPEED.value,
            step_function=self._set_alpha,
            resolve_function=self._end_fade_animation,
            count_int=True
        )

    @property
    def node(self) -> MapParticles.Node | MapParticles.BigNode:
        """Getter."""
        return self._node

    @property
    def status(self) -> FoodStatus:
        """Getter."""
        return self._status

    @status.setter
    def status(self, other: FoodStatus) -> None:
        """Setter."""
        self._status = other

    def _set_current_image_index(self, index: int) -> None:
        """Callback function."""
        self._current_image_index = index
        return None

    def _scale_images(self, scale_factor: float) -> None | AttributeError:
        """Callback function."""
        if hasattr(self, "_animation_images"):
            self._animation_images = list(
                utils.scale_images(
                    *self._animation_images,
                    relevant_size=self.relevant_size * (1 + scale_factor)
                )
            )
            return None
        else:
            raise AttributeError(f"No attribute named: '_animation_images'")

    def _set_alpha(self, alpha_value: int) -> None:
        """Callback function."""
        self._alpha_value = alpha_value
        return None

    def _end_collect_animation(self) -> None:
        """Resolve function."""
        self._scale_images(scale_factor=0)
        if not self._fade_animation.counting:
            self._flashing_animation.end()
            self._status = FoodStatus.COLLECTED
        return None

    def _end_fade_animation(self) -> None:
        """Resolve function."""
        self._set_alpha(alpha_value=utils.COLORS_ALPHA_MAX.value)
        if not self._collect_animation.counting:
            self._flashing_animation.end()
            self._status = FoodStatus.COLLECTED
        return None

    def _is_faded(self) -> bool:
        """Callback function."""
        current_alpha = self.image.get_alpha()
        if current_alpha > 0:
            return False
        return True

    def is_flashing(self) -> bool:
        """Getter."""
        return self._flashing_animation.counting

    def set_flashing(self) -> None:
        """Setter."""
        if not self.is_flashing():
            self._flashing_animation.start()

    def is_collecting(self) -> bool:
        """Getter."""
        return self._status == FoodStatus.COLLECTING

    def is_collected(self) -> bool:
        """Getter."""
        return self._status == FoodStatus.COLLECTED

    def collect(self) -> int:
        """Collects the food object. Returns the value that food object holds."""
        if self._status == FoodStatus.UNCOLLECTED:
            self._status = FoodStatus.COLLECTING
            self._collect_animation.start()
            self._fade_animation.start()
            return self.value
        return 0

    def _center(self) -> tuple[int, int]:
        """Syntactic sugar method."""
        return self.node.pos_xy

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Method updates food object."""
        # animations
        self._flashing_animation.next()
        self._collect_animation.next()
        self._fade_animation.next()

        self.image = self._animation_images[self._current_image_index]
        self.image.set_alpha(self._alpha_value)
        self.rect = self.image.get_rect(center=self._center())

    @property
    @abstractmethod
    def type(self) -> FoodType:
        """Getter."""
        pass

    @property
    @abstractmethod
    def value(self) -> int:
        """
        Abstract method.
        Returns the value (that is, score) when it's collected.
        """
        pass

    @property
    @abstractmethod
    def relevant_size(self) -> float:
        """Returns the relevant size of the food object."""
        pass
