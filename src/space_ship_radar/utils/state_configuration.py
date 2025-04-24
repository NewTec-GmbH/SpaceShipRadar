"""Background State

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import cv2

from utils.state import State
# from utils.state_background import BackgroundState
from utils.state_setup import SetupState

# Variables ********************************************************************

# Classes **********************************************************************


class ConfigurationState(State):
    """Configuration State
        - Creates the 'settings'-window which contains trackbars, which 
            can be used to adjust different values in the code like
                - The ArUco-marker-width or the Gaussian Blur (used in ObjectFinder)"""

    def __init__(self):
        super().__init__()
        self.name = "ConfigurationState"

    @staticmethod
    def _nothing(*_):
        """does nothing"""

    @staticmethod
    def _start_settings():
        """
        Create a settings window with the following trackbars:
            - Histogram
            - Gaussian
            - ArUco
        """

        cv2.namedWindow("settings", cv2.WINDOW_NORMAL)
        width = 500
        height = 200
        cv2.resizeWindow("settings", width, height)
        # cv2.createTrackbar("Histogram", "settings", 50,
        #                    100, ConfigurationState._nothing)
        cv2.createTrackbar("Gaussian", "settings", 21,
                           201, ConfigurationState._nothing)
        cv2.createTrackbar("ArUco", "settings", 100,
                           500, ConfigurationState._nothing)

        cv2.waitKey(0)

    def run(self, camera) -> None:
        ConfigurationState._start_settings()

        # pylint: disable=no-member

        self.context.transition_to(SetupState())

# Functions ********************************************************************

# Main *************************************************************************
