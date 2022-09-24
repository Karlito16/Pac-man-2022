#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from __future__ import annotations

from .animation import Animation
import src.utils as utils

from typing import Callable
import pygame


class PacmanDyingAnimation(Animation):
    """Animation class."""

    def __init__(self, instance: pygame.sprite.Sprite, callback_function: Callable):
        """Constructor."""
        self._attr_name = utils.CHARACTER_ANIMATION_IMAGES_ATTR_NAMES.value["death"]
        self._callback_function = callback_function
        super().__init__(
            instance=instance,
            counter=utils.Counter,
            init_value=0,
            count_from=0,
            count_to=len(getattr(instance, self._attr_name)),
            count_speed=utils.CHARACTER_MOVING_ANIMATION_SPEED.value,
            step_function=self.step_function,
            resolve_function=self.resolve_function,
            count_int=True,
            count_repeat=1
        )

    def resolve_function(self) -> None:
        """Callback."""
        super().resolve_function()
        self._callback_function()
        return None

    def update_image(self) -> None:
        """Updates the instance.image object."""
        self.instance.image = getattr(self.instance, self._attr_name)[self.value]
        return None

    def update_rect(self) -> None:
        """Updates the instance.rect object."""
        super().update_rect()
        self.instance.rect.center = self.instance.position
        return None
