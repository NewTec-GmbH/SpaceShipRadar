"""Enter short module description here

Enter detailed module description here

Author: Name (mail)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import cv2

# Variables ********************************************************************

# Classes **********************************************************************

# Functions ********************************************************************


def nothing(*_):
    """does nothing"""


def start_settings():
    """
    Create a settings window with the following trackbars:
        - Histogram
        - Gaussian
        - Ar-width
    """

    cv2.namedWindow("settings", cv2.WINDOW_NORMAL)
    cv2.createTrackbar("Histogram", "settings", 50, 100, nothing)
    cv2.createTrackbar("Gaussian", "settings", 51, 201, nothing)
    cv2.createTrackbar("Ar-width", "settings", 96, 1000, nothing)

    cv2.waitKey(0)

# Main *************************************************************************


if __name__ == "__main__":
    pass
