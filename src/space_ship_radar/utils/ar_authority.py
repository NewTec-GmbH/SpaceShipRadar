"""Ar Authority

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
        self._marker_corners: np.array = np.array([])
        self.marker_perimeter = -1

    @property
    def marker_corners(self) -> np.array:
        """getter for the marker corners"""
        return self._marker_corners

    @staticmethod
    def _pre_process_image(image) -> np.array:
        # upper and lower bound for magenta ar trackers
        lower_bound = np.array([105, 0, 105])
        upper_bound = np.array([255, 150, 255])

        mask = cv2.inRange(image, lower_bound, upper_bound)

        # create a white image
        output = np.ones_like(image) * 255

        # only the parts of the mask are colored black
        output[mask > 0] = [0, 0, 0]

        # visualize the result for debugging
        cv2.namedWindow("Ar Pre: ", cv2.WINDOW_NORMAL)
        cv2.imshow("Ar Pre: ", output)

        return output

    @staticmethod
    def _my_arc_length(corner, bo):

        result = cv2.arcLength(corner, bo)
        print(f"perimeter: {result}")
        return result

    def calculate_corners(self, image: np.array):
        """finds where the corners of predefined ar-markers are in the image

        Args:
            image (np.array): target image which (can) contains 4 ar-markers

        Returns:
            List[Tuple[int, int]]: corner-points of the 4 ar-markers (only the most outer points -> 4 points in total)
            int : marker perimeter of first marker or -1 if None found
        """
        # extract only magenta colors form the image (for magenta ar trackers)
        image = self._pre_process_image(image)

        # search the image for aruco markers
        marker_corners, marker_ids = ArAuthority._get_corners_from_dict(image)

        if marker_corners is None or marker_ids is None or len(marker_ids) < 4:
            logging.warning("AR corners not found")

            corners = self._return_default(image)
            self._marker_corners = corners
            return corners, -1

        # calculate marker perimeter (used for coordinate scaling later)
        marker_perimeter = int(
            np.mean([self._my_arc_length(corner, True) for corner in marker_corners]))

        # sort the markers clock wise
        ok, result = ArAuthority._get_bounding_rect_unsorted(
            marker_corners, marker_ids)

        if not ok:
            corners = self._return_default(image)
            self._marker_corners = corners
            return corners, -1

        self._marker_corners = result
        return result, marker_perimeter

    def _return_default(self, image):
        """will return default corners if the markers cannot be detected

        Args:
            image (np.array): target image

        Returns:
            array: list of default corners
        """

        # if markers have already been found return those
        if len(self.marker_corners) > 3:
            return self.marker_corners

        # else return the image corners (then the scaling will do nothing)
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
