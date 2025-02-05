"""Defines the main loop of the programm or core functionality

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import cv2
import keyboard
from utils.found_object_master import FoundObjectMaster
from utils.found_object import FoundObject
from utils.background_manager import BackgroundManager
from utils import drawer
from utils.image_getter import ImageGetter
from utils.object_finder import ObjectFinder

# Variables ********************************************************************

# Classes **********************************************************************


class SpaceShipRadar():
    """Defines the Setup (pre_main) and the Tracking (main_loop)"""
    # save_index is used as a file suffix for saved images
    save_index = 0
    found_object_master = FoundObjectMaster()
    background_manager = BackgroundManager()

    def __init__(self):
        self.save_index: int = 0

    @staticmethod
    def pre_main(camera):
        """setup before the main loop"""

        image_bgr = ImageGetter.get_image(camera)

        empty = SpaceShipRadar.background_manager.get_background()
        contours = ObjectFinder.get_contours(image_bgr, empty)
        for cnt in contours:
            x, y, w, h = cnt
            center_point = (int(x+w/2), int(y+h/2))

            # check if the found object is a roboter and should be tracked
            # or if it is 'noise' and can be added to the background and therefore
            # will not be considered for the tracking (does only work for static/non-moving obstacles)
            if SpaceShipRadar.found_object_master.is_found_object(image_bgr, (x, y, w, h)):
                SpaceShipRadar.found_object_master.add_found_object(
                    FoundObject(0, center_point))
            else:
                SpaceShipRadar.background_manager.copy_region(
                    image_bgr, (x, y, w, h))

    @staticmethod
    def main_loop(camera):
        """main loop"""
        if keyboard.is_pressed('s'):  # save image
            cv2.imwrite("image_saved" + str(SpaceShipRadar.save_index) +
                        ".png", ImageGetter.get_image(camera))
            SpaceShipRadar.save_index += 1

        image_bgr = ImageGetter.get_image(camera)
        contours = ObjectFinder.get_contours(
            image_bgr, SpaceShipRadar.background_manager.get_background())
        sample_frame = image_bgr.copy()

        for cnt in contours:
            x, y, w, h = cnt
            SpaceShipRadar.found_object_master.update_found_object(x, y, w, h)

        found_object_list = []
        for found in SpaceShipRadar.found_object_master.found_objects:
            speed = found.get_speed()
            found_color = found.color
            x, y, w, h = found.current_position[:4]
            found_object_list.append(
                {"speed": speed, "color": found_color, "position": [x, y, w, h]})

        drawer.draw_objects(found_object_list, sample_frame)
        cv2.imshow('Webots Camera Image',
                   cv2.resize(sample_frame, (800, 600)))
        cv2.waitKey(25)  # (1000ms / 40fps = 25)

# Functions ********************************************************************

# Main *************************************************************************


if __name__ == "__main__":
    pass
