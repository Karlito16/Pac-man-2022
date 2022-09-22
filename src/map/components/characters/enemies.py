#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from __future__ import annotations

from .character import Character
from .character_type import CharacterType
from .enemy_type import EnemyType
from ..elementary import MapParticles, NodeType
import src.utils as utils
import src.utils.path as path

from typing import TYPE_CHECKING
import pygame
import random

if TYPE_CHECKING:
    from .. import EnemyBox


class Enemies(pygame.sprite.Group):
    """Enemies class."""

    class Enemy(Character):
        """Enemy class."""

        def __init__(self, starting_node: MapParticles.BigNode, enemy_out_node: MapParticles.BigNode, type_: EnemyType):
            """Constructor."""
            self._enemy_out_node = enemy_out_node
            self._type = type_
            super().__init__(
                starting_node=starting_node,
                character_type=CharacterType.ENEMY,
                moving_speed_percentage=utils.CHARACTER_MOVING_SPEED_PERCENTAGE.value
            )
            self.moving = False
            self.moving_direction = utils.Directions.UNDEFINED
            self._moving_path = list()

        @property
        def enemy_out_node(self) -> MapParticles.BigNode:
            """Getter."""
            return self._enemy_out_node

        @property
        def type(self) -> EnemyType:
            """Getter."""
            return self._type

        @property
        def moving_path(self) -> list[MapParticles.BigNode]:
            """Returns the moving path."""
            return self._moving_path

        def _in_box(self) -> bool:
            """Returns True if enemy is in the enemy box."""
            return self.current_node.type == NodeType.ENEMY_IN

        def _exit_box(self) -> None:
            """Enemy exits the box."""
            self._goto(node=self._enemy_out_node)
            return

        def _goto(self, node: MapParticles.Node) -> None:
            """Sets the enemy path from starting node to the given node."""
            pass
            """Go-to method. Sets the enemy path."""
            self._moving_path = path.Path.find_shortest(from_node=self.current_node, to_node=node)
            if not self._moving_path:   # case when distance node is very close, inside two big nodes
                self.moving_direction = utils.Particle.get_direction(particle1=self.current_node, particle2=node)
            return None

        def unleash(self) -> None:
            """Unleashes the enemy."""
            if self._in_box():
                self._exit_box()
            self.moving = True
            return None

        def _get_next_random_direction(self) -> utils.Directions:
            """Returns the next random direction."""
            # avoid returning back to the box
            possible_neighbours = self.current_node.big_neighbours
            preferable_neighbours = list()
            not_preferable_direction = utils.Directions.get_opposite(direction=self.moving_direction)
            for direction in possible_neighbours:
                if direction == not_preferable_direction:   # avoid returning back
                    continue
                neighbour = possible_neighbours[direction]
                if neighbour and neighbour.node.type != NodeType.GATE:  # avoid returning back to the box
                    preferable_neighbours.append(neighbour)
            if preferable_neighbours:
                return utils.Particle.get_direction(
                    particle1=self.current_node,
                    particle2=random.choice(preferable_neighbours).node
                )
            return utils.Particle.get_direction(
                    particle1=self.current_node,
                    particle2=random.choice(list(possible_neighbours.get_all()))
                )

        def set_future_node(self) -> None:
            """Overrides in Character."""
            super().set_future_node()
            self.moving = True
            return None

        def intersection(self) -> None:
            """Overrides in Character."""
            if self.current_node in self._moving_path:
                self._moving_path = self._moving_path[self._moving_path.index(self.current_node) + 1:]
                if self._moving_path:
                    self.moving_direction = utils.Particle.get_direction(particle1=self.current_node, particle2=self._moving_path[0])
                    return None
            self.moving_direction = self._get_next_random_direction()
            return None

        def move(self) -> None:
            """Overrides in Character."""
            if self.moving:
                super().move()
            return None

    def __init__(self, enemy_out_node: MapParticles.BigNode, enemy_box: EnemyBox):
        """Contructor."""
        self._enemy_out_node = enemy_out_node
        self._enemy_box = enemy_box
        super().__init__()

        for starting_node, enemy_type in zip([self._enemy_out_node] + self._enemy_box, [EnemyType.SHADOW, EnemyType.POKEY, EnemyType.SPEEDY, EnemyType.BASHFUL]):
            self.add(Enemies.Enemy(starting_node=starting_node, enemy_out_node=self._enemy_out_node, type_=enemy_type))

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
