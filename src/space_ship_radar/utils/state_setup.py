"""Setup State

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import cv2
import numpy as np

from utils.state import State
from utils.state_tracking import TrackingState
from utils.image_getter import ImageGetter
from utils.scene import Scene
from utils.transformer import Transformer
# from utils.rotation_director import RotationDirector

# Variables ********************************************************************

# Classes **********************************************************************


class SetupState(State):
    """Setup State
        - Initializes the FoundObject Master with current FoundObjects found"""

    def __init__(self):
        super().__init__()
        self.name = "SetupState"

    def run(self, camera) -> None:
        image_bgr = ImageGetter.get_image(camera)

        corners, marker_perimeter = Scene.ar_authority.calculate_corners(
            image_bgr)
        image_bgr = Transformer.perspective_transform(image_bgr, corners)

        # ArUco-width
        real_ar_width = cv2.getTrackbarPos("ArUco", "settings")
        real_ar_perimeter = np.float64(real_ar_width) * 4

        Scene.lord_scaler.init(marker_perimeter, real_ar_perimeter)

        self.context.transition_to(TrackingState())

# Functions ********************************************************************

# Main *************************************************************************
