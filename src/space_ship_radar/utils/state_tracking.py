"""Tracking State

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

from utils.state import State
from utils.tracker import Tracker

# Variables ********************************************************************

# Classes **********************************************************************


class TrackingState(State):
    """main loop"""

    def run(self, camera) -> None:
        """tracking ..."""
        Tracker.tracking(camera)

# Functions ********************************************************************

# Main *************************************************************************
