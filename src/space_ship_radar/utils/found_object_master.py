"""Found Object Master

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import math
from typing import Dict
import time

from utils.found_object import FoundObject
from utils.lord_scaler import LordScaler

# Variables ********************************************************************

# Classes **********************************************************************


class FoundObjectMaster:
    """Found Object Master manages multiple Found Objects"""

    def __init__(self):
        self.found_objects: Dict[int, FoundObject] = {}
        self.last_speed_calculation_time = time.time()

        self.lord_scaler = LordScaler()

    @staticmethod
    def angle_difference(alpha: float, beta: float) -> float:
        """calculates the shortest difference between two angles

        Args:
            alpha (float): first angle in mrad
            beta (float): second angle in mrad

        Returns:
            float: shortest difference (- clock-wise)
        """

        diff = beta - alpha
        if abs(diff) > 1000*math.pi:
            diff = abs(diff) - 2000*math.pi
        return diff

    def update_list(self, props: dict[int, FoundObject]) -> None:
        """updates found_objects

        Args:
            props (dict[int, FoundObject]): new found objects
        """
        # scale coordinates
        for identifier, found_object in props.items():
            r_x = self.lord_scaler.convert(found_object.position_x)
            r_y = self.lord_scaler.convert(found_object.position_y)

            found_object.position_x = r_x
            found_object.position_y = r_y

            # pylint: disable=unsubscriptable-object
            # pylint: disable=unsupported-membership-test
            if identifier in self.found_objects:
                # speed
                x_diff = found_object.position_x - \
                    self.found_objects[identifier].position_x
                y_diff = found_object.position_y - \
                    self.found_objects[identifier].position_y

                time_diff = time.time() - self.last_speed_calculation_time

                found_object.speed_x = 0 if time_diff == 0 else round(
                    x_diff / time_diff, 2)
                found_object.speed_y = 0 if time_diff == 0 else round(
                    y_diff / time_diff, 2)

                # rotation
                previous_angle = self.found_objects[identifier].angle
                new_angle = found_object.angle

                angle_difference = self.angle_difference(
                    previous_angle, new_angle)

                found_object.angle = previous_angle + angle_difference

            self.found_objects[identifier] = found_object
        self.last_speed_calculation_time = time.time()

# Functions ********************************************************************

# Main *************************************************************************
