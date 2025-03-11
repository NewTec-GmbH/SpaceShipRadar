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
    def __init__(self):
        self._ratio = 1

    def init(self, marker_perimeter: int):
        if marker_perimeter == -1:
            return

        # Ar-width
        real_ar_width = cv2.getTrackbarPos("Ar-width", "settings")
        real_ar_perimeter = real_ar_width * 4

        ratio = real_ar_perimeter / marker_perimeter
        self._ratio = ratio

    def convert(self, num: int) -> int:
        """should convert pixel value into mm"""
        return int(round(self._ratio * num, 1))

    @property
    def ratio(self):
        return self._ratio

# Functions ********************************************************************

# Main *************************************************************************
