"""Time Checker

Author: Marc Trosch (marc.trosch@newtec.de)
"""


# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import time

# Variables ********************************************************************

# Classes **********************************************************************


class TimeChecker():
    """Time Checker"""

    def __init__(self):
        self._last_call_time = None

    def _check_time(self) -> bool:
        """check if 1 second has passed

        Returns:
            bool: True if more than 1s has passed
                    else: False 
        """
        current_time = time.time()

        if self._last_call_time is None:
            self._last_call_time = current_time
            return False

        elapsed_time = current_time - self._last_call_time

        if elapsed_time > 1:
            self._last_call_time = current_time
            return True

        return False


# Functions ********************************************************************

# Main *************************************************************************
