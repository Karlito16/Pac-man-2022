#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from .coin import Coin
from .super_coin import SuperCoin
from .food_status import FoodStatus
from ..elementary.node_type import NodeType
import src.utils as utils
import pygame
import random


class FoodGroup(pygame.sprite.Group):
    """Food group container."""

    def __init__(self, food_nodes):
        """Constructor."""
        self._food_nodes = food_nodes
        super().__init__()
        for food_node in self._food_nodes.get_all():
            if food_node.type == NodeType.REGULAR:
                class_ = Coin
            else:
                class_ = SuperCoin
            self.add(class_(node=food_node))

        self._flashing_event = utils.CustomEvents.new(
            interval=utils.FOOD_FLASH_ANIMATION_INTERVAL.value,
            callback_function=self.flash_animation
        )

    def _get_non_active_sprites(self):
        """Method returns all sprites that currently doesn't perform animation."""
        for sprite in self.sprites():
            if not sprite.is_flashing() and sprite.status != FoodStatus.COLLECTED:
                yield sprite

    def flash_animation(self):
        """Method initiate flash animation for randomly selected food objects."""
        non_active_sprites = list(self._get_non_active_sprites())
        amount_of_needed_sprites = len(non_active_sprites) * utils.FOOD_PERCENTAGE_OF_FLASHING_OBJECTS_AT_ONCE.value
        num_of_selected = 0
        while num_of_selected < amount_of_needed_sprites:
            random_sprite = random.choice(non_active_sprites)
            random_sprite.set_flashing()
            non_active_sprites.remove(random_sprite)
            num_of_selected += 1
