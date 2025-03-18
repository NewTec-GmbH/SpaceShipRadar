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
from utils.rotation_director import RotationDirector

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

        background = Scene.background_manager.background
        image_bgr = cv2.resize(
            image_bgr, (background.shape[1], background.shape[0]))

        boxes = ObjectFinder.get_contours(image_bgr, background)

        # reset found object master
        Scene.found_object_master.reset()

        for found_object_index, cnt in enumerate(boxes):
            x, y, w, h = cnt

            # check if the found object is a robot and should be tracked
            # or if it is 'noise' and can be added to the background and therefore
            # will not be considered for the tracking (does only work for static/non-moving obstacles)

            # roi_object = image_bgr[y:y+h, x:x+w]

            # if Scene.found_object_master.is_found_object(image_bgr, (x, y, w, h)):
            angle = RotationDirector.calc_angle(image_bgr, (x, y, w, h))
            Scene.found_object_master.add_found_object(
                found_object_index, (x, y, w, h), angle)
            # else:
            #     # copy the object into the background which will ignore it in the future
            #     Scene.background_manager.copy_region(
            #         image_bgr, (x, y, w, h))
            #     # pas
        # pylint: disable=no-member

        self.context.transition_to(TrackingState())

# Functions ********************************************************************

# Main *************************************************************************
