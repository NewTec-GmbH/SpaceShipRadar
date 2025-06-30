"""Tests FoundObjectMaster
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import time

# pylint: disable=import-error
from found_object_master import FoundObjectMaster
from found_object import FoundObject

# Variables ********************************************************************

# Classes **********************************************************************

# Functions ********************************************************************


def test_update_list_speed():
    """checks if FoundObjectMaster can correctly determine the speed 
        of an object if it moves (twice) with a certain tolerance
    """
    # 1. Arrange
    my_master = FoundObjectMaster()
    my_objct_initial = FoundObject((0, 0), (0, 0), (0))
    my_objct_moved = FoundObject((500, 500), (0, 0), (0))
    my_objct_moved_again = FoundObject((250, 250), (0, 0), (0))

    # 2. Act
    my_master.update_list({0: my_objct_initial})
    time.sleep(0.1)
    my_master.update_list({0: my_objct_moved})

    # 3. Assert
    target_value = 5000
    actual_value = my_master.found_objects[0].speed_x
    tolerance = 0.2 * target_value

    assert abs(actual_value - target_value) <= tolerance

    # 4. Act
    time.sleep(0.1)
    my_master.update_list({0: my_objct_moved_again})

    # 5. Assert
    target_value = -2500
    actual_value = my_master.found_objects[0].speed_x
    tolerance = -(0.2 * target_value)

    assert abs(actual_value - target_value) <= tolerance

# Main *************************************************************************
