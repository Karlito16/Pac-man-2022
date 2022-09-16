#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from __future__ import annotations

from .animation import Animation
import src.utils as utils

import pygame.sprite


class MovingAnimation(Animation):
    """Animation class."""

    def __init__(self, instance: pygame.sprite.Sprite):
        """Constructor."""
        super().__init__(
            instance=instance,
            counter=utils.CycleCounter,
            init_value=0,
            count_from=0,
            count_to=len(getattr(instance, instance.current_animation_assets_attr_name)),
            count_speed=utils.CHARACTER_MOVING_ANIMATION_SPEED.value,
            step_function=self.step_function,
            resolve_function=self.resolve_function,
            count_int=True,
            count_repeat=-1
        )

    def update_image(self) -> None:
        """Updates the instance.image object."""
        self.instance.image = getattr(self.instance, self.instance.current_animation_assets_attr_name)[self.value]
        return None

    def update_rect(self) -> None:
        """Updates the instance.rect object."""
        super().update_rect()
        self.instance.rect.center = self.instance.position
        return None
