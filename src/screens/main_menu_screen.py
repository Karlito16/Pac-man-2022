#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from .screen import Screen
import src.utils as utils
import pygame


class MainMenuScreen(Screen):
    """Main Menu Screen class."""

    def __init__(self):
        """Constructor."""
        super().__init__()

    @property
    def name(self) -> str:
        """Overrides in Screen."""
        return utils.MAIN_MENU_SCREEN.value

    def update(self, events: list[pygame.event.Event]) -> None:
        """Overrides in Screen."""
        return None
