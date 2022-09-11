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


def get_trajectory(start_point: tuple, end_point: tuple):
    """Method calculates parabolic function which will represent path from the start point to the end point."""
    # f(x) = ax^2
    delta_i = end_point[0] - start_point[0]
    delta_j = end_point[1] - start_point[0]
    a = delta_j / pow(delta_i, 2)
    return lambda x: a * pow(x, 2)


def get_direction(point_1: tuple, point_2: tuple):
    """Returns orientation from point_1 to point_2: positive if point_1.x < point_2.x, negative otherwise"""
    return utils.Directions.RIGHT if point_1[0] < point_2[0] else utils.Directions.LEFT
