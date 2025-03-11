"""Background State

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

from utils.state import State
from utils.state_setup import SetupState
from utils.tracker import Tracker

# Variables ********************************************************************

# Classes **********************************************************************


class BackgroundState(State):
    """pre_main"""

    def run(self, camera) -> None:
        Tracker.background(camera)
        # pylint: disable=no-member
        self.context.transition_to(SetupState())

# Functions ********************************************************************

# Main *************************************************************************
