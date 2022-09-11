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
        self.image = self._animation_images[self._current_image_index]
        self.rect = self.image.get_rect(center=self._center())
        self._status = FoodStatus.UNCOLLECTED

        self._flashing_animation_counter = utils.AnimationCounter(
            count_from=0,
            count_to=len(self._animation_images),
            step=utils.FOOD_FLASH_ANIMATION_SPEED.value
        )
        self._collecting_animation_counter = utils.AnimationCounter(
            count_from=0,
            count_to=utils.FOOD_COLLECTING_ANIMATION_MAX_SIZE_PERCENTAGE.value,
            step=utils.FOOD_COLLECTING_ANIMATION_SPEED.value
        )

    @property
    def node(self):
        """Getter."""
        return self._node

    @property
    def status(self):
        """Getter."""
        return self._status

    @status.setter
    def status(self, other: FoodStatus):
        """Setter."""
        self._status = other

    def is_flashing(self):
        """Getter."""
        return self._flashing_animation_counter.counting

    def set_flashing(self):
        """Setter."""
        self._flashing_animation_counter.start()

    def is_collecting(self):
        """Getter."""
        return self._collecting_animation_counter.counting

    def is_collected(self):
        """Getter."""
        return self._status == FoodStatus.COLLECTED

    def collect(self):
        """Collects the food object."""
        if self._status == FoodStatus.UNCOLLECTED:
            self._status = FoodStatus.COLLECTING
            self._collecting_animation_counter.start()

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
        # flashing animation
        if self.is_flashing():
            self._current_image_index = self._flashing_animation_counter.next_int()

        # collecting animation
        if self.is_collecting():
            self._animation_images = list(utils.scale_images(
                *self._animation_images,
                relevant_size=self.relevant_size * (1 + self._collecting_animation_counter.next())
            ))

            if not self.is_collecting():
                self._status = FoodStatus.COLLECTED

        self.image = self._animation_images[self._current_image_index]
        # next line is important because we might scale image during collecting animation, so we need to keep img in center
        self.rect = self.image.get_rect(center=self._center())
