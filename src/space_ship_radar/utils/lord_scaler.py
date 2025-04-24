"""Converts Pixel-Values into mm

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import numpy as np

import cv2

# Variables ********************************************************************

# Classes **********************************************************************
# 984
# 14.5 + 3*297 - 100


class LordScaler:
    """Lord Scaler
        - Responsible for converting pixel values into mm"""

    def __init__(self):
        self._ratio = 1

    def init(self, marker_perimeter: int) -> None:
        """calculates a conversion ratio based on the found markers size"""
        print(f"in init: {marker_perimeter}")
        if marker_perimeter == -1:
            return

        # ArUco-width
        # cv2.getTrackbarPos("ArUco", "settings")  # 96.5
        real_ar_width = 100
        real_ar_perimeter = np.float64(real_ar_width) * 4

        try:
            # marker_perimeter  # 438.03 #
            ratio = np.float64(real_ar_perimeter) / \
                np.float64(marker_perimeter)  # 226.32423210144043 # 226.0

            print(f"ratio: {ratio}")
        except ZeroDivisionError:
            ratio = 1
        self._ratio = ratio

    def convert(self, num: float) -> int:
        """should convert pixel value into mm"""

        # print(f"this num {num}")

        # print(f"self ratio {self._ratio}")
        good_value = round(self._ratio * num, 0)
        # print(f'good_value {good_value}')

        good_value = int(good_value)
        return good_value

    @property
    def ratio(self) -> float:
        """getter for the conversion ratio"""
        return self._ratio

# Functions ********************************************************************

# Main *************************************************************************
