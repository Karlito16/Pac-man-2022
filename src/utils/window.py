#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


import src.utils as utils
import pygame


def calculate_grid_dimensions(grid_size: tuple[int, int]) -> tuple[int, int, int]:
    """Function calculates the size of the grid as well as the size of one grid slot."""
    n_horizontal, n_vertical = grid_size
    total_win_height = utils.WIN_HEIGHT.value
    grid_height = total_win_height * (1 - (utils.MAP_MARGIN_TOP_PERCENTAGE.value + utils.MAP_MARGIN_BOTTOM_PERCENTAGE.value))
    grid_slot_size = grid_height // n_vertical
    grid_width = n_horizontal * grid_slot_size
    return grid_width, grid_height, grid_slot_size


def scale_image(img: pygame.Surface, relevant_size: int):
    """Scales the image object to the relevant size."""
    current_size = img.get_size()[0]
    return pygame.transform.rotozoom(img, 0, relevant_size / current_size)


def scale_images(*args: pygame.Surface, relevant_size: int):
    """Same as scale_image function."""
    for img in args:
        yield scale_image(img=img, relevant_size=relevant_size)
