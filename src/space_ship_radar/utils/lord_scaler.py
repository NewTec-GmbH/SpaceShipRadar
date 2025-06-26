"""Converts Pixel-Values into mm

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import numpy as np

# Variables ********************************************************************

# Classes **********************************************************************


class LordScaler:
    """Lord Scaler
        - Responsible for converting pixel values into mm"""

    def __init__(self):
        self._ratio = 1

    def init(self, marker_perimeter: float, real_ar_perimeter: float) -> None:
        """calculates a conversion ratio based on the found markers size

        Args:
            marker_perimeter (float): marker_perimeter size in pixel
            real_ar_perimeter (float): marker_perimeter size in mm
        """
        print(f"in init: {marker_perimeter}")
        if marker_perimeter == -1:
            return

        try:
            ratio = np.float64(real_ar_perimeter) / \
                np.float64(marker_perimeter)
        except ZeroDivisionError:
            ratio = 1
        self._ratio = ratio

    def convert(self, num: float) -> int:
        """converts pixel values into mm values

        Args:
            num (float): pixel number to convert to mm-value

        Returns:
            int: converted mm-value
        """

        mm_value = round(self._ratio * num, 0)
        return int(mm_value)

    @property
    def ratio(self) -> float:
        """getter for the conversion ratio"""
        return self._ratio

# Functions ********************************************************************

# Main *************************************************************************
