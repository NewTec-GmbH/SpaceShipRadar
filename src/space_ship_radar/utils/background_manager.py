"""Manages what is considered to be background"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import cv2
from utils.path_gouverneur import PathGouverneur

# Classes **********************************************************************


class BackgroundManager:
    """This class manages what is considered to be the background 
        and therefore what is ignored by the visual recognition. """

    def __init__(self):
        self.empty = cv2.imread(
            PathGouverneur.get_path() + 'empty.png', cv2.IMREAD_GRAYSCALE)

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
