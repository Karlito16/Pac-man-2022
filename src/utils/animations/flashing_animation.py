#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from __future__ import annotations

from .animation import Animation
import src.utils as utils

import pygame.sprite


class FlashingAnimation(Animation):
    """Animation class."""

    def __init__(self, instance: pygame.sprite.Sprite):
        """Constructor."""
        super().__init__(
            instance=instance,
            counter=utils.CycleCounter,
            init_value=0,
            count_from=0,
            count_to=len(instance.animation_images),
            count_speed=utils.FOOD_FLASH_ANIMATION_SPEED.value,
            step_function=self.step_function,
            resolve_function=self.resolve_function,
            count_int=True
        )

    def update_image(self) -> None:
        """Updates the instance.image object."""
        self.instance.image = self.instance.animation_images[self.value]
        return None

    def update_rect(self) -> None:
        """Updates the instance.rect object."""
        super().update_rect()
        self.instance.rect.center = self.instance.center()
        return None
