#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from src.map.components.elementary import MapParticles
import src.utils as utils

from typing import Any, Iterable
import pygame


class Walls(pygame.sprite.Group):
    """Walls class."""

    class Wall(pygame.sprite.Sprite):
        """Wall class."""

        _DIRECTION_LINE_POINTS_DICT = {
            utils.Directions.TOP: (lambda rect: (rect.topleft, rect.topright)),
            utils.Directions.RIGHT: (lambda rect: (rect.topright, rect.bottomright)),
            utils.Directions.BOTTOM: (lambda rect: (rect.bottomleft, rect.bottomright)),
            utils.Directions.LEFT: (lambda rect: (rect.topleft, rect.bottomleft))
        }

        def __init__(self, grid_slot: MapParticles.GridSlot, wall_size: int, wall_inside_color: str, wall_border_color: str, wall_radius: int):
            """
            Constructor.
            """
            self._grid_slot = grid_slot
            self._wall_size = wall_size
            self._wall_inside_color = wall_inside_color
            self._wall_border_color = wall_border_color
            self._wall_radius = wall_radius
            super().__init__()
            self.image, self.rect = self._init_wall()
            self.rect.topleft = (
                self._grid_slot.size * self._grid_slot.i,
                self._grid_slot.size * self._grid_slot.j
            )

        @property
        def grid_slot(self) -> MapParticles.GridSlot:
            """Getter."""
            return self._grid_slot

        @property
        def wall_size(self) -> int:
            """Getter."""
            return self._wall_size

        @property
        def wall_inside_olor(self) -> str:
            """Getter."""
            return self._wall_inside_color

        @property
        def wall_border_color(self) -> str:
            """Getter."""
            return self._wall_border_color

        @property
        def wall_radius(self) -> int:
            """Getter."""
            return self._wall_radius

        def _init_wall(self) -> tuple[pygame.Surface, pygame.Rect]:
            """Inits the wall surface."""
            surface = pygame.Surface((self._grid_slot.size, self._grid_slot.size))
            surface.fill(self.wall_inside_olor)
            rect = surface.get_rect()
            rect.inflate_ip(-1, -1)
            for direction in (direction for direction in utils.Directions if direction != utils.Directions.UNDEFINED):
                neighbour = self._grid_slot.neighbours.get(direction=direction)
                if (not neighbour and direction in (utils.Directions.TOP, utils.Directions.BOTTOM)) or (neighbour and neighbour.is_path()):
                    pygame.draw.line(
                        surface,
                        self.wall_border_color,
                        *Walls.Wall._DIRECTION_LINE_POINTS_DICT[direction](rect=rect),
                        width=self.wall_size
                    )
            return surface, rect

        def update(self, *args: Any, **kwargs: Any) -> None:
            """Overrides the method in sprite class."""
            pass

    def __init__(self, grid_slots_wall: Iterable[MapParticles.GridSlot]):
        """
        Constructor.
        """
        self._grid_slots_wall = grid_slots_wall
        super().__init__()
        for grid_slot in self._grid_slots_wall:
            self.add(Walls.Wall(
                grid_slot=grid_slot,
                wall_size=utils.MAP_WALL_SIZE.value,
                wall_inside_color=utils.MAP_WALL_INSIDE_COLOR.value,
                wall_border_color=utils.MAP_WALL_BORDER_COLOR.value,
                wall_radius=utils.MAP_WALL_RADIUS.value
            ))
