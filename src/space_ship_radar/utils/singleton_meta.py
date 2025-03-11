"""Singleton Meta

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# source: https://refactoring.guru/design-patterns/singleton/python/example


# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

# Variables ********************************************************************

# Classes **********************************************************************


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

# Functions ********************************************************************

# Main *************************************************************************
