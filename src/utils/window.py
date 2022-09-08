#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


import src.utils as utils


def calculate_map_dimensions(grid_size: tuple[int, int]) -> tuple[int, int, int]:
    """Function calculates the size of the map aswell as the size of the one grid slot."""
    n_horizontal, n_vertical = grid_size
    total_win_height = utils.WIN_HEIGHT.value
    map_height = total_win_height * (1 - (utils.MAP_MARGIN_TOP_PERCENTAGE.value + utils.MAP_MARGIN_BOTTOM_PERCENTAGE.value))
    grid_slot_size = map_height // n_vertical
    map_width = n_horizontal * grid_slot_size
    return map_width, map_height, grid_slot_size
