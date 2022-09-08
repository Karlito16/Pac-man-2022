#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


import src.utils as utils
from .map_parser import MapParser
from src.utils import MapFile


class Map(object):
    """
    Map class.
    """

    def __init__(self, name):
        """
        Constructor.
        """


def load_maps():
    """
    Function loads the game maps.
    :return: (<class 'Map'>)
    """
    for map_name in utils.MAP_NAMES.value:
        file_data = MapFile.load(file_name=map_name)
        parsed_data = MapParser.parse(data=file_data)
        if parsed_data == -1:
            raise TypeError(f"file content invalid:\nfile: {map_name}")
