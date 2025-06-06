"""Background State

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import time
import cv2

from utils.state import State
from utils.state_setup import SetupState
from utils.image_getter import ImageGetter
from utils.scene import Scene
from utils.transformer import Transformer

# Variables ********************************************************************

# Classes **********************************************************************


class BackgroundState(State):
    """Background State
        - Is able to change what is considered to be background if the user presses b
            - Then the current image is the background
        - If the user presses something else, then the background is not changed"""

    def __init__(self):
        super().__init__()
        self.name = "BackgroundState"

    def run(self, camera) -> None:
        """changes the background if the b-key is pressed"""

        image_bgr = ImageGetter.get_image(camera)

        corners, _ = Scene.ar_authority.calculate_corners(
            image_bgr)
        image_bgr = Transformer.perspective_transform(image_bgr, corners)

        if cv2.waitKey(0) == ord('b'):
            print("***updating background***")
            cv2.imwrite("transformed_one.png", image_bgr)
            Scene.background_manager.set_background(
                cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY))
            time.sleep(1)
        cv2.waitKey(0)

        # pylint: disable=no-member

        self.context.transition_to(SetupState())

# Functions ********************************************************************

# Main *************************************************************************
