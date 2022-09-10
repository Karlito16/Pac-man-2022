#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from .map_parser import MapParser
import src.utils as utils
import src.map.components as components

import pygame
from typing import Any


class Map(pygame.Surface):
    """
    Map class.
    """

    def __init__(self, name, size, nodes, grid_slots_wall):
        """
        Constructor.
        """
        self._name = name
        self._size = size
        self._nodes = nodes

        super().__init__(self._size)
        self.rect = self.get_rect()
        self.rect.midtop = (utils.WIN_WIDTH.value // 2, utils.WIN_HEIGHT.value * utils.MAP_MARGIN_TOP_PERCENTAGE.value)

        self._walls = components.Walls(grid_slots_wall=grid_slots_wall)
        self._food = components.FoodGroup(
            food_nodes=nodes.get_all_by_type(
                components.elementary.NodeType.REGULAR,
                components.elementary.NodeType.SUPER
            )
        )

    @property
    def name(self):
        """Getter."""
        return self._name

    @property
    def size(self):
        """Getter."""
        return self._size

    @property
    def nodes(self):
        """Getter."""
        return self._nodes

    @property
    def walls(self):
        """Getter."""
        return self._walls

    @property
    def food(self):
        """Getter."""
        return self._food

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Overrides the method in sprite class."""
        self.food.update()

    def draw(self, surface):
        """Draws the map."""
        self.walls.draw(surface=self)
        self.food.draw(surface=self)

        surface.blit(self, self.rect)


def load_maps():
    """
    Function loads the game maps.
    :return: (<class 'Map'>)
    """
    for map_name in utils.MAP_NAMES.value:
        file_data = utils.load_map_file(file_name=map_name)
        parsed_data = MapParser.parse(data=file_data)
        if parsed_data == -1:
            raise TypeError(f"file content invalid:\nfile: {map_name}")

        grid_size, nodes, walls = parsed_data
        yield Map(
            name=map_name,
            size=grid_size,
            nodes=nodes,
            grid_slots_wall=walls
        )
