#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from __future__ import annotations

from .character import Character
from .character_type import CharacterType
from ..elementary import MapParticles, NodeType
import src.utils as utils

from typing import TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from .. import EnemyBox


class Enemies(pygame.sprite.Group):
    """Enemies class."""

    class Enemy(Character):
        """Enemy class."""

        def __init__(self, starting_node: MapParticles.BigNode, enemy_out_node: MapParticles.BigNode):
            """Constructor."""
            self._enemy_out_node = enemy_out_node
            super().__init__(
                starting_node=starting_node,
                character_type=CharacterType.ENEMY,
                moving_speed_percentage=utils.CHARACTER_MOVING_SPEED_PERCENTAGE.value
            )
            self.moving = False
            self.moving_direction = utils.Directions.UNDEFINED

        @property
        def enemy_out_node(self) -> MapParticles.BigNode:
            """Getter."""
            return self._enemy_out_node

        def _in_box(self) -> bool:
            """Returns True if enemy is in the enemy box."""
            return self.current_node.type == NodeType.ENEMY_IN

        def goto(self, node: MapParticles.BigNode) -> None:
            """Sets the enemy path from starting node to the given node."""
            pass

        def unleash(self) -> None:
            """Unleashes the enemy."""
            # if self._in_box():

    def __init__(self, enemy_out_node: MapParticles.BigNode, enemy_box: EnemyBox):
        """Contructor."""
        self._enemy_out_node = enemy_out_node
        self._enemy_box = enemy_box
        super().__init__()

        for starting_node in [self._enemy_out_node] + self._enemy_box:
            self.add(Enemies.Enemy(starting_node=starting_node, enemy_out_node=self._enemy_out_node))

        utils.CustomEvents.new(
            interval=utils.CHARACTER_ENEMY_START_MOVING_INTERVAL.value,
            callback_function=self._unleash,
            loops=utils.CHARACTER_NUM_OF_ENEMIES.value
        )

    def __iter__(self) -> None:
        """Iter."""
        self._index = 0
        return None

    def __next__(self) -> pygame.sprite.Sprite:
        """Next."""
        if not hasattr(self, "_index"):
            self.__iter__()
        if self._index >= len(self):
            raise StopIteration()
        ret_val = self.sprites()[self._index]
        self._index += 1
        return ret_val

    @property
    def enemy_out_node(self) -> MapParticles.BigNode:
        """Getter."""
        return self._enemy_out_node

    @property
    def enemy_box(self) -> EnemyBox:
        """Getter."""
        return self._enemy_box

    def _unleash(self) -> None:
        """Unleashes the one enemy, triggered by a timer."""
        enemy = next(self)
        enemy.unleash()
        return None
