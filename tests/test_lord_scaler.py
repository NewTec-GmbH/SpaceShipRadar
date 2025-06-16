"""Tests LordScaler
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

# pylint: disable=import-error
from lord_scaler import LordScaler

# Variables ********************************************************************

# Classes **********************************************************************

# Functions ********************************************************************


def test_lord_scaler():
    """tests if LordScaler returns the expected converted values 
        for different ratios between the pixel_perimeter and the mm_perimeter
    """
    lord = LordScaler()

    # first parameter is marker_perimeter in px
    # second parameter is real_ar_perimeter in mm
    lord.init(1, 1)
    converted = lord.convert(10)

    assert converted == 10

    lord.init(1, 2)
    converted = lord.convert(10)
    assert converted == 20

    lord.init(2, 1)
    converted = lord.convert(10)
    assert converted == 5

# Main *************************************************************************
