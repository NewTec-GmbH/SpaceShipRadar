"""Helper Functions

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import numpy as np

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

# Functions ********************************************************************


color_generator = ColorGenerator()


def random_color() -> tuple[int, int, int]:
    """returns a random color"""
    return color_generator.random_color()


# Main *************************************************************************
