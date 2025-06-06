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
        # diff: describes a number between 0 and 1 represents how good the histograms match
        # (1: is very good, and 0: is very bad)
        diff = cv2.compareHist(HistogramStar.get_robo_hist(),
                               hist, cv2.HISTCMP_CORREL)

        # get the value of settings-window of Histogram
        h1 = cv2.getTrackbarPos("Histogram", "settings")
        h1 = h1 / 100

        # if the difference is too big then it is not considered to be a found object and False is returned
        # In this case h1 is the threshold of how "good" a result has to be to be considered to be a found_object
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

    def update_found_object(self, object_properties):
        """updates the position of the best match

        Args:
            object_properties: dict which holds 'position' in (x, y, w, h) and 'angle' in mrad for each found object
        """

        # will assign each found object the closest contour
        for found in self.found_objects:
            result = []
            for item in object_properties:
                x, y, w, h = item["position"]
                point = (x+w/2, y+h/2)

                found_point = found.get_newest_point()
                diff = abs(found_point[0] - point[0]) + \
                    abs(found_point[1] - point[1])
                result.append(diff)

            if len(result) > 0:
                smallest_number = min(result)
                smallest_index = result.index(smallest_number)

                x, y, w, h = object_properties[smallest_index]["position"]
                angle = object_properties[smallest_index]["angle"]
                object_properties.pop(smallest_index)
                found.update([x, y, w, h], angle)
            else:
                logging.warning(
                    "no match for found Object %s", found.identifier_number)

        if len(object_properties) > 0:
            logging.warning("contours unused")

    def get_found_object(self, index: int) -> FoundObject:
        """getter for found object"""
        return self.found_objects[index]

    def reset(self):
        """removes all found objects"""
        self.found_objects = []

# Functions ********************************************************************

# Main *************************************************************************
