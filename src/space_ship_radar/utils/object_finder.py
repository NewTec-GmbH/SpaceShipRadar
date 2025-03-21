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
    """Responsible for finding Objects in Images"""

    @staticmethod
    def get_contours(image: np.ndarray, background: np.ndarray) -> np.array:
        """get the contours from an images"""
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.namedWindow("Background: ", cv2.WINDOW_NORMAL)
        cv2.imshow("Background: ", background)
        dframe = cv2.absdiff(background, gray_image)

        # blurred number has to be uneven
        # this is only temporary and will be changed later
        gaussian_value = cv2.getTrackbarPos("Gaussian", "settings")
        if gaussian_value % 2 == 0:
            logging.error(
                "The Gaussian blur number needs to be uneven!")
            sys.exit(1)

        blurred = cv2.GaussianBlur(dframe, (gaussian_value, gaussian_value), 0)

        ret, tframe = cv2.threshold(
            blurred, 30, 255, cv2.THRESH_BINARY)

        cv2.namedWindow("tframe: ", cv2.WINDOW_NORMAL)
        cv2.imshow("tframe: ", tframe)

        if ret:
            (contours, _) = cv2.findContours(tframe.copy(),
                                             cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            object_location = []
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                object_location.append([x, y, w, h])

            return np.array(object_location)
        return np.array([])

# Classes **********************************************************************

# Functions ********************************************************************

# Main *************************************************************************
