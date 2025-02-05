"""Manages what is considered to be background

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import cv2
import numpy as np
from utils.path_gouverneur import PathGouverneur

# Variables ********************************************************************

# Classes **********************************************************************


class BackgroundManager:
    """This class manages what is considered to be the background 
        and therefore what is ignored by the visual recognition. """

    def __init__(self):
        self.background_path: str = "./empty.png"
        self.__load_background()

    def __load_background(self):
        self.empty: np.array = cv2.imread(
            f"{PathGouverneur.get_path()}{self.background_path}", cv2.IMREAD_GRAYSCALE)

    def get_background(self):
        """getter for the empty background"""
        return self.empty

    def copy_region(self, image, rectangle: tuple[int, int, int, int]):
        """copies a image into the background"""
        x, y, w, h = rectangle
        source_image = image.copy()
        source_image = cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY)

        # Extract the region of interest (ROI) from the source image
        roi = source_image[y:y+h, x:x+w]
        cv2.imshow("roi", roi)
        cv2.waitKey(1)

        # Paste the ROI into the destination image at the same location
        self.empty[y:y+h, x:x+w] = roi

    def get_background_path(self) -> str:
        """getter for the current background image"""
        return self.background_path

    def set_background_path(self, path: str) -> None:
        """setter for the current background image and reload the background image"""
        self.background_path = path
        self.__load_background()

# Functions ********************************************************************

# Main *************************************************************************
