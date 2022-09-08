#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević
from typing import Any

import pygame
import src.utils as utils


class Walls(pygame.sprite.Group):
    """Walls class."""

    class Wall(pygame.sprite.Sprite):
        """Wall class."""

        def __init__(self, grid_slot, grid_slot_size, wall_size, wall_color, wall_radius):
            """
            Constructor.
            """
            self._grid_slot = grid_slot
            self._grid_slot_size = grid_slot_size
            self._wall_size = wall_size
            self._wall_color = wall_color
            self._wall_radius = wall_radius
            super().__init__()
            self.image = pygame.Surface((self._grid_slot_size, self._grid_slot_size))
            self.rect = pygame.draw.rect(
                surface=self.image,
                color=self._wall_color,
                rect=self.image.get_rect(),
                width=self.wall_size,
                border_radius=self._wall_radius
            )
            self.rect.topleft = (
                self._grid_slot_size * self._grid_slot.i,
                self._grid_slot_size * self._grid_slot.j
            )

        @property
        def grid_slot(self):
            """Getter."""
            return self._grid_slot

        @property
        def wall_size(self):
            """Getter."""
            return self._wall_size

        @property
        def wall_color(self):
            """Getter."""
            return self._wall_color

        @property
        def wall_radius(self):
            """Getter."""
            return self._wall_radius

        def update(self, *args: Any, **kwargs: Any) -> None:
            """Overrides the method in sprite class."""
            pass

    def __init__(self, grid_slots_wall, grid_slot_size):
        """
        Constructor.
        """
        self._grid_slots_wall = grid_slots_wall
        super().__init__()
        for grid_slot in self._grid_slots_wall:
            self.add(Walls.Wall(
                grid_slot=grid_slot,
                grid_slot_size=grid_slot_size,
                wall_size=utils.MAP_WALL_SIZE.value,
                wall_color=utils.MAP_WALL_COLOR.value,
                wall_radius=utils.MAP_WALL_RADIUS.value
            ))
