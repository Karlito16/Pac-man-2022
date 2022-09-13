#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević

from __future__ import annotations
import src.utils as utils

from typing import Any, Generator
import os
import pygame


def load_map_file(file_name: str, read_binary: bool = False, file_path: str = None) -> str | None:
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


def load_images(directory: str, directory_constraints: list[str, ] = None, wshadow: bool = False) -> Generator[pygame.Surface, ]:
    """Returns loaded images in given directory."""
    directory_constraints = [""] if directory_constraints is None else directory_constraints
    for constraint in directory_constraints:
        constraint = constraint + "_wshadow" if wshadow else constraint
        for img_file in (file_name for file_name in os.listdir(directory) if constraint in file_name):
            yield pygame.image.load(f"{directory}\\{img_file}").convert_alpha()


def import_assets(instance: Any, attr_name: str, directory: str, relevant_size: float = 1.0, directory_constraints: list[str, ] = None, wshadow: bool = False) -> None | ValueError:
    """Imports the assets from given directory."""
    # load the assets images
    loaded_images = list(load_images(directory=directory, directory_constraints=directory_constraints, wshadow=wshadow))
    # check asset number
    if len(loaded_images) < utils.MINIMAL_REQUIRED_ANIMATION_IMAGES.value:
        raise ValueError(f"minimal required amount of animation assets is: {utils.MINIMAL_REQUIRED_ANIMATION_IMAGES.value}\n{directory_constraints}")
    # scale the images
    scaled_images = utils.scale_images(*loaded_images, relevant_size=relevant_size)
    # set attribute
    setattr(instance, attr_name, list(scaled_images))
    return None
