#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


import src.utils as utils
from abc import ABC, abstractmethod
import pygame


class Screen(pygame.Surface, ABC):
    """Screen class."""

    def __init__(self):
        """Constructor."""
        super().__init__(utils.WIN_SIZE.value)

    @property
    @abstractmethod
    def name(self) -> str:
        """Returns the screen name."""
        pass

    @abstractmethod
    def update(self, events: list[pygame.event.Event]) -> None:
        """Updates the screen at singular frame."""
        pass
