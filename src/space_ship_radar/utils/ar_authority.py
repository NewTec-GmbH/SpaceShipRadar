"""Ar-Marker

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import logging
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
            int : marker perimeter of first marker or -1 if None found
        """
        marker_corners, marker_ids = ArAuthority._get_corners_from_dict(image)
        if marker_ids is None or len(marker_ids) < 4:
            logging.error(marker_ids)

        if marker_corners is None or marker_ids is None or len(marker_ids) < 4:
            logging.warning("AR corners not found")

            corners = self._return_default(image)
            self._corners = corners
            return corners, -1

        marker_perimeter = int(cv2.arcLength(marker_corners[0], True))
        ok, result = ArAuthority._get_bounding_rect_unsorted(
            marker_corners, marker_ids)

        if ok:
            self._corners = result
            return result, marker_perimeter

        else:
            corners = self._return_default(image)
            self._corners = corners
            return corners, -1

    @staticmethod
    def _return_default(image):
        top_l = (0, 0)
        top_r = (image.shape[1], 0)
        bottom_r = (image.shape[1], image.shape[0])
        bottom_l = (0, image.shape[0])

        corners = [top_l, top_r, bottom_r, bottom_l]
        return corners

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
            cv2.aruco.DICT_5X5_50)
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

    # (923, 1001, 241, 1007) original
    # (923, 431, 1007, 316) mirrored
    # (1007, 316, 923, 431) works
    # (6, 13, 35, 49) new dict
    @staticmethod
    def _get_bounding_rect_unsorted(marker_corners, marker_ids, sequence=(6, 13, 35, 49)):
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

        # logging.warning("bounding corners: %s", bounding_corners)
        try:
            for i, position in enumerate(sequence):
                r_bounding_corners.append(bounding_corners[position][0][i])
            return True, r_bounding_corners
        except KeyError as error:
            logging.error(error)
            return False, -1

# Functions ********************************************************************

# Main *************************************************************************
