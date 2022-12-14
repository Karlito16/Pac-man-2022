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

from copy import copy
from typing import TYPE_CHECKING, Any, List
import pygame
import random

if TYPE_CHECKING:
    from .. import EnemyBox


class Enemies(pygame.sprite.Group):
    """Enemies class."""

    class Enemy(Character):
        """Enemy class."""

        def __init__(self, name: str, starting_node: MapParticles.BigNode, enemy_out_node: MapParticles.BigNode, type_: EnemyType):
            """Constructor."""
            self._name = name
            self._enemy_out_node = enemy_out_node
            self._type = type_
            super().__init__(
                name=self._name,
                starting_node=starting_node,
                character_type=CharacterType.ENEMY,
                moving_speed_percentage=utils.CHARACTER_ENEMY_MOVING_SPEED_PERCENTAGE.value,
                body_assets_dir=utils.CHARACTERS_ENEMY_BODY_DIR.value
            )

            self._reinit()

            # self._body_color = pygame.Surface(self.image.get_size()).convert_alpha()
            self._init_eye_assets()

        def _init_eye_assets(self) -> None:
            """Method loads the eyes and stores them into the dictionary."""
            self._eye_assets = dict()
            for direction in utils.Directions:
                self._eye_assets[direction] = utils.scale_image(
                    img=next(
                        utils.load_images(
                            directory=utils.CHARACTERS_ENEMY_EYES_DIR.value,
                            directory_constraints=[direction.name.lower()]
                        )
                    ),
                    relevant_size=self.relevant_size
                )
            return None

        def _reinit(self) -> None:
            """Overrides in Characters."""
            super()._reinit()
            self.moving = False
            self.moving_direction = utils.Directions.UNDEFINED
            self._moving_path = list()
            self._is_food = False
            self._dead = False

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

        @property
        def dead(self) -> bool:
            """Getter."""
            return self._dead

        @property
        def moving_direction(self) -> utils.Directions:
            """Getter."""
            return super().moving_direction

        @moving_direction.setter
        def moving_direction(self, other: utils.Directions) -> None:
            """Overrides in Character."""
            super(Enemies.Enemy, self.__class__).moving_direction.fset(self, other)
            if hasattr(self, "_is_food") and self._is_food:
                self.current_animation_assets_attr_name = utils.CHARACTER_ANIMATION_IMAGES_ATTR_NAMES.value[utils.CHARACTER_DEATH_KEYWORD.value]

        @property
        def body_color(self) -> tuple:
            """Overrides in Character."""
            return utils.CHARACTER_ENEMY_NAMES.value[self._name] if not self._is_food else utils.CHARACTER_DEATH_COLOR.value

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

        def die(self, *args, **kwargs) -> None:
            """Method is called when Pacman eats the Enemy while having boost mode on."""
            self._dead = True
            return None

        def become_food(self) -> None:
            """Turns the enemy into a food."""
            self._is_food = True
            self.moving_speed_percentage = utils.CHARACTER_ENEMY_AS_FOOD_MOVING_SPEED_PERCENTAGE.value
            return None

        def become_ordinary(self) -> None:
            """Turns the enemy back as enemy."""
            self._is_food = False
            self._dead = False
            self.moving_speed_percentage = utils.CHARACTER_ENEMY_MOVING_SPEED_PERCENTAGE.value
            return None

        def run_back_into_the_box(self) -> None:
            """Method is called when Enemy gets eaten."""
            self.respawn()
            self.unleash()
            self.become_ordinary()
            self._dead = True
            # self.become_food()  # TODO: Solve the case when enemies becomes ordinary just as this enemy runs back into the box
            return None

        def update(self, *args: Any, **kwargs: Any) -> None:
            """Overrides in Character."""
            super().update()

            # update body color
            # image_cpy = copy(self.image)
            # self._body_color.fill(utils.CHARACTER_ENEMY_NAMES.value[self._name] if not self._is_food else utils.CHARACTER_DEATH_COLOR.value)
            # image_cpy.blit(self._body_color, self._body_color.get_rect(), special_flags=pygame.BLEND_RGBA_ADD)

            return None

        def update_body_color(self) -> pygame.Surface:
            """Overrides in Character."""
            image_cpy = super().update_body_color()

            # update the eyes
            eyes = self._eye_assets[self.moving_direction]
            image_cpy.blit(eyes, eyes.get_rect())
            return image_cpy

    def __init__(self, enemy_out_node: MapParticles.BigNode, enemy_box: EnemyBox):
        """Contructor."""
        self._enemy_out_node = enemy_out_node
        self._enemy_box = enemy_box
        super().__init__()
        self._enemies_ordered = list()

        for starting_node, enemy_type in zip([self._enemy_out_node] + self._enemy_box, [EnemyType.SHADOW, EnemyType.POKEY, EnemyType.SPEEDY, EnemyType.BASHFUL]):
            enemy = Enemies.Enemy(
                name=enemy_type.value,
                starting_node=starting_node,
                enemy_out_node=self._enemy_out_node,
                type_=enemy_type
            )
            self._enemies_ordered.append(enemy)
            self.add(enemy)

        self._reinit()

    def _reinit(self) -> None:
        """Reinit method. Usually called when respawning all the enemies."""
        self._index = 0
        if hasattr(self, "_unleashing_event"):
            utils.CustomEvents.delete(event=self._unleashing_event)
        self._unleashing_event = utils.CustomEvents.new(
            interval=utils.CHARACTER_ENEMY_START_MOVING_INTERVAL.value,
            callback_function=self._unleash,
            loops=utils.CHARACTER_NUM_OF_ENEMIES.value
        )
        return None

    def __next__(self) -> pygame.sprite.Sprite:
        """Next."""
        if self._index >= len(self._enemies_ordered):
            raise StopIteration
        ret_val = self._enemies_ordered[self._index]
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
        if enemy:
            enemy.unleash()
        return None

    def freeze(self) -> None:
        """Freezes the enemies."""
        for enemy in self:
            enemy.freezed = True
        return None

    def unfreeze(self) -> None:
        """Unfreezes the enemies."""
        for enemy in self:
            enemy.freezed = False
        return None

    def hide_all(self) -> None:
        """Hides all enemies."""
        for enemy in self:
            enemy.hidden = True
        return None

    def show_all(self) -> None:
        """Opposite from hide_all method."""
        for enemy in self:
            enemy.hidden = False
        return None

    def respawn_all(self) -> None:
        """Respawns all the enemies."""
        for enemy in self:
            enemy.respawn()
        self._reinit()
        return None

    def become_food_all(self) -> None:
        """Method is called when Pacman eats the super coin."""
        for enemy in self:
            enemy.become_food()

    def become_ordinary_all(self) -> None:
        """Method is called when Pacman eats the super coin."""
        for enemy in self:
            enemy.become_ordinary()

    def draw(self, surface: pygame.Surface) -> List[pygame.Rect]:
        """Overrides in SpriteGroup."""
        temp_removed = [enemy for enemy in self if enemy.hidden]
        self.remove(*temp_removed)
        ret_val = super().draw(surface)
        self.add(*temp_removed)
        return ret_val
