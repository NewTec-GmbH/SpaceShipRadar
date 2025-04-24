"""Setup State

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import cv2

from utils.state import State
from utils.state_tracking import TrackingState
from utils.image_getter import ImageGetter
from utils.scene import Scene
from utils.transformer import Transformer
from utils.object_finder import ObjectFinder
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
        Scene.lord_scaler.init(marker_perimeter)

        # background = Scene.background_manager.background
        # image_bgr = cv2.resize(
        #     image_bgr, (background.shape[1], background.shape[0]))

        # boxes = ObjectFinder.get_contours(image_bgr, background)

        # reset found object master
        # Scene.found_object_master.reset()

        # for found_object_index, cnt in enumerate(boxes):
        #     x, y, w, h = cnt

        # angle = RotationDirector.calc_angle(image_bgr, (x, y, w, h))
        # Scene.found_object_master.add_found_object(
        #     found_object_index, (x, y, w, h), angle)
        # pylint: disable=no-member

        self.context.transition_to(TrackingState())

# Functions ********************************************************************

# Main *************************************************************************
