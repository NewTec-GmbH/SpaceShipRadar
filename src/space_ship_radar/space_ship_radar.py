"""The main module with the program entry point.

Controller definition

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import sys
import logging
from cv2 import cv2
import keyboard
from controller import Robot  # type: ignore # pylint: disable=import-error
from utils import helper
from utils.core import SpaceShipRadar

try:
    from space_ship_radar.version import __version__, __author__, __email__, __repository__, __license__
except ModuleNotFoundError:
    # provide dummy information when not installed as package but called directly
    # also necessary to get sphinx running without error
    __version__ = 'dev'
    __author__ = 'Marc Trosch'
    __email__ = 'marc.trosch@newtec.de'
    __repository__ = 'SpaceShipRadar'
    __license__ = 'none'

# Variables ********************************************************************

LOG: logging.Logger = logging.getLogger(__name__)

# Classes **********************************************************************


class Controller(Robot):
    """Class representing a Controller"""

    def __init__(self):
        super().__init__()
        self.time_step = 32
        self.camera = self.getDevice('camera')
        self.camera.enable(self.time_step)

    def run(self) -> None:
        """Main function of the controller"""

        # Setup
        self.step(self.time_step)  # step required
        SpaceShipRadar.pre_main(self.camera)

        # Main Loop
        while self.step(self.time_step) != -1:
            SpaceShipRadar.main_loop(self.camera)
            if keyboard.is_pressed('q'):  # quit
                break
        cv2.destroyAllWindows()

    def run_save(self) -> None:
        """Debug function to save an image"""
        self.step(self.time_step)
        image = helper.get_image(self.camera)
        cv2.imwrite("new_not_empty.png", image)

    def run_record(self) -> None:
        """Debug function to record a video"""
        while self.step(self.time_step) != -1:
            if keyboard.is_pressed('q'):
                break

            if keyboard.is_pressed('s'):
                helper.record_video(self.camera, self.step, self.time_step)

# Functions ********************************************************************


def main() -> int:
    """ The program entry point function.

    .. uml::

        Alice -> Bob: Hi!
        Alice <- Bob: How are you?

    Returns:
        int: System exit status.
    """
    controller = Controller()
    controller.run()
    logging.basicConfig(level=logging.INFO)
    LOG.info("Hello World!")
    return 0  # return without errors

# Main *************************************************************************


if __name__ == "__main__":
    sys.exit(main())
