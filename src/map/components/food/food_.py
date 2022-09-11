#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from .food_status import FoodStatus
import src.utils as utils

from typing import Any
from abc import ABC, abstractmethod
import pygame


class Food(pygame.sprite.Sprite, ABC):
    """Food class."""

    def __init__(self, node):
        """
        Constructor.
        """
        self._node = node
        super().__init__()

        self._animation_images = list(
            utils.scale_images(
                *list(
                    utils.load_images(
                        directory=f"{utils.FOOD_DIR.value}\\{self.type.name}"
                    )
                ),
                relevant_size=self.relevant_size
            )
        )
        if len(self._animation_images) < utils.MINIMAL_REQUIRED_ANIMATION_IMAGES.value:
            raise ValueError(f"minimal required amount of animations is: {utils.MINIMAL_REQUIRED_ANIMATION_IMAGES.value}")

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
            resolve_function=lambda: self._scale_images(scale_factor=0)
        )
        self._fade_animation = utils.ConditionalCounter(
            condition_function=self._is_faded,
            count_from=utils.COLORS_ALPHA_MIN.value,
            count_speed=-utils.FOOD_FADE_ANIMATION_SPEED.value,
            step_function=self._set_alpha,
            resolve_function=lambda: self._set_alpha(alpha_value=utils.COLORS_ALPHA_MAX.value),
            count_int=True
        )

    @property
    def node(self):
        """Getter."""
        return self._node

    @property
    def status(self):
        """Getter."""
        return self._status

    def _set_current_image_index(self, index: int) -> None:
        """Callback function."""
        self._current_image_index = index
        return None

    def _scale_images(self, scale_factor: float) -> None:
        """Callback function."""
        self._animation_images = list(
            utils.scale_images(
                *self._animation_images,
                relevant_size=self.relevant_size * (1 + scale_factor)
            )
        )
        return None

    def _set_alpha(self, alpha_value: int) -> None:
        """Callback function."""
        self._alpha_value = alpha_value
        return None

    def _is_faded(self):
        """Callback function."""
        current_alpha = self.image.get_alpha()
        if current_alpha > 0:
            return False
        return True

    @status.setter
    def status(self, other: FoodStatus):
        """Setter."""
        self._status = other

    def is_flashing(self):
        """Getter."""
        return self._flashing_animation.counting

    def set_flashing(self):
        """Setter."""
        if not self.is_flashing():
            self._flashing_animation.start()

    def is_collecting(self):
        """Getter."""
        return self._collect_animation.counting

    def is_collected(self):
        """Getter."""
        return self._status == FoodStatus.COLLECTED

    def collect(self):
        """Collects the food object."""
        if self._status == FoodStatus.UNCOLLECTED:
            self._status = FoodStatus.COLLECTING
            self._collect_animation.start()
            self._fade_animation.start()

    @property
    @abstractmethod
    def type(self):
        """Getter."""
        pass

    @property
    @abstractmethod
    def value(self):
        """
        Abstract method.
        Returns the value (that is, score) when it's collected.
        """
        pass

    @property
    @abstractmethod
    def relevant_size(self):
        """Returns the relevant size of the food object."""
        pass

    def _center(self):
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
