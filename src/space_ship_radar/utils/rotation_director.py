"""Rotation Director

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# inspired by: https://www.geeksforgeeks.org/filter-color-with-opencv/

# Imports **********************************************************************

import math
import cv2
import numpy as np

# Variables ********************************************************************

# Classes **********************************************************************


class RotationDirector():
    """Rotation Director"""

    @staticmethod
    def __calc_angle(point1, point2, offset=90):

        delta_x = point2[0] - point1[0]
        delta_y = point2[1] - point1[1]

        # Radians
        angle_rad = math.atan2(delta_y, delta_x)

        # Degrees
        angle_deg = math.degrees(angle_rad)

        # Return a positiv angle
        # 0 Degrees points up with default offset 90
        angle_deg = (angle_deg + offset) % 360

        angle_deg = round(angle_deg, 2)
        return angle_deg

    @staticmethod
    def get_biggest_contour(contours):
        """returns the biggest contour by area"""
        # only biggest contour
        b_cnt = []
        for cnt in contours:
            _, _, c_width, c_height = cv2.boundingRect(cnt)
            s_area = c_width * c_height
            b_cnt.append({"contour": cnt, "area": s_area})
        b_cnt_sorted = sorted(b_cnt, key=lambda x: x["area"], reverse=True)

        selected_cnt = b_cnt_sorted[0]["contour"]
        return selected_cnt

    @staticmethod
    def _get_contours_of_color_space(roi):
        """finds the contours of a color space inside the region of interest

        Args:
            roi (np.array): region of interest inside of an image

        Returns:
            np.array: found contours
        """

        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # webots
        lower = np.array([139, 0, 0])
        upper = np.array([170, 20, 100])

        # real
        # lower = np.array([0, 60, 100])
        # upper = np.array([40, 255, 250])

        # preparing the mask to overlay
        mask = cv2.inRange(hsv, lower, upper)

        blurred = cv2.GaussianBlur(mask, (21, 21), 0)

        _, tframe = cv2.threshold(
            blurred, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        # contours
        contours, _ = cv2.findContours(
            tframe, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        return contours

    @staticmethod
    def calc_angle(image, rectangle):
        """calculates an angle based on a color mask"""
        x, y, w, h = rectangle

        # Extract the region of interest (ROI) from the source image
        roi = image[y:y+h, x:x+w]
        contours = RotationDirector._get_contours_of_color_space(
            roi)

        if len(contours) < 1:
            return -1

        selected_cnt = RotationDirector.get_biggest_contour(contours)

        # middle of picture
        middle_of_picture = int(w / 2), int(h / 2)

        # middle of contour
        x, y, w, h = cv2.boundingRect(selected_cnt)
        middle_of_contour = int(x+w/2), int(y+h/2)

        # calculate angle
        angle = RotationDirector.__calc_angle(
            middle_of_picture, middle_of_contour)
        return angle

# Functions ********************************************************************

# Main *************************************************************************
