"""Manages what is considered to be background

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import cv2
import numpy as np

from utils.path_governor import PathGovernor

# Variables ********************************************************************

# Classes **********************************************************************


class BackgroundManager:
    """This class manages what is considered to be the background 
        and therefore what is ignored by the visual recognition. """

    def __init__(self):
        self._background_path: str = "./empty.png"
        self._empty = None
        self.__load_background()

    def __load_background(self):
        self._empty: np.array = cv2.imread(
            f"{PathGovernor.get_path()}{self.background_path}", cv2.IMREAD_GRAYSCALE)

    @property
    def background(self) -> np.array:
        """getter for the empty background"""
        return self._empty

    def copy_region(self, image, rectangle: tuple[int, int, int, int]):
        """copies a image into the background"""
        x, y, w, h = rectangle
        source_image = image.copy()
        source_image = cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY)

        # Extract the region of interest (ROI) from the source image
        roi = source_image[y:y+h, x:x+w]

        # For Testing
        # cv2.waitKey(1)
        # cv2.imwrite(f"testing{random.randint(1,10000)}.png", roi)
        # Paste the ROI into the destination image at the same location
        self._empty[y:y+h, x:x+w] = roi

    @property
    def background_path(self) -> str:
        """getter for the current background image path"""
        return self._background_path

    @background_path.setter
    def background_path(self, path: str) -> None:
        """setter for the current background image and reload the background image"""
        self._background_path = path
        self.__load_background()

    def set_background(self, image):
        """set background"""
        self._empty = image

# Functions ********************************************************************

# Main *************************************************************************
