#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević

from __future__ import annotations

from .coin import Coin
from .food_ import Food
from .food_status import FoodStatus
from .super_coin import SuperCoin
from ..elementary import MapParticles, NodeType, Nodes
import src.utils as utils

from typing import Generator
import pygame
import random


class FoodGroup(pygame.sprite.Group):
    """Food group container."""

    def __init__(self, food_nodes: Nodes[MapParticles.Node, ]):
        """Constructor."""
        self._food_nodes = food_nodes
        super().__init__()
        self._num_of_coins = 0
        for food_node in self._food_nodes.get_all():
            if food_node.type == NodeType.REGULAR:
                class_ = Coin
            else:
                class_ = SuperCoin
            food = class_(node=food_node)
            self._num_of_coins += 1
            self.add(food)

        self._flashing_event = utils.CustomEvents.new(
            interval=utils.FOOD_FLASH_ANIMATION_INTERVAL.value,
            callback_function=self.flash_animation
        )

    @property
    def num_of_coins(self) -> int:
        """Getter."""
        return self._num_of_coins

    def _get_non_active_sprites(self) -> Generator[Food, ]:
        """Method returns all sprites that currently doesn't perform animation."""
        for sprite in self.sprites():
            if not sprite.is_flashing() and not sprite.is_collected():
                yield sprite

    def flash_animation(self) -> None:
        """Method initiate flash animation for randomly selected food objects."""
        non_active_sprites = list(self._get_non_active_sprites())
        amount_of_needed_sprites = len(non_active_sprites) * utils.FOOD_PERCENTAGE_OF_FLASHING_OBJECTS_AT_ONCE.value
        num_of_selected = 0
        while num_of_selected < amount_of_needed_sprites:
            random_sprite = random.choice(non_active_sprites)
            random_sprite.set_flashing()
            non_active_sprites.remove(random_sprite)
            num_of_selected += 1
        return None

    def get_sprite_by_node(self, node: MapParticles.Node | MapParticles.BigNode) -> Food | None:
        """Returns food object that is made of given node."""
        for food in self.sprites():
            if food.node == node:
                return food
        return None
