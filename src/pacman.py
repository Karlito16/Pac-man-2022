#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević
# filename: pacman.py
# created: 2022-09-04 20:39


import pygame
import src.utils as utils
import src.map as map_


class Pacman(utils.Game):
    """Main class."""

    def __init__(self, screen, clock):
        """Constructor. Initiliazes the game parameters."""
        super().__init__(screen, clock)
        self._maps = map_.load_maps()

    def mainloop(self):
        """Main game loop"""
        while True:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()

            # Updating game stats

            # Screen update
            pygame.display.update()
            self.clock.tick(utils.FPS_RATE.value)


def main():
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


if __name__ == "__main__":
    main()
