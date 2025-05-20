"""Transformer 

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# inspired by: nathancy (https://stackoverflow.com/questions/7263621/how-to-find-corners-on-a-image-using-opencv)

# Imports **********************************************************************

from typing import List, Tuple
from dataclasses import dataclass
import numpy as np
import cv2

# Variables ********************************************************************

# Classes **********************************************************************


@dataclass
class Transformer:
    """Transformer for images"""

    @staticmethod
    def perspective_transform(image: np.array, corners: List[Tuple[int, int]]) -> np.array:
        """Perspectively transforms an image based on the bounding corners

        Args:
            image (np.array): target image which should be transformed
            corners (List[Tuple[int, int]]): bounding corners in the sequence:
                top_left, top_right, bottom_right then bottom_left

        Returns:
            np.array: The resulting transformed image
        """

        top_l, top_r, bottom_r, bottom_l = corners

        # Determine width of new image which is the max distance between
        # (bottom right and bottom left) or (top right and top left) x-coordinates
        width_a = np.sqrt(((bottom_r[0] - bottom_l[0])
                           ** 2) + ((bottom_r[1] - bottom_l[1]) ** 2))
        width_b = np.sqrt(((top_r[0] - top_l[0]) ** 2) +
                          ((top_r[1] - top_l[1]) ** 2))
        width = max(int(width_a), int(width_b)) + 1

        # Determine height of new image which is the max distance between
        # (top right and bottom right) or (top left and bottom left) y-coordinates
        height_a = np.sqrt(((top_r[0] - bottom_r[0]) ** 2) +
                           ((top_r[1] - bottom_r[1]) ** 2))
        height_b = np.sqrt(((top_l[0] - bottom_l[0]) ** 2) +
                           ((top_l[1] - bottom_l[1]) ** 2))
        height = max(int(height_a), int(height_b)) + 1

        # Construct new points to obtain top-down view of image in
        # top_r, top_l, bottom_l, bottom_r order
        dimensions = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1],
                               [0, height - 1]], dtype="float32")

        # Convert to Numpy format
        corners = np.array(corners, dtype="float32")

        # Find perspective transform matrix
        matrix = cv2.getPerspectiveTransform(corners, dimensions)

        # Return the transformed image
        result_i = cv2.warpPerspective(image, matrix, (width, height))
        return result_i


# Functions ********************************************************************

# Main *************************************************************************
