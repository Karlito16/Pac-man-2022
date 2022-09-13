#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


from typing import Any, TYPE_CHECKING
# if TYPE_CHECKING:
from src.utils import Particle


class ParticleContainer(list):
    """Particle container list."""

    def __init__(self, particle_instance: Any):
        """Constructor."""
        self._particle_instance = particle_instance
        super().__init__()

    def __contains__(self, particle: Particle) -> bool:
        """
        Checks if container contains given item.
        It is important for the particle_instance class that it implements __eq__ dunder method!
        :param particle: item that we want to find ::particle_instance
        :return: bool
        """
        if self.__instancecheck__(instance=particle):
            for particle_ in self:
                if particle == particle_:
                    return True
            return False

    def __instancecheck__(self, instance: object) -> bool:
        """Checks if given instance is instance of the particle_instance"""
        return isinstance(instance, self._particle_instance)

    def __setitem__(self, key: int, value: Particle) -> PermissionError:
        """Disables any changes to the original container."""
        raise PermissionError(f"you do not have permission to edit this object: {type(self)}")

    def add(self, *args: Particle) -> bool:
        """Adds the given particle/s to the container."""
        status = True
        for particle_ in list(args):
            if self.__instancecheck__(instance=particle_) and not self.__contains__(particle=particle_):
                self.append(particle_)
            else:
                status = False
        return status
