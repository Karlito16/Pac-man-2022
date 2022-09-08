#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Karlo Dimjašević


class ParticleContainer(list):
    """Particle container list."""

    def __init__(self, particle_instance):
        """Constructor."""
        self._particle_instance = particle_instance
        super().__init__()

    def __contains__(self, particle):
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

    def __instancecheck__(self, instance):
        """Checks if given instance is instance of the particle_instance"""
        return isinstance(instance, self._particle_instance)

    def __setitem__(self, key, value):
        """Disables any changes to the original container."""
        raise PermissionError(f"you do not have permission to edit this object: {type(self)}")

    def add(self, *args):
        """Adds the given particle/s to the container."""
        status = True
        for particle_ in list(args):
            if self.__instancecheck__(instance=particle_) and not self.__contains__(particle=particle_):
                self.append(particle_)
            else:
                status = False
        return status
