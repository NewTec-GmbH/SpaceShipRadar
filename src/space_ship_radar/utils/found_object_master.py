"""Found Object Master"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import cv2
import utils.helper as helper
from utils.found_object import FoundObject

# Classes **********************************************************************


class FoundObjectMaster:
    """Found Object Master manages multiple Found Objects"""

    def __init__(self):
        self.found_objects: list[FoundObject] = []

    def is_found_object(self, image, x, y, w, h) -> bool:
        """determins if the picture is a object which should be tracked"""
        source_image = image.copy()

        # Extract the region of interest (ROI) from the source image
        roi = source_image[y:y+h, x:x+w]

        hist = helper.get_hist(roi)
        diff = cv2.compareHist(helper.get_robo_hist(),
                               hist, cv2.HISTCMP_CORREL)

        if diff < 0.5:
            return False

        return True

    def add_found_object(self, found_o: FoundObject) -> bool:
        """adder for Found Objects"""
        self.found_objects.append(found_o)
        return True

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

    def update_found_object(self, x: int, y: int, w: int, h: int) -> int:
        """updates the position of the best match"""
        center_point = (int(x+w/2), int(y+h/2))

        index = self.get_best_match(center_point)
        if index == -1:
            return -1

        # Update position of found objects
        self.get_found_object(index).add_previous_point(center_point)
        self.get_found_object(index).update_position(x, y, w, h)

        return index

    def get_found_object(self, index: int) -> FoundObject:
        """getter for found object"""
        return self.found_objects[index]
