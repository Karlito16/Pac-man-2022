#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević
# filename: pacman.py
# created: 2022-09-04 20:39


import src.map as map_
import src.utils as utils
import pygame


class Pacman(utils.Game):
    """Main class."""

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        """Constructor. Initiliazes the game parameters."""
        super().__init__(screen, clock)
        self._maps = map_.load_maps()

        self._current_map = next(self._maps)   # TODO: Temp solution!

    @property
    def current_map(self) -> map_.Map:
        """Getter."""
        return self._current_map

    def mainloop(self) -> None:
        """Main game loop"""
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
                    utils.CustomEvents.process(event=event.type)

            # Updating game stats

            # Screen update
            self._current_map.update()
            self._current_map.draw(surface=self.screen)

            pygame.display.update()
            self.clock.tick(utils.FPS_RATE.value)

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
