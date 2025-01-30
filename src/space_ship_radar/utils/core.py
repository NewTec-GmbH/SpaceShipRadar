"""Defines the main loop of the programm or core functionality"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import cv2
import keyboard
import utils.helper as helper
from utils.found_object_master import FoundObjectMaster
from utils.found_object import FoundObject
from utils.background_manager import BackgroundManager
import utils.drawer as drawer

# Classes **********************************************************************


class SpaceShipRadar():
    """Class representing a Controller"""
    # save_index is used as a file suffix for saved images
    save_index = 0
    found_object_master = FoundObjectMaster()
    background_manager = BackgroundManager()

    def __init__(self):
        self.save_index: int = 0

    @staticmethod
    def pre_main(camera):
        """setup before the main loop"""

        image_bgr = helper.get_image(camera)

        empty = SpaceShipRadar.background_manager.get_background()
        contours = helper.get_contours(image_bgr, empty)
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            center_point = (int(x+w/2), int(y+h/2))

            # check if the found object is a roboter and should be trackerd
            # or if it is 'noise' and can be added to the background and therefore
            # will not be considered for the tracking (does only work for static/non-moving obsticles)
            if SpaceShipRadar.found_object_master.is_found_object(image_bgr, x, y, w, h):
                SpaceShipRadar.found_object_master.add_found_object(
                    FoundObject(0, center_point))
            else:
                SpaceShipRadar.background_manager.copy_region(
                    image_bgr, x, y, w, h)

    @staticmethod
    def main_loop(camera):
        """main loop"""
        if keyboard.is_pressed('s'):  # save image
            cv2.imwrite("image_saved" + str(SpaceShipRadar.save_index) +
                        ".png", helper.get_image(camera))
            SpaceShipRadar.save_index += 1

        image_bgr = helper.get_image(camera)
        contours = helper.get_contours(
            image_bgr, SpaceShipRadar.background_manager.get_background())
        sample_frame = image_bgr.copy()

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            SpaceShipRadar.found_object_master.update_found_object(x, y, w, h)

        drawer.draw_objet_master(
            SpaceShipRadar.found_object_master, sample_frame)
        cv2.imshow('Webots Camera Image',
                   cv2.resize(sample_frame, (800, 600)))
        cv2.waitKey(25)  # (1000ms / 40fps = 25)


# Main *************************************************************************

if __name__ == "__main__":
    pass
