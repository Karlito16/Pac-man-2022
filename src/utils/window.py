#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from __future__ import annotations
import src.utils as utils
from typing import Callable, Generator
import pygame


def calculate_grid_dimensions(grid_size: tuple[int, int]) -> tuple[int, int, int]:
    """Function calculates the size of the grid as well as the size of one grid slot."""
    n_horizontal, n_vertical = grid_size
    total_win_height = utils.WIN_HEIGHT.value
    grid_height = total_win_height * (1 - (utils.MAP_MARGIN_TOP_PERCENTAGE.value + utils.MAP_MARGIN_BOTTOM_PERCENTAGE.value))
    grid_slot_size = grid_height // n_vertical
    grid_height = grid_slot_size * n_vertical   # cuts off the bottom map remainder
    grid_width = n_horizontal * grid_slot_size
    return grid_width, grid_height, grid_slot_size


def scale_image(img: pygame.Surface, relevant_size: float = None, angle: float = None, smoothscale: bool = True) -> pygame.Surface:
    """Scales the image object to the relevant size."""
    current_size = img.get_size()[0]
    # smoothscale function uses real size value, whereas rotozoom uses percentage of the given size
    # rotozoom is bad! -> using rotate instead!
    size = relevant_size if smoothscale and relevant_size else relevant_size / current_size if relevant_size else current_size
    func, *args = (pygame.transform.smoothscale, img, (size, size)) if smoothscale else (pygame.transform.rotate, img, angle)
    return func(*args)


def scale_images(*args: pygame.Surface, relevant_size: float = None, angle: float = None, smoothscale: bool = True) -> Generator[pygame.Surface]:
    """Same as scale_image function."""
    for img in args:
        yield scale_image(img=img, relevant_size=relevant_size, angle=angle, smoothscale=smoothscale)


def rotate_images(*args: pygame.Surface, angle: float, relevant_size: float = None) -> Generator[pygame.Surface]:
    """Rotates the given pygame surfaces for given angle value."""
    return scale_images(*args, relevant_size=relevant_size, angle=angle, smoothscale=False)


def get_trajectory(start_point: tuple[float, float], end_point: tuple[float, float]) -> Callable:
    """Method calculates parabolic function which will represent path from the start point to the end point."""
    # f(x) = ax^2
    delta_i = end_point[0] - start_point[0]
    delta_j = end_point[1] - start_point[0]
    a = delta_j / pow(delta_i, 2)
    return lambda x: a * pow(x, 2)


def get_direction(point_1: tuple[float, float], point_2: tuple[float, float]) -> utils.Directions:
    """Returns orientation from point_1 to point_2: positive if point_1.x < point_2.x, negative otherwise"""
    return utils.Directions.RIGHT if point_1[0] < point_2[0] else utils.Directions.LEFT
