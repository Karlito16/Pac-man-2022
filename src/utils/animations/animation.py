#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević

from __future__ import annotations

from abc import ABC, abstractmethod
import src.utils as utils

from typing import Any
import pygame.sprite


class Animation(ABC):
    """Animation class."""

    def __init__(self, instance: pygame.sprite.Sprite, counter: utils.Counter.__class__, init_value: Any, *args, **kwargs):
        """Constructor."""
        self._instance = instance
        self._counter = counter
        self._animation = self._counter(*args, **kwargs)
        self._init_value = init_value
        self._value = self._init_value      # measured parameter (image index, alpha value, img size, ...)
        self.update()   # inits the instance.image and instance.rect objects

    @property
    def instance(self):
        """Getter."""
        return self._instance

    @property
    def value(self) -> Any:
        """Returns the measured value."""
        return self._value

    @value.setter
    def value(self, other: Any) -> None:
        """Setter."""
        self._value = other

    def is_alive(self) -> bool:
        """Returns if animation is in progress."""
        return self._animation.counting

    def start(self) -> None:
        """Method starts the animation."""
        self._animation.start()
        return None

    def pause(self) -> None:
        """Pauses the animation."""
        self._animation.pause()
        return None

    def unpause(self) -> None:
        """Unpauses the animation."""
        self._animation.unpause()
        return None

    def is_paused(self) -> bool:
        """Returns if animation is paused."""
        return self._animation.paused

    def end(self) -> None:
        """Ends the animation."""
        self._animation.end()
        return None

    def _next(self) -> None:
        """Next iteration."""
        self._animation.next()
        return None

    def update(self) -> None:
        """Updates the instance.image and instance.rect values."""
        if self.is_alive() and not self.is_paused():
            self._next()
        self.update_image()
        self.update_rect()
        return None

    def step_function(self, step_value: int | float) -> None:
        """Callable function."""
        self.value = step_value
        return None

    def resolve_function(self) -> None:
        """Callable function."""
        self.step_function(step_value=self._init_value)
        return None

    def condition_function(self) -> bool:
        """Callable function. Must be overrided if used."""
        pass

    @abstractmethod
    def update_image(self) -> None:
        """Updates the instance.image object."""
        pass

    def update_rect(self) -> None:
        """Updates the instance.rect object."""
        self.instance.rect = self.instance.image.get_rect()
        return None
