"""Found Object"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import numpy as np
from utils import helper


# Classes **********************************************************************

class FoundObject:
    """Found Object"""

    def __init__(self, num: int, start_point: tuple[int, int]):
        self.color = helper.random_color()
        self.previous_points = []  # format middle_point
        self.num = num  # unused
        self.current_position = (0, 0, 0, 0)  # format (x, y, w, h)

        if start_point is not None:
            self.previous_points.append(start_point)

    def get_newest_point(self) -> tuple[int, int]:
        """returns the newest point of this Found Object"""
        if len(self.previous_points) < 1:
            return (-1, -1)
        return self.previous_points[len(self.previous_points) - 1]

    def add_previous_point(self, point: tuple[int, int]) -> None:
        """adds a new point. Until a maximum of 3 is reached. 
        If there are more then the oldest point is remove from the list"""
        if len(self.previous_points) >= 4:
            self.previous_points.pop(0)

        self.previous_points.append(point)

    def update_position(self, x: int, y: int, w: int, h: int):
        """updates the x, y, width, and height values"""
        self.current_position = (x, y, w, h)

    def calculate_speed(self) -> tuple[int, int]:
        """calculates the speed based on the previous points"""
        points = np.array(self.previous_points, dtype=np.int32)
        return helper.calculate_speed(points)
