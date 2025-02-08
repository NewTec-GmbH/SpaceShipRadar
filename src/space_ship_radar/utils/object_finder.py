"""Object Finder

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

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
        # blurred number has to be uneven
        blurred = cv2.GaussianBlur(dframe, (41, 41), 0)
        cv2.namedWindow("GaussianBlur: ", cv2.WINDOW_NORMAL)
        cv2.imshow("GaussianBlur: ", blurred)
        cv2.waitKey(1)
        ret, tframe = cv2.threshold(
            blurred, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
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
