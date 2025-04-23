"""Converts Pixel-Values into mm

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import cv2

# Variables ********************************************************************

# Classes **********************************************************************


class LordScaler:
    """Lord Scaler
        - Responsible for converting pixel values into mm"""

    def __init__(self):
        self._ratio = 1

    def init(self, marker_perimeter: int) -> None:
        """calculates a conversion ratio based on the found markers size"""
        if marker_perimeter == -1:
            return

        # ArUco-width
        real_ar_width = cv2.getTrackbarPos("ArUco-width", "settings")
        real_ar_perimeter = real_ar_width * 4

        try:
            ratio = real_ar_perimeter / marker_perimeter
        except ZeroDivisionError:
            ratio = 1
        self._ratio = ratio

    def convert(self, num: int) -> int:
        """should convert pixel value into mm"""
        return int(round(self._ratio * num, 1))

    @property
    def ratio(self) -> float:
        """getter for the conversion ratio"""
        return self._ratio

# Functions ********************************************************************

# Main *************************************************************************
