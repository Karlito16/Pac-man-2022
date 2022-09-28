#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from __future__ import annotations

from typing import TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from .screen import Screen


class ScreenManager(dict):
    """Screen Manager class."""

    def __init__(self, *screens: Screen):
        """Constructor."""
        super().__init__()
        for screen in screens:
            self[screen.name] = screens
        self._active_screen = screens[0]

    @property
    def active_screen(self) -> Screen:
        """Getter."""
        return self._active_screen

    def update_active_screen(self, window: pygame.Surface, events: list[pygame.event.Event]) -> None:
        """Update method."""
        # Active screen control
        self._active_screen.update(events=events)

        # Update main window
        window.blit(self._active_screen, self._active_screen.get_rect())
        return None
