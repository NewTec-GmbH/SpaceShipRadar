"""Object Finder

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import logging
import math
from dataclasses import dataclass
import cv2
import numpy as np

# Variables ********************************************************************


@dataclass
class ObjectFinder:
    """Responsible for finding Objects in Images"""

    @staticmethod
    def get_contours(image: np.ndarray, background: np.ndarray) -> np.array:
        """get the contours from an images"""
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        cv2.namedWindow("Gray: ", cv2.WINDOW_NORMAL)
        cv2.imshow("Gray: ", gray_image)
        cv2.imwrite("new_gray.png", gray_image)

        cv2.namedWindow("Background: ", cv2.WINDOW_NORMAL)
        cv2.imshow("Background: ", background)

        dframe = cv2.absdiff(background, gray_image)
        cv2.namedWindow("Diff: ", cv2.WINDOW_NORMAL)
        cv2.imshow("Diff: ", dframe)
        cv2.imwrite("new_diff.png", dframe)

        gaussian_value = (cv2.getTrackbarPos("Gaussian", "settings") * 2) - 1
        gaussian_value = max(gaussian_value, 1)

        blurred = cv2.GaussianBlur(dframe, (gaussian_value, gaussian_value), 0)

        ret, tframe = cv2.threshold(
            blurred, 30, 255, cv2.THRESH_BINARY)

        cv2.namedWindow("tframe: ", cv2.WINDOW_NORMAL)
        cv2.imshow("tframe: ", tframe)
        cv2.imwrite("new_schwell.png", tframe)

        # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # dframe = cv2.absdiff(background, gray_image)

        # # blurred number has to be uneven
        # # this is only temporary and will be changed later

        # gaussian_value = 5
        # blurred = cv2.GaussianBlur(dframe, (gaussian_value, gaussian_value), 0)

        # ret, tframe = cv2.threshold(
        #     blurred, 30, 255, cv2.THRESH_BINARY)

        # kernel_closing = np.ones((1, 1), np.uint8)
        # kernel_erosion = np.ones((20, 20), np.uint8)

        # closing = cv2.morphologyEx(tframe, cv2.MORPH_CLOSE, kernel_closing)
        # erosion = cv2.erode(closing, kernel_erosion, iterations=1)
        # cv2.namedWindow("Erosion: ", cv2.WINDOW_NORMAL)
        # cv2.imshow("Erosion: ", erosion)

        if ret:
            (contours, _) = cv2.findContours(tframe.copy(),
                                             cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            object_location = []
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                object_location.append([x, y, w, h])

            return np.array(object_location)
        return np.array([])

    @staticmethod
    def _ro_ro_helper(point, middle, offset=45) -> int:
        point_x, point_y = point
        middle_x, middle_y = middle

        vector_x = point_x - middle_x
        vector_y = point_y - middle_y

        # vector_x = east_middle_x - middle_x
        # vector_y = east_middle_y - middle_y

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

        in_zero_one_x = (top_right[0] + bot_right[0]) / 2
        in_zero_one_y = (top_right[1] + bot_right[1]) / 2

        ys = ObjectFinder._ro_ro_helper(
            [in_zero_one_x, in_zero_one_y], [middle_x, middle_y], 0)

        # east_middle_x = (top_right[0] + bot_right[0])
        # east_middle_y = (top_right[1] + bot_right[1])

        # point_x, point_y = top_right

        # vector_x = point_x - middle_x
        # vector_y = point_y - middle_y

        # # vector_x = east_middle_x - middle_x
        # # vector_y = east_middle_y - middle_y

        # rad = math.atan2(vector_x, vector_y)
        # deg = math.degrees(rad)
        # mrad = round((deg - 45) % 360, 0)
        # mrad = math.radians(mrad) * 1000

        mrad = ObjectFinder._ro_ro_helper(top_right, [middle_x, middle_y])

        mrad_top_right = ObjectFinder._ro_ro_helper(
            top_right, [middle_x, middle_y], 45)

        mrad_top_left = ObjectFinder._ro_ro_helper(
            top_left, [middle_x, middle_y], 135)

        mrad_bot_left = ObjectFinder._ro_ro_helper(
            bot_left, [middle_x, middle_y], 225)

        mrad_bot_right = ObjectFinder._ro_ro_helper(
            bot_right, [middle_x, middle_y], 315)

        # print(
        #     f'top_right: {mrad_top_right}')
        # print(
        #     f'top_left: {mrad_top_left}')
        # print(
        #     f'bot_left: {mrad_bot_left}')
        # print(
        #     f'bot_right: {mrad_bot_right}')

        l = [mrad_bot_left, mrad_top_left, mrad_bot_left, mrad_bot_right]

        mrad_mean = np.median([l])

        # print(f'mrad mean: {mrad_mean}')

        # mrad = -rad * 1000

        # # adjust :) pointing east is 0
        # mrad -= 785.398

        # R, _ = cv2.Rodrigues(marker)

        # yaw = np.arctan2(R[1][0], R[0][0])  # Z-Achse (Yaw)
        # pitch = np.arcsin(-R[2][0])         # Y-Achse (Pitch)
        # roll = np.arctan2(R[2][1], R[2][2])  # X-Achse (Roll)

        # print(f'Marker, Yaw: {yaw}, Pitch: {pitch}, Roll: {roll}')

        return ys  # mrad

    # @staticmethod
    # def _get_rotation_from_ar(marker) -> float:
    #     top_left, top_right, bot_right, bot_left = marker

    #     refernce_point = top_left

    #     direction = []

    #     for point in marker[1:]:
    #         dx = point[0] - refernce_point[0]
    #         dy = point[0] - refernce_point[1]

    #         winkel = np.arctan2(dy, dx)

    #         direction.append(winkel)

    #     mrad = [winkel * 1000 for winkel in direction]
    #     return mrad[0]

    @staticmethod
    def get_ar(image: np.ndarray) -> np.array:
        """get the ar from an images"""

        dictionary = cv2.aruco.getPredefinedDictionary(
            cv2.aruco.DICT_4X4_50)
        parameters = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(dictionary, parameters)

        # pylint: disable=unpacking-non-sequence
        marker_corners, marker_ids, _ = detector.detectMarkers(image)

        # print(marker_corners)
        object_location = []
        for i, marker in enumerate(marker_corners):
            identifier = marker_ids[i]
            rotation = ObjectFinder._get_rotation_from_ar(marker[0])

            _, _, w, h = cv2.boundingRect(marker)
            # logging.error(marker[0][0])
            x, y = marker[0][0]
            # # x, y = [int(round(x, 1)), int(round(y, 1))]
            x, y = [np.float64(x), np.float64(y)]
            logging.error(type(x))
            # print(f"this is x {x}, y {y}")

            object_location.append(
                {"position": [x, y, w, h], "identifier": identifier, "angle": rotation})
        return np.array(object_location)

# Classes **********************************************************************

# Functions ********************************************************************

# Main *************************************************************************
