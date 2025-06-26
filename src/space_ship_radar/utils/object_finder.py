"""Object Finder

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import math
from dataclasses import dataclass
import cv2
import numpy as np

from utils.found_object import FoundObject

# Variables ********************************************************************


@dataclass
class ObjectFinder:
    """Responsible for finding Objects in Images"""

    @staticmethod
    def _calculate_rotational_offset(point, middle) -> float:
        point_x, point_y = point
        middle_x, middle_y = middle

        vector_x = point_x - middle_x
        vector_y = point_y - middle_y

        mrad = math.atan2(vector_x, vector_y) * 1000
        return mrad

    @staticmethod
    def _get_rotation_from_ar(marker) -> float:
        top_left, top_right, bot_right, bot_left = marker

        middle_x = (
            top_right[0] + top_left[0] + bot_right[0] + bot_left[0]) / 4
        middle_y = (
            top_right[1] + top_left[1] + bot_right[1] + bot_left[1]) / 4

        east_middle_x = (top_right[0] + bot_right[0]) / 2
        east_middle_y = (top_right[1] + bot_right[1]) / 2

        ys = ObjectFinder._calculate_rotational_offset(
            [east_middle_x, east_middle_y], [middle_x, middle_y])

        return round(ys, 2)  # mrad

    @staticmethod
    def get_ar(image: np.ndarray):
        """get the ar from an images"""

        dictionary = cv2.aruco.getPredefinedDictionary(
            cv2.aruco.DICT_4X4_50)
        parameters = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(dictionary, parameters)

        # pylint: disable=unpacking-non-sequence
        marker_corners, marker_ids, _ = detector.detectMarkers(image)

        object_location = {}
        for i, marker in enumerate(marker_corners):
            identifier = marker_ids[i]
            rotation = ObjectFinder._get_rotation_from_ar(marker[0])

            x, y = marker[0][0]
            my_object = FoundObject((x, y), (0, 0), rotation)
            object_location[int(identifier.item())] = my_object

        return object_location

# Classes **********************************************************************

# Functions ********************************************************************

# Main *************************************************************************
