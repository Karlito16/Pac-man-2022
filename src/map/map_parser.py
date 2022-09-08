#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


import src.utils as utils
from .components.elementary import Grid, MapParticles, NodeType


def _safe_evaluation(func):
    def wrapper(*args, **kwargs):
        try:
            evaluated_data = func(*args, **kwargs)
        except SyntaxError as e:
            print(f"Exception during file data evaluation:\n{e.msg}")
            return None
        except TypeError as e:
            print(f"Exception during file data evaluation:\n{e}")
            return None
        else:
            return evaluated_data

    return wrapper


class MapParser(object):
    """Map parser class."""

    def __init__(self):
        """
        Constructor.
        """

    @staticmethod
    @_safe_evaluation
    def _evaluate(string_value):
        return eval(string_value)

    @staticmethod
    def _all_valid(*args):
        """Checks if all arguments are valid and have some value."""
        for arg in args:
            if arg is None:
                return False
        return True

    @staticmethod
    def _parse_row(data_row):
        """Parses the data row and checks it's validity."""
        parsed_data = list()
        for data in data_row:
            parsed_data.append(MapParser._evaluate(data))
        if not MapParser._all_valid(*parsed_data):
            return -1
        return parsed_data

    @staticmethod
    def parse(data):
        """
        Parses the given file data.
        :param data: file data ::str
        :return:
        """
        data_rows = data.split(utils.MAP_FILE_ROW_DELIMITER.value)

        # get the size of the grid, adn create the grid => first row of the file
        grid_size = MapParser._evaluate(string_value=data_rows[0])
        if not MapParser._all_valid(grid_size):
            return -1
        grid = Grid(size=grid_size)

        # parse the other rows
        data_rows = list(map(lambda x: x.strip().split(utils.MAP_FILE_DATA_DELIMITER.value), data_rows))
        for data_row in data_rows[1:-1]:
            # get the data
            parsed_data_row = MapParser._parse_row(data_row=data_row)
            if parsed_data_row == -1:
                return -1

            # unpack valid data values and create BigNodes
            pos_1, pos_2, type_1, type_2 = parsed_data_row
            big_node_1 = grid.create_big_node(*pos_1, type_=NodeType(type_1))
            big_node_2 = grid.create_big_node(*pos_2, type_=NodeType(type_2))

            # create new big connection
            direction = MapParticles.BigNode.get_direction(particle1=big_node_1, particle2=big_node_2)
            MapParticles.BigNode.big_connect(big_node_1=big_node_1, big_node_2=big_node_2, direction_1_2=direction)  # big neighbours

            # create all sub-nodes between two big nodes, with appropriate type
            sub_nodes = grid.create_sub_nodes(from_node=big_node_1, to_node=big_node_2, direction=direction)  # generator

            # set-up little neighbours
            nodes = [big_node_1] + list(sub_nodes) + [big_node_2]
            grid.nodes.neighbourhood(*nodes, direction=direction)

        # collect grid slots that remained as WALLS
        walls = grid.get_all_walls()

        return grid.nodes, walls