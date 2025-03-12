"""Tracking State

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

from __future__ import annotations
from utils.rotation_director import RotationDirector
from utils.transformer import Transformer
from utils.object_finder import ObjectFinder
from utils.image_getter import ImageGetter
from utils.state import State
from utils.scene import Scene
from time import perf_counter

import cv2
import keyboard

# import sys
# BackgroundState = sys.modules[__package__ + ".state_background"]


# Variables ********************************************************************

# Classes **********************************************************************


class TrackingState(State):
    """main loop"""

    def __init__(self):
        super().__init__()
        self.name = "TrackingState"

    def run(self, camera) -> None:
        """tracking ..."""
        if keyboard.is_pressed('s'):  # save image
            cv2.imwrite("image_saved" + str(Scene.save_index) +
                        ".png", ImageGetter.get_image(camera))
            Scene.save_index += 1

        # start_image = perf_counter()
        image_bgr = ImageGetter.get_image(camera)
        # end_image = perf_counter()
        # print(f'Time to image: {end_image - start_image} seconds')
        # start = perf_counter()

        cv2.namedWindow("Original Video", cv2.WINDOW_NORMAL)
        cv2.imshow("Original Video", image_bgr)

        if keyboard.is_pressed('b'):
            from utils.state_background import BackgroundState
            self.context.transition_to(BackgroundState())
            return
        else:
            # corners = Scene.ar_authority.corners
            corners, _ = Scene.ar_authority.calculate_corners(image_bgr)

        image_bgr = Transformer.perspective_transform(image_bgr, corners)
        cv2.namedWindow("Transformed: ", cv2.WINDOW_NORMAL)
        cv2.imshow("Transformed: ", image_bgr)

        image_bgr = cv2.resize(
            image_bgr, (Scene.background_manager.background.shape[1], Scene.background_manager.background.shape[0]))

        boxes = ObjectFinder.get_contours(
            image_bgr, Scene.background_manager.background)
        sample_frame = image_bgr.copy()

        found_list = []
        for cnt in boxes:
            x, y, w, h = cnt
            angle = RotationDirector.calc_angle(image_bgr, (x, y, w, h))
            found_list.append({"position": (x, y, w, h), "angle": angle})

        Scene.found_object_master.update_found_object(found_list)
        # end = perf_counter()
        # print(f'Time before list: {end - start} seconds')

        # create list for drawer
        found_object_list = []
        for found in Scene.found_object_master.found_objects:
            speed = found.get_speed()
            speed = tuple(map(Scene.lord_scaler.convert, speed))
            found_color = found.color
            x, y, w, h = found.current_position[:4]
            r_x = Scene.lord_scaler.convert(x)
            r_y = Scene.lord_scaler.convert(y)
            ratio = Scene.lord_scaler.ratio
            found_identifier_number = found.identifier_number
            found_angle = found.angle
            # found_type = found.texture

            found_object_list.append(
                {"speed": speed, "color": found_color, "position": [x, y, w, h],
                 "identifier_number": found_identifier_number, "angle": found_angle,
                 "real_position": (r_x, r_y), "ratio": ratio})

        # Scene.publisher.send(found_object_list.copy())
        Scene.drawer.draw_objects(found_object_list, sample_frame)
        cv2.namedWindow('Webots Camera Image', cv2.WINDOW_NORMAL)
        cv2.imshow('Webots Camera Image', sample_frame)

        cv2.waitKey(1)  # waits 1ms to display the image

# Functions ********************************************************************

# Main *************************************************************************
