"""Ar-Marker

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import numpy as np
import cv2

# Variables ********************************************************************

# Classes **********************************************************************


class ArAuthority:
    """ArAuthority"""

    def __init__(self):
        self._corners = []

    @property
    def corners(self) -> np.array:
        """getter for the corners"""
        return self._corners

    def calculate_corners(self, image: np.array):
        """finds where the corners of the predefined ar-markers are in the image

        Args:
            image (np.array): target image which contains 4 ar-markers

        Returns:
            List[Tuple[int, int]]: corner-points of the 4 ar-markers (only the most outer points -> 4 points in total)
        """
        marker_corners, _ = ArAuthority._get_corners_from_dict(image)
        result = ArAuthority._get_bounding_rect_sorted(marker_corners)
        self._corners = result
        return result

    @staticmethod
    def _get_corners_from_dict(image: np.array):
        """returns all marker_corners and the corresponding marker_ids found in the image

        Args:
            image (np.array): target image with ar-markers

        Returns:
            List[List[Tuple[float, float]]]: marker_corners
            List[int]: marker_ids
        """
        dictionary = cv2.aruco.getPredefinedDictionary(
            cv2.aruco.DICT_ARUCO_ORIGINAL)
        parameters = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(dictionary, parameters)

        # pylint: disable=unpacking-non-sequence
        marker_corners, marker_ids, _ = detector.detectMarkers(
            image)  # _ = rejectedCandidates
        return marker_corners, marker_ids

    @staticmethod
    def _get_bounding_rect_sorted(marker_corners):
        """returns the 4 most outer points from marker_corners assumed the markers are already in the order:
                top_left, top_right, bottom_right then bottom_left

        Args:
            marker_corners (List[List[Tuple[float, float]]]): found marker_corners

        Returns:
            List[Tuple[float, float]]: The most outer points of the marker_corners
        """

        result = []
        for i, marker in enumerate(marker_corners):
            result.append(marker[0][i])

        return result

    @staticmethod
    def _get_bounding_rect_unsorted(marker_corners, marker_ids, sequence=(923, 1001, 241, 1007)):
        """returns the 4 most outer points from marker_corners assumed the markers are NOT already in the order:
            top_left, top_right, bottom_right then bottom_left

        Args:
            marker_corners (List[List[Tuple[float, float]]]): found marker_corners
            marker_ids (List[int]): ids of the found markers
            sequence (List[int]): the sequence in which the markers should be to sorted to

        Returns:
            List[Tuple[float, float]]: The most outer points of the marker_corners
        """

        # bounding_corners = dict(zip(markerIds, markerCorners))
        bounding_corners = {int(marker_ids[i]): marker_corners[i]
                            for i in range(len(marker_ids))}

        r_bounding_corners = []
        # top_l, top_r, bottom_r, bottom_l

        for i, position in enumerate(sequence):
            r_bounding_corners.append(bounding_corners[position][0][i])


# Functions ********************************************************************

# Main *************************************************************************
