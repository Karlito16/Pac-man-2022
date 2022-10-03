#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from __future__ import annotations

import src.utils as utils
from .screen import Screen

from enum import auto, unique, Enum
from typing import Generator, TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from src.map import Map


@unique
class _GameState(Enum):
    """Game status enum."""

    NORMAL = auto()
    PACMAN_DIE = auto()
    PACMAN_CATCHING = auto()
    PACMAN_CATCHING_ENDING = auto()
    ENEMY_DIE = auto()
    ENDING = auto()
    END = auto()

    def _is_x(self, state: _GameState) -> bool:
        """Global state getter."""
        return self.value == state.value

    def is_normal(self) -> bool:
        """Getter."""
        return self._is_x(state=_GameState.NORMAL)

    def is_pacman_die(self) -> bool:
        """Getter."""
        return self._is_x(state=_GameState.PACMAN_DIE)

    def is_pacman_catching(self) -> bool:
        """Getter."""
        return self._is_x(state=_GameState.PACMAN_CATCHING)

    def is_pacman_catching_ending(self) -> bool:
        """Getter."""
        return self._is_x(state=_GameState.PACMAN_CATCHING_ENDING)

    def is_enemy_die(self) -> bool:
        """Getter."""
        return self._is_x(state=_GameState.ENEMY_DIE)

    def is_ending(self) -> bool:
        """Getter."""
        return self._is_x(state=_GameState.ENDING)

    def is_end(self) -> bool:
        """Getter."""
        return self._is_x(state=_GameState.END)


