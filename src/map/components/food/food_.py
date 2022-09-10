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

        self.image = self._animation_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = self._center()
        self._status = FoodStatus.UNCOLLECTED
        self._flashing_animation_counter = utils.AnimationCounter(
            count_from=0,
            count_to=len(self._animation_images),
            step=utils.FOOD_FLASH_ANIMATION_SPEED.value
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
        """Method calculates the position for food object."""
        node_size = self._node.size
        grid_slot_size = node_size / utils.MAP_GRID_SLOT_NODE_SIZE_RELATION.value
        x = grid_slot_size * self.node.i
        y = grid_slot_size * self.node.j
        return x, y

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Method updates food object."""
        # flashing animation
        if self.is_flashing():
            self.image = self._animation_images[self._flashing_animation_counter.next_int()]
