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
    def _ro_ro_helper(point, middle, offset=45) -> int:
        point_x, point_y = point
        middle_x, middle_y = middle

        vector_x = point_x - middle_x
        vector_y = point_y - middle_y

        rad = math.atan2(vector_x, vector_y)
        deg = math.degrees(rad)
        mrad = round((deg - offset) % 360, 0)
        mrad = math.radians(mrad) * 1000
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

        ys = ObjectFinder._ro_ro_helper(
            [east_middle_x, east_middle_y], [middle_x, middle_y], 0)

        # R, _ = cv2.Rodrigues(marker)

        # yaw = np.arctan2(R[1][0], R[0][0])  # Z-Achse (Yaw)
        # pitch = np.arcsin(-R[2][0])         # Y-Achse (Pitch)
        # roll = np.arctan2(R[2][1], R[2][2])  # X-Achse (Roll)

        # print(f'Marker, Yaw: {yaw}, Pitch: {pitch}, Roll: {roll}')

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

            # _, _, w, h = cv2.boundingRect(marker)

            x, y = marker[0][0]

            x, y = [np.float64(x), np.float64(y)]

            my_object = FoundObject(x, y, 0, 0, rotation)
            object_location[int(identifier.item())] = my_object

        return object_location

# Classes **********************************************************************

# Functions ********************************************************************

# Main *************************************************************************
