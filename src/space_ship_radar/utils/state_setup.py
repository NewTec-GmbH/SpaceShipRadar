"""Setup State

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

from utils.state import State
from utils.state_tracking import TrackingState
from utils.tracker import Tracker

# Variables ********************************************************************

# Classes **********************************************************************


class SetupState(State):
    """pre_main"""

    def run(self, camera) -> None:
        Tracker.setup(camera)
        # pylint: disable=no-member
        self.context.transition_to(TrackingState())

# Functions ********************************************************************

# Main *************************************************************************
