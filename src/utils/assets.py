#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


import src.utils as utils
import pygame
import os


def load_map_file(file_name, read_binary=False, file_path=None):
    """
    Loads the file with given filename.
    Returns the file data.
    :param file_name: name of the file (extension is ignored) ::str
    :param read_binary: reads the file binary if True ::bool
    :param file_path:
    :return: file data ::str
    """
    # file_name = file_name[:file_name.index('.')] if '.' in file_name else file_name
    file_path = file_path if file_path is not None else utils.MAPS_DIR.value
    # file_extension = utils.MAP_FILE_EXTENSION.value
    open_mode = "rb" if read_binary else 'r'

    try:
        with open(f"{file_path}\\{file_name}", mode=open_mode) as f:
            data = f.read()
    except Exception:
        print(f"Exception while loading the file '{file_name}':\n{file_path}\\{file_name}")
        return None
    else:
        return data


def load_images(directory):
    """Returns loaded images in given directory."""
    for img_file in os.listdir(directory):
        yield pygame.image.load(f"{directory}\\{img_file}").convert_alpha()
