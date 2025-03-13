"""Found Object

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import time

from utils import helper

# Variables ********************************************************************

# Classes **********************************************************************


class FoundObject:
    """Found Object"""

    def __init__(self, identifier_number: int, start_point: tuple[int, int, int, int], angle):
        self.color = helper.random_color()
        self._identifier_number: int = identifier_number
        self.current_position = start_point  # format (x, y, w, h)
        self.angle = angle

        self._previous_center_point = None  # used for speed calculation
        self._previous_speed = (0, 0)
        self._last_call_time = None

    @property
    def identifier_number(self) -> int:
        """getter for identifier number"""
        return self._identifier_number

    def get_newest_point(self) -> tuple[int, int]:
        """returns the newest point of this Found Object"""
        x, y, w, h = self.current_position
        point = (x+w/2, y+h/2)
        return point

    def get_speed(self) -> tuple[int, int]:
        """getter for current speed"""
        return self.__calculate_speed()

    def _update_position(self, x: int, y: int, w: int, h: int):
        """updates the x, y, width, and height values"""
        self.current_position = (x, y, w, h)

    def __calculate_speed(self) -> tuple[int, int]:
        """calculates the speed based on the previous points"""
        # points = np.array(self.previous_points, dtype=np.int32)
        if self._check_time():
            self._previous_speed = self._speed()
        return self._previous_speed

    def _speed(self):
        """returns the position difference between last call"""
        if self._previous_center_point is None:
            self._previous_center_point = self.get_newest_point()
            return (0, 0)

        last_x, last_y = self._previous_center_point
        new_x, new_y = self.get_newest_point()
        speed = (int(new_x-last_x), int(new_y-last_y))
        self._previous_speed = speed
        self._previous_center_point = (new_x, new_y)
        return speed

    def _check_time(self) -> bool:
        """check if 1 second has passed

        Returns:
            bool: True if more than 1s has passed
                    else: False 
        """
        current_time = time.time()

        if self._last_call_time is None:
            self._last_call_time = current_time
            return False

        elapsed_time = current_time - self._last_call_time

        if elapsed_time > 1:
            self._last_call_time = current_time
            return True
        else:
            return False

    def update(self, x, y, w, h, angle):
        """updates the position and angle of this object

        Args:
            x (int): top left corner of object x position
            y (int): top left corner of object y postion
            w (int): width of object
            h (int): height of object
            angle (int): angle of the object
        """
        self._update_position(x, y, w, h)
        self.angle = angle


# Functions ********************************************************************

# Main *************************************************************************
