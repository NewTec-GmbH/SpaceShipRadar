"""Tests ArAuthority
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import cv2

# pylint: disable=import-error
from ar_authority import ArAuthority

# Variables ********************************************************************

# Classes **********************************************************************

# Functions ********************************************************************


def test_ar_authority():
    """tests if ArAuthority is able to find four ArUco Markers in a
        test image (edge_marker.png) and correctly identifies the position
        and the perimeter of the markers
    """
    # 1. Arrange
    authority = ArAuthority()
    image = cv2.imread("tests/data/edge_marker.png")

    assert image is not None

    # outside corners of the markers [top_left, top_right, bottom_right, bottom_left]
    expected_corners = [[7, 9], [623, 9], [623, 491], [7, 491]]
    expected_perimeter = 808

    # 2. Act
    corners, perimeter = authority.calculate_corners(image)

    # 3. Assert
    assert corners[0][0] == expected_corners[0][0]
    assert corners[0][1] == expected_corners[0][1]

    assert corners[1][0] == expected_corners[1][0]
    assert corners[1][1] == expected_corners[1][1]

    assert corners[2][0] == expected_corners[2][0]
    assert corners[2][1] == expected_corners[2][1]

    assert corners[3][0] == expected_corners[3][0]
    assert corners[3][1] == expected_corners[3][1]

    assert perimeter == expected_perimeter

# Main *************************************************************************
