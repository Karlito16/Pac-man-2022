#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from __future__ import annotations

from src.map.components.elementary import MapParticles
from src.map.components.elementary import Nodes
import src.map.components as components
from .map_parser import MapParser
import src.utils as utils
import src.utils.path as path

import pygame
from typing import Generator, Iterable


class Map(pygame.Surface):
    """
    Map class.
    """

    def __init__(self, name: str, size: tuple[int, int], nodes: Nodes, grid_slots_wall: Iterable[MapParticles.GridSlot]):
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
        self._enemy_box = components.EnemyBox(enemy_in_nodes=self._nodes.get_all_by_type(components.elementary.NodeType.ENEMY_IN))
        self._food = components.FoodGroup(
            food_nodes=nodes.get_all_by_type(
                components.elementary.NodeType.REGULAR,
                components.elementary.NodeType.SUPER
            )
        )

        self._passages = components.Passages(
            passage_nodes=self._nodes.get_all_by_type(components.elementary.NodeType.PASSAGE),
            all_nodes=self._nodes       # updates the self._nodes with bridges!
        )
        path.Path.init_nodes(nodes=self._nodes)  # important!

        self._pacman = components.Pacman(starting_node=next(self._nodes.get_all_by_type(components.elementary.NodeType.PACMAN)))
        self._pacman_group = pygame.sprite.GroupSingle(self._pacman)
        self._enemies = components.Enemies(
            enemy_out_node=next(self._nodes.get_all_by_type(components.elementary.NodeType.ENEMY_OUT)),
            enemy_box=self._enemy_box
        )

    @property
    def name(self) -> str:
        """Getter."""
        return self._name

    @property
    def size(self) -> tuple[int, int]:
        """Getter."""
        return self._size

    @property
    def nodes(self) -> Nodes:
        """Getter."""
        return self._nodes

    @property
    def walls(self) -> components.Walls:
        """Getter."""
        return self._walls

    @property
    def enemy_box(self) -> components.EnemyBox:
        """Getter."""
        return self._enemy_box

    @property
    def food(self) -> components.FoodGroup:
        """Getter."""
        return self._food

    @property
    def passages(self) -> components.Passages:
        """Getter."""
        return self._passages

    @property
    def pacman(self) -> components.Pacman:
        """Getter."""
        return self._pacman

    @property
    def pacman_group(self) -> pygame.sprite.GroupSingle:
        """Getter."""
        return self._pacman_group

    @property
    def enemies(self) -> components.Enemies:
        """Getter."""
        return self._enemies

    def update(self) -> None:
        """Updates the map."""
        # update
        self.food.update()
        self.pacman_group.update()
        self.enemies.update()
        return None

    def draw(self, surface: pygame.Surface) -> None:
        """Draws the map."""
        self.fill(utils.MAP_BACKGROUND_COLOR.value)
        self.walls.draw(surface=self)
        self.food.draw(surface=self)
        if not self.pacman.hidden:
            self.pacman_group.draw(surface=self)
        self.enemies.draw(surface=self)

        surface.blit(self, self.rect)
        return None


def load_maps() -> Generator[Map, ]:
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
