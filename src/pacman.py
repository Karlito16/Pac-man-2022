#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević
# filename: pacman.py
# created: 2022-09-04 20:39


from __future__ import annotations

import src.map as map_
import src.screens as screens
import src.utils as utils

from typing import TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from src.map import Map


class PacmanApp(utils.App):
    """Main class."""

    def __init__(self, window: pygame.Surface, clock: pygame.time.Clock):
        """Constructor. Initiliazes the app parameters."""
        super().__init__(window, clock)
        self._maps = list(map_.load_maps())     # see how to improve performance with pure Generator

        # screen init
        main_menu_screen = screens.MainMenuScreen()
        game_screen = screens.GameScreen(current_map=self._maps[1])  # TODO: Temp solution for current map!
        self._screen_manager = screens.ScreenManager(game_screen, main_menu_screen)

    @property
    def maps(self) -> list[Map]:
        """Getter,"""
        return self._maps

    def mainloop(self) -> None:
        """Main app loop."""
        self.app_running = True
        while self.app_running:
            # Event handling - terminate case - equal for all screens
            self.catch_new_app_events()
            for event in self.app_events:
                if event.type == pygame.QUIT:
                    self.terminate()

            self._screen_manager.update_active_screen(window=self.window, events=self.app_events)

            pygame.display.update()
            self.clock.tick(utils.FPS_RATE.value)

        return None


def main() -> int:
    """
    Main function.
    :return: None
    """
    pygame.init()
    window = pygame.display.set_mode((
        utils.WIN_WIDTH.value,
        utils.WIN_HEIGHT.value
    ))
    clock = pygame.time.Clock()

    pacman = PacmanApp(window, clock)
    pacman.mainloop()

    return 0


if __name__ == "__main__":
    main()
