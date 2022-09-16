#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from __future__ import annotations

from .animation import Animation
import src.utils as utils

import pygame.sprite


class FadeAnimation(Animation):
    """Animation class."""

    def __init__(self, instance: pygame.sprite.Sprite):
        """Constructor."""
        super().__init__(
            instance=instance,
            counter=utils.ConditionalCounter,
            init_value=utils.COLORS_ALPHA_MIN.value,
            condition_function=self.condition_function,
            count_from=utils.COLORS_ALPHA_MIN.value,
            count_speed=-utils.FOOD_FADE_ANIMATION_SPEED.value,
            step_function=self.step_function,
            resolve_function=self.resolve_function,
            count_int=True
        )

    def resolve_function(self) -> None:
        """Callable function."""
        self.instance.set_collected()
        self.step_function(step_value=utils.COLORS_ALPHA_MAX.value)
        return None

    def condition_function(self) -> bool:
        """Callable function."""
        return self.instance.image.get_alpha() <= 0

    def update_image(self) -> None:
        """Updates the instance.image object."""
        self.instance.image.set_alpha(self.value)
        return None

    def update_rect(self) -> None:
        """Updates the instance.rect object."""
        super().update_rect()
        self.instance.rect.center = self.instance.center()
        return None
