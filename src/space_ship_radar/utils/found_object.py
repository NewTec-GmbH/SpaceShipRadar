"""Found Object

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

from dataclasses import dataclass

# Variables ********************************************************************

# Classes **********************************************************************


@dataclass
class FoundObject:
    """Dataclass used to represent a Found Object"""

    def __init__(self, position, speed, angle):
        position_x, position_y = position
        speed_x, speed_y = speed
        self.position_x = position_x
        self.position_y = position_y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.angle = angle

# Functions ********************************************************************

# Main *************************************************************************
