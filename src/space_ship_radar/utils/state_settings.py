"""Background State

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

from utils.state import State
from utils.state_background import BackgroundState
from utils.settings import start_settings

# Variables ********************************************************************

# Classes **********************************************************************


class SettingsState(State):
    """pre_main"""

    def __init__(self):
        super().__init__()
        self.name = "SettingsState"

    def run(self, camera) -> None:
        start_settings()

        # pylint: disable=no-member

        self.context.transition_to(BackgroundState())

# Functions ********************************************************************

# Main *************************************************************************
