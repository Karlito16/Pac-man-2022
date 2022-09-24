#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević
# filename: pacman.py
# created: 2022-09-04 20:39


from __future__ import annotations

import src.map as map_
import src.utils as utils

from enum import Enum, auto, unique
from typing import Generator
import pygame


@unique
class _GameState(Enum):
    """Game status enum."""

    NORMAL = auto()
    PACMAN_DIE = auto()
    PACMAN_CATCHING = auto()
    ENEMY_DIE = auto()

    def _is_x(self, state: _GameState) -> bool:
        """Global state getter."""
        return self == state

    def is_normal(self) -> bool:
        """Getter."""
        return self._is_x(state=_GameState.NORMAL)

    def is_pacman_die(self) -> bool:
        """Getter."""
        return self._is_x(state=_GameState.PACMAN_DIE)

    def is_pacman_catching(self) -> bool:
        """Getter."""
        return self._is_x(state=_GameState.PACMAN_CATCHING)

    def is_enemy_die(self) -> bool:
        """Getter."""
        return self._is_x(state=_GameState.ENEMY_DIE)


class Pacman(utils.Game):
    """Main class."""

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        """Constructor. Initiliazes the game parameters."""
        super().__init__(screen, clock)
        self._game_state = None
        self._maps = map_.load_maps()

        self._current_map = next(self._maps)   # TODO: Temp solution!

    @property
    def current_map(self) -> map_.Map:
        """Getter."""
        return self._current_map

    def mainloop(self) -> None:
        """Main game loop."""
        self._game_state = _GameState.NORMAL
        self.game_running = True
        while self.game_running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key in utils.CHARACTER_MOVING_KEYS.value:
                        self._current_map.pacman.moving_direction = utils.Directions.get_direction_by_keypress(key=event.key)
                elif event.type in utils.CustomEvents.events():
                    utils.CustomEvents.process(event_type=event.type)

            # Updating game stats
            if self._check_collisions():
                if self._game_state.is_normal():
                    self._on_pacman_death_generator = self._on_pacman_death()
                    next(self._on_pacman_death_generator)
                elif self._game_state.is_pacman_catching():
                    self._on_enemy_death()

            # Screen update
            self._current_map.update()
            self._current_map.draw(surface=self.screen)

            pygame.display.update()
            self.clock.tick(utils.FPS_RATE.value)

        return None

    def _check_collisions(self) -> bool:
        """Method checks characters collisions."""
        if pygame.sprite.spritecollideany(sprite=self._current_map.pacman, group=self._current_map.enemies):
            return True
        return False

    def _on_pacman_death(self) -> Generator:
        """Method is called when Pacman gets caught."""
        self._game_state = _GameState.PACMAN_DIE
        self._freeze_all_characters()
        utils.CustomEvents.new(
            interval=utils.CHARACTER_DEATH_GAME_PAUSE_INTERVAL.value,
            callback_function=lambda: next(self._on_pacman_death_generator),
            loops=1
        )
        yield   # continues after <interval> break
        self._current_map.enemies.hide_all()
        self._current_map.pacman.die(callback_function=lambda: next(self._on_pacman_death_generator))
        yield
        self._current_map.pacman.hidden = True
        utils.CustomEvents.new(
            interval=utils.CHARACTER_DEATH_GAME_PAUSE_INTERVAL.value,
            callback_function=lambda: next(self._on_pacman_death_generator),
            loops=1
        )
        yield
        self._respawn_all_characters()
        self._current_map.pacman.moving = False
        utils.CustomEvents.new(
            interval=utils.RESUME_GAME_INTERVAL.value,
            callback_function=lambda: next(self._on_pacman_death_generator),
            loops=1
        )
        yield
        # Continues with game, and game sound, if pacman have some left lives, else display some menu...
        self._current_map.pacman.moving = True
        self._game_state = _GameState.NORMAL
        yield

    def _on_enemy_death(self) -> None:
        """Method is called when Enemy gets caught."""
        self._game_state = _GameState.ENEMY_DIE

        return None

    def _freeze_all_characters(self) -> None:
        """Method freezes all characters."""
        self._current_map.pacman.freezed = True
        self._current_map.enemies.freeze()
        return None

    def _respawn_all_characters(self) -> None:
        """Method respawns all the characters."""
        self._current_map.pacman.respawn()
        self._current_map.enemies.respawn_all()
        return None


def main() -> int:
    """
    Main function.
    :return: None
    """
    pygame.init()
    screen = pygame.display.set_mode((
        utils.WIN_WIDTH.value,
        utils.WIN_HEIGHT.value
    ))
    clock = pygame.time.Clock()

    pacman = Pacman(screen, clock)
    pacman.mainloop()

    return 0


if __name__ == "__main__":
    main()
