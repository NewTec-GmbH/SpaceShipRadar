"""Found Object Master

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import math
from typing import Dict
from time import perf_counter

from utils.found_object import FoundObject
from utils.lord_scaler import LordScaler

# Variables ********************************************************************

# Classes **********************************************************************


class FoundObjectMaster:
    """Found Object Master manages multiple Found Objects"""

    def __init__(self):
        self.found_objects: Dict[int, FoundObject] = {}
        # self.previous_aruco_list: list[FoundObject] = None
        self.last_speed_calculation_time = perf_counter()

        self.lord_scaler = LordScaler()

    @staticmethod
    def _angle_difference(alpha, beta):
        diff = beta - alpha
        if abs(diff) > 1000*math.pi:
            diff = abs(diff) - 2000*math.pi
        return diff

    def update_list(self, props):
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

                time_diff = perf_counter() - self.last_speed_calculation_time

                found_object.speed_x = round(x_diff / time_diff, 2)
                found_object.speed_y = round(y_diff / time_diff, 2)
                self.last_speed_calculation_time = perf_counter()

                # rotation
                previous_angle = self.found_objects[identifier].angle
                new_angle = found_object.angle

                angle_difference = self._angle_difference(
                    previous_angle, new_angle)

                found_object.angle = previous_angle + angle_difference

            self.found_objects[identifier] = found_object

            # Functions ********************************************************************

            # Main *************************************************************************
