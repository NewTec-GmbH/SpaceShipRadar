"""Found Object Master

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import logging
import cv2

from utils.histogram_star import HistogramStar
from utils.found_object import FoundObject

# Variables ********************************************************************

# Classes **********************************************************************


class FoundObjectMaster:
    """Found Object Master manages multiple Found Objects"""

    def __init__(self):
        self.found_objects: list[FoundObject] = []

    def is_found_object(self, image, rectangle: tuple[int, int, int, int]) -> bool:
        """determines if the picture is a object which should be tracked"""
        x, y, w, h = rectangle

        # Extract the region of interest (ROI) from the source image
        roi = image[y:y+h, x:x+w]

        hist = HistogramStar.get_hist(roi)
        diff = cv2.compareHist(HistogramStar.get_robo_hist(),
                               hist, cv2.HISTCMP_CORREL)

        h1 = cv2.getTrackbarPos("Histogram", "settings")
        h1 = h1 / 100
        if diff < h1:
            return False

        return True

    def add_found_object(self, num: int, position: tuple[int, int, int, int], angle) -> None:
        """adder for Found Objects"""
        self.found_objects.append(FoundObject(num, position, angle))

    def get_best_match(self, point: tuple[int, int]) -> int:
        """Return the index of the Found Objects which is closest to the point"""
        result: list[int] = []

        for found in self.found_objects:
            found_point = found.get_newest_point()
            diff = abs(found_point[0] - point[0]) + \
                abs(found_point[1] - point[1])
            result.append(diff)

        if len(result) < 1:
            return -1

        smallest_number = min(result)
        return result.index(smallest_number)

    def update_found_object(self, a_list):
        """updates the position of the best match"""

        for found in self.found_objects:
            result = []
            for item in a_list:
                x, y, w, h = item["position"]
                point = (x+w/2, y+h/2)

                found_point = found.get_newest_point()
                diff = abs(found_point[0] - point[0]) + \
                    abs(found_point[1] - point[1])
                result.append(diff)

            if len(result) > 0:
                smallest_number = min(result)
                smallest_index = result.index(smallest_number)

                x, y, w, h = a_list[smallest_index]["position"]
                angle = a_list[smallest_index]["angle"]
                a_list.pop(smallest_index)
                found.update(x, y, w, h, angle)
            else:
                logging.warning(
                    "no match for found Object %s", found.identifier_number)

        if len(a_list) > 0:
            logging.warning("contours unused")

    def get_found_object(self, index: int) -> FoundObject:
        """getter for found object"""
        return self.found_objects[index]

    def reset(self):
        self.found_objects = []

# Functions ********************************************************************

# Main *************************************************************************
