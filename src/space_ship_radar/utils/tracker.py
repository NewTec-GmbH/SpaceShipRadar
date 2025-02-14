"""Tracker

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import keyboard
import cv2

from utils.scene import Scene
from utils.image_getter import ImageGetter
from utils.object_finder import ObjectFinder
from utils import drawer
from utils.transformer import Transformer

# Variables ********************************************************************

# Classes **********************************************************************


class Tracker:
    """Tracker"""

    @staticmethod
    def setup(camera):
        """setup before the main loop"""

        image_bgr = ImageGetter.get_image(camera)
        corners = Scene.ar_authority.calculate_corners(image_bgr)
        image_bgr = Transformer.perspective_transform(image_bgr, corners)

        empty = Scene.background_manager.background

        contours = ObjectFinder.get_contours(image_bgr, empty)
        for found_object_index, cnt in enumerate(contours):
            x, y, w, h = cnt
            center_point = (int(x+w/2), int(y+h/2))

            # check if the found object is a robot and should be tracked
            # or if it is 'noise' and can be added to the background and therefore
            # will not be considered for the tracking (does only work for static/non-moving obstacles)
            if Scene.found_object_master.is_found_object(image_bgr, (x, y, w, h)):
                Scene.found_object_master.add_found_object(
                    found_object_index, center_point)
            else:
                Scene.background_manager.copy_region(
                    image_bgr, (x, y, w, h))

    @staticmethod
    def tracking(camera):
        """main loop"""
        if keyboard.is_pressed('s'):  # save image
            cv2.imwrite("image_saved" + str(Scene.save_index) +
                        ".png", ImageGetter.get_image(camera))
            Scene.save_index += 1

        image_bgr = ImageGetter.get_image(camera)

        cv2.namedWindow("Original Video", cv2.WINDOW_NORMAL)
        cv2.imshow("Original Video", image_bgr)

        corners = Scene.ar_authority.corners
        image_bgr = Transformer.perspective_transform(image_bgr, corners)

        contours = ObjectFinder.get_contours(
            image_bgr, Scene.background_manager.background)
        sample_frame = image_bgr.copy()

        for cnt in contours:
            x, y, w, h = cnt
            Scene.found_object_master.update_found_object(x, y, w, h)

        # create list for drawer
        found_object_list = []
        for found in Scene.found_object_master.found_objects:
            speed = found.get_speed()
            found_color = found.color
            x, y, w, h = found.current_position[:4]
            found_identifier_number = found.identifier_number

            found_object_list.append(
                {"speed": speed, "color": found_color, "position": [x, y, w, h],
                 "identifier_number": found_identifier_number})

        drawer.draw_objects(found_object_list, sample_frame)
        cv2.imshow('Webots Camera Image',
                   cv2.resize(sample_frame, (800, 600)))
        cv2.waitKey(1)  # waits 1ms to display the image

    # Functions ********************************************************************

    # Main *************************************************************************
