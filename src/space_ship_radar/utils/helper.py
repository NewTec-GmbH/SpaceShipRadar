"""Helper Functions

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import numpy as np
from numba import jit

# Variables ********************************************************************

# Classes **********************************************************************


class ColorGenerator:
    """Manages random colors"""

    def __init__(self):
        self.previous_colors = []

    def random_color(self):
        """returns a random color which is different from the previous random colors"""

        new_color: np.ndarray = np.random.randint(50, 200, (1, 3))[0]

        # Check for maximum distance from previous colors
        i: int = -1
        while self.previous_colors:
            i += 1
            distances = [np.linalg.norm(new_color - np.array(color))
                         for color in self.previous_colors]
            if min(distances) < 100 and i < 3:
                new_color = np.random.randint(0, 200, (1, 3))[
                    0]  # Regenerate if too close
            else:
                break

        # Store the new color
        self.previous_colors.append(new_color.tolist())

        return new_color.tolist()

    def foos(self):
        """this function exists to make pylint happy"""

# Functions ********************************************************************


color_generator = ColorGenerator()


def random_color() -> tuple[int, int, int]:
    """returns a random color"""
    return color_generator.random_color()


@jit
def calculate_speed(points: np.ndarray) -> tuple[int, int]:
    """calculates the speed based on previous points"""
    if len(points) < 2:
        return (0, 0)  # Not enough points to calculate speed

    # Calculate differences in x and y coordinates
    dx = np.empty(len(points) - 1, dtype=np.int32)
    dy = np.empty(len(points) - 1, dtype=np.int32)

    for i in range(1, len(points)):
        dx[i - 1] = points[i][0] - points[i - 1][0]
        dy[i - 1] = points[i][1] - points[i - 1][1]

    # Calculate median of differences using np.median
    median_dx = int(np.median(dx))
    median_dy = int(np.median(dy))

    return (median_dx, median_dy)


# Main *************************************************************************
