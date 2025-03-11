"""Object Finder

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import logging
import sys
from dataclasses import dataclass
import cv2
import numpy as np

# Variables ********************************************************************


@dataclass
class ObjectFinder:
    """Object Finder"""

    @staticmethod
    def get_contours(image: np.ndarray, background: np.ndarray) -> np.array:
        """get the contours from an images"""
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.namedWindow("Background: ", cv2.WINDOW_NORMAL)
        cv2.imshow("Background: ", background)
        dframe = cv2.absdiff(background, gray_image)
        # cv2.namedWindow("Dframe: ", cv2.WINDOW_NORMAL)
        # cv2.imshow("Dframe: ", dframe)

        # kernel = np.ones((16, 16), np.uint8)
        # erosion = cv2.morphologyEx(
        #     dframe, cv2.MORPH_OPEN, kernel, iterations=1)
        # cv2.namedWindow("Morph: ", cv2.WINDOW_NORMAL)
        # cv2.imshow("Morph: ", erosion)

        # ret, tframe_morph = cv2.threshold(
        #     erosion, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        # cv2.namedWindow("Morph thresh: ", cv2.WINDOW_NORMAL)
        # cv2.imshow("Morph thresh: ", tframe_morph)

        # blurred number has to be uneven
        g1 = cv2.getTrackbarPos("Gaussian", "settings")
        if g1 % 2 == 0:
            logging.error(
                "The Gaussian blur number needs to be uneven!")
            cv2.destroyAllWindows()
            sys.exit(1)

        blurred = cv2.GaussianBlur(dframe, (g1, g1), 0)
        # cv2.namedWindow("GaussianBlur: ", cv2.WINDOW_NORMAL)
        # cv2.imshow("GaussianBlur: ", blurred)

        ret, tframe = cv2.threshold(
            blurred, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        # ret, tframe = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)

        cv2.namedWindow("tframe: ", cv2.WINDOW_NORMAL)
        cv2.imshow("tframe: ", tframe)

        if ret:

            # kernel = np.ones((5, 5), np.uint8)
            # morphed = cv2.morphologyEx(tframe, cv2.MORPH_CLOSE, kernel)

            # eroded = cv2.erode(morphed, kernel, iterations=1)
            (contours, _) = cv2.findContours(tframe.copy(),
                                             cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            object_location = []
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                rotrect = cv2.minAreaRect(cnt)
                angle = rotrect[-1]

                # from https://www.pyimagesearch.com/2017/02/20/text-skew-correction-opencv-python/
                # the `cv2.minAreaRect` function returns values in the
                # range [-90, 0); as the rectangle rotates clockwise the
                # returned angle trends to 0 -- in this special case we
                # need to add 90 degrees to the angle
                if angle < -45:
                    angle = -(90 + angle)

                # otherwise, just take the inverse of the angle to make
                # it positive
                else:
                    angle = -angle

                object_location.append([x, y, w, h])

            return np.array(object_location)
        return np.array([])

    # Classes **********************************************************************
    # Functions ********************************************************************
    # Main *************************************************************************
