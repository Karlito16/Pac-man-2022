#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević

from __future__ import annotations

from .food_status import FoodStatus
from .food_type import FoodType
from ..elementary import MapParticles
import src.utils as utils
import src.utils.animations as animations

from abc import ABC, abstractmethod
from typing import Any, Iterable
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

        self._animation_images = list()
        utils.import_assets(
            instance=self,
            attr_name="_animation_images",
            directory=f"{utils.FOOD_DIR.value}\\{self.type.name}",
            relevant_size=self.relevant_size
        )

        self._current_image_index = 0
        self._alpha_value = 255
        self.image = self._animation_images[self._current_image_index]
        self.rect = self.image.get_rect(center=self.center())
        self._status = FoodStatus.UNCOLLECTED

        self._flashing_animation = animations.FlashingAnimation(instance=self)
        self._collecting_animation = animations.CollectingAnimation(instance=self)
        self._fade_animation = animations.FadeAnimation(instance=self)

    @property
    def node(self) -> MapParticles.Node | MapParticles.BigNode:
        """Getter."""
        return self._node

    @property
    def animation_images(self) -> Iterable[pygame.Surface, ]:
        """Getter."""
        return self._animation_images

    @property
    def status(self) -> FoodStatus:
        """Getter."""
        return self._status

    @status.setter
    def status(self, other: FoodStatus) -> None:
        """Setter."""
        self._status = other

    @property
    def flashing_animation(self) -> animations.FlashingAnimation:
        """Getter."""
        return self._flashing_animation

    def is_flashing(self) -> bool:
        """Getter."""
        return self._flashing_animation.is_alive()

    def set_flashing(self) -> None:
        """Setter."""
        if not self.is_flashing() and not self.is_collected():
            self._flashing_animation.start()
            pass
        return None

    def is_uncollected(self) -> bool:
        """Getter."""
        return self._status == FoodStatus.UNCOLLECTED

    def is_collecting(self) -> bool:
        """Getter."""
        return self._status == FoodStatus.COLLECTING

    def is_collected(self) -> bool:
        """Getter."""
        return self._status == FoodStatus.COLLECTED

    def set_collected(self) -> None:
        """Setter."""
        self._status = FoodStatus.COLLECTED
        return None

    def collect(self) -> int:
        """Collects the food object. Returns the value that food object holds."""
        if self._status == FoodStatus.UNCOLLECTED:
            self._status = FoodStatus.COLLECTING
            self._collecting_animation.start()
            self._fade_animation.start()
            return self.value
        return 0

    def center(self) -> tuple[int, int]:
        """Syntactic sugar method."""
        return self.node.pos_xy

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Method updates food object."""
        self._flashing_animation.update()
        self._collecting_animation.update()
        self._fade_animation.update()

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
