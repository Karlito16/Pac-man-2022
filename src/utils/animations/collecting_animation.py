#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from __future__ import annotations

from .animation import Animation
import src.utils as utils

import pygame.sprite


class CollectingAnimation(Animation):
    """Animation class."""

    def __init__(self, instance: pygame.sprite.Sprite):
        """Constructor."""
        super().__init__(
            instance=instance,
            counter=utils.CycleCounter,
            init_value=0,
            count_from=0,
            count_to=utils.FOOD_COLLECTING_ANIMATION_MAX_SIZE_PERCENTAGE.value,
            count_speed=utils.FOOD_COLLECTING_ANIMATION_SPEED.value,
            step_function=self.step_function,
            resolve_function=self.resolve_function
        )

    def resolve_function(self) -> None:
        """Callable function."""
        self.instance.set_collected()
        super().resolve_function()
        return None

    def update_image(self) -> None:
        """Updates the instance.image object."""
        self.instance.image = utils.scale_image(
            img=self.instance.image,
            relevant_size=self.instance.relevant_size * (1 + self.value)
        )
        return None

    def update_rect(self) -> None:
        """Updates the instance.rect object."""
        super().update_rect()
        self.instance.rect.center = self.instance.center()
        return None