class GameScreen(Screen):
    """Constructor."""

    def __init__(self, current_map: Map):
        """Constructor."""
        self._current_map = current_map
        super().__init__()
        self._game_state = _GameState.NORMAL

        # init text
        self._text_color = utils.color_hex_to_tuple(color_hex=utils.COLORS_PACMAN.value)
        # title
        top_win_offset = utils.MAP_MARGIN_TOP_PERCENTAGE.value * utils.WIN_HEIGHT.value
        self._title_font_size = int(top_win_offset * utils.GAME_SCREEN_FONT_PERCENTAGE.value)
        self._title_font = pygame.font.Font(utils.FONT_STYLE.value, self._title_font_size)
        self._title = self._title_font.render("Pac-Man", True, self._text_color)
        self._title_rect = self._title.get_rect()
        self._title_rect.center = utils.WIN_WIDTH.value // 2, top_win_offset // 2

        bottom_win_offset = utils.WIN_HEIGHT.value - top_win_offset - self.current_map.size[1]
        horizontal_win_offset = (utils.WIN_WIDTH.value - self.current_map.size[0]) // 2
        self._info_font_size = int(bottom_win_offset * utils.GAME_SCREEN_FONT_PERCENTAGE.value)
        self._info_font = pygame.font.Font(utils.FONT_STYLE.value, self._info_font_size)

        # lives
        self._lives_rect_tuple = horizontal_win_offset, utils.WIN_HEIGHT.value - bottom_win_offset // 2
        self._update_lives(lives=self.current_map.pacman.lives)

        # score
        self._score_rect_tuple = utils.WIN_WIDTH.value - horizontal_win_offset - self.current_map.size[0] // 2, utils.WIN_HEIGHT.value - bottom_win_offset // 2
        self._update_score()

    @property
    def current_map(self) -> Map:
        """Getter."""
        return self._current_map

    @property
    def name(self) -> str:
        """Overrides in Screen."""
        return utils.GAME_SCREEN.value

    def update(self, events: list[pygame.event.Event]) -> str | None:
        """Overrides in Screen."""
        # Event handling
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in utils.CHARACTER_MOVING_KEYS.value:
                    self._current_map.pacman.moving_direction = utils.Directions.get_direction_by_keypress(
                        key=event.key)
            elif event.type in utils.CustomEvents.events():
                utils.CustomEvents.process(event_type=event.type)

        # Updating game stats
        if self._game_state.is_end():
            return utils.MAIN_MENU_SCREEN.value
        elif self.current_map.pacman.num_of_coins_collected >= self.current_map.food.num_of_coins and not self._game_state.is_ending():
            self._on_ending_generator = self._on_ending()
            next(self._on_ending_generator)
        else:
            if self.current_map.pacman.boosted and not self._game_state.is_pacman_catching():
                self._on_pacman_boost_generator = self._on_pacman_boost()
                next(self._on_pacman_boost_generator)
            self._collided_enemy = self._check_collisions()
            if self._collided_enemy:
                if self._game_state.is_normal():
                    self._on_pacman_death_generator = self._on_pacman_death()
                    next(self._on_pacman_death_generator)
                elif self._game_state.is_pacman_catching() and not self._collided_enemy.dead:
                    self._on_enemy_death_generator = self._on_enemy_death()
                    next(self._on_enemy_death_generator)

        self._update_score()

        # Screen update
        self.fill(utils.MAP_BACKGROUND_COLOR.value)  # clear previous screen state

        self._current_map.update()
        self._current_map.draw(surface=self)

        self.blit(self._title, self._title_rect)
        self.blit(self._lives, self._lives_rect)
        self.blit(self._score, self._score_rect)
        return None

    def _update_score(self) -> None:
        """Updates the score text."""
        score = self.current_map.pacman.score
        self._score = self._info_font.render(f"Score: {score}", True, self._text_color)
        self._score_rect = self._score.get_rect()
        self._score_rect.midleft = self._score_rect_tuple
        return None

    def _update_lives(self, lives: int) -> None:
        """Updates the lives text."""
        self._lives = self._info_font.render(f"Lives: {lives}", True, self._text_color)
        self._lives_rect = self._lives.get_rect()
        self._lives_rect.midleft = self._lives_rect_tuple
        return None

    def _check_collisions(self) -> pygame.sprite.Sprite:
        """Method checks characters collisions."""
        return pygame.sprite.spritecollideany(sprite=self._current_map.pacman, group=self._current_map.enemies)

    def _on_pacman_boost(self) -> Generator:
        """Method is called when Pacman eats super coin."""
        self.current_map.pacman.boosted = False
        self._game_state = _GameState.PACMAN_CATCHING
        self.current_map.enemies.become_food_all()
        utils.CustomEvents.new(
            interval=utils.CHARACTER_PACMAN_BOOST_MAIN_INTERVAL.value,
            callback_function=lambda: next(self._on_pacman_boost_generator),
            loops=1
        )
        yield
        # TODO: Flashing enemy animation
        utils.CustomEvents.new(
            interval=utils.CHARACTER_PACMAN_BOOST_ENDING_INTERVAL.value,
            callback_function=lambda: next(self._on_pacman_boost_generator),
            loops=1
        )
        yield
        self.current_map.enemies.become_ordinary_all()
        self._game_state = _GameState.NORMAL
        yield

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
        self._freeze_all_characters()
        utils.CustomEvents.new(
            interval=utils.RESUME_GAME_INTERVAL.value,
            callback_function=lambda: next(self._on_pacman_death_generator),
            loops=1
        )
        self._update_lives(lives=self.current_map.pacman.lives)
        yield
        # Continues with app, and app sound, if pacman has some left lives, else display some menu...
        self._unfreeze_all_characters()
        self._game_state = _GameState.NORMAL if self.current_map.pacman.lives > 0 else _GameState.END
        yield

    def _on_enemy_death(self) -> Generator:
        """Method is called when Enemy gets caught."""
        # self._game_state = _GameState.ENEMY_DIE
        collided_enemy = self._collided_enemy
        collided_enemy.die()
        self.current_map.pacman.eat_enemy()
        self._freeze_all_characters()
        utils.CustomEvents.new(
            interval=utils.CHARACTER_ENEMY_DEATH_PAUSE_INTERVAL.value,
            callback_function=lambda: next(self._on_enemy_death_generator),
            loops=1
        )
        yield
        self._unfreeze_all_characters()
        collided_enemy.run_back_into_the_box()
        yield

    def _on_ending(self) -> Generator:
        """Method is called when player collects all the coins."""
        self._game_state = _GameState.ENDING
        self._freeze_all_characters()
        utils.CustomEvents.new(
            interval=utils.ENDING_GAME_INTERVAL.value,
            callback_function=lambda: next(self._on_ending_generator),
            loops=1
        )
        yield
        self._game_state = _GameState.END
        yield

    def _freeze_all_characters(self) -> None:
        """Method freezes all characters."""
        self._current_map.pacman.freezed = True
        self._current_map.enemies.freeze()
        return None

    def _unfreeze_all_characters(self) -> None:
        """Method freezes all characters."""
        self._current_map.pacman.freezed = False
        self._current_map.enemies.unfreeze()
        return None

    def _respawn_all_characters(self) -> None:
        """Method respawns all the characters."""
        self._current_map.pacman.respawn()
        self._current_map.enemies.respawn_all()
        return None
