"""Tests ObjectFinder
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import cv2

# pylint: disable=import-error
from object_finder import ObjectFinder

# Variables ********************************************************************

# Classes **********************************************************************

# Functions ********************************************************************


def test_object_finder():
    """tests if ObjectFinder is able to find three ArUco Markers from an 
        test image (object_marker.png) and determine the position, (speed) 
        and angle of the markers
    """
    # 1. Arrange
    finder = ObjectFinder()

    image = cv2.imread("tests/data/object_marker.png")

    assert image is not None

    # 2. Act
    markers = finder.get_ar(image)

    # 3. Assert
    assert markers[0].position_x == 54
    assert markers[0].position_y == 58
    assert markers[0].speed_x == 0
    assert markers[0].speed_y == 0
    assert markers[0].angle == 1570.8

    assert markers[3].position_x == 648
    assert markers[3].position_y == 767
    assert markers[3].speed_x == 0
    assert markers[3].speed_y == 0
    assert markers[3].angle == 1570.8

    assert markers[7].position_x == 910
    assert markers[7].position_y == 147
    assert markers[7].speed_x == 0
    assert markers[7].speed_y == 0
    assert markers[7].angle == 1570.8

# Main *************************************************************************
