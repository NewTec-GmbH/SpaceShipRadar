"""Tracking State

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

from __future__ import annotations
from time import perf_counter
import cv2
import keyboard

from utils.transformer import Transformer
from utils.object_finder import ObjectFinder
from utils.image_getter import ImageGetter
from utils.state import State
from utils.scene import Scene

# Variables ********************************************************************

# Classes **********************************************************************


class TrackingState(State):
    """main loop"""

    def __init__(self):
        super().__init__()
        self.name = "TrackingState"

    def run(self, camera) -> None:
        """update the position of all found_objects
            Also:
                - the user can create a screenshot with the s-key
                - or reset the background and search for objects again with the b-key"""
        # save image
        if keyboard.is_pressed('s'):  # save image
            cv2.imwrite("image_saved" + str(Scene.save_index) +
                        ".png", ImageGetter.get_image(camera))
            Scene.save_index += 1

        image_bgr = ImageGetter.get_image(camera)

        cv2.namedWindow("Original Video", cv2.WINDOW_NORMAL)
        cv2.imshow("Original Video", image_bgr)

        corners = Scene.ar_authority.marker_corners

        image_bgr = Transformer.perspective_transform(image_bgr, corners)
        cv2.namedWindow("Transformed: ", cv2.WINDOW_NORMAL)
        cv2.imshow("Transformed: ", image_bgr)

        aruco_list = ObjectFinder.get_ar(image_bgr)

        # scale coordinates
        for identifier, found_object in aruco_list.items():
            r_x = Scene.lord_scaler.convert(found_object.position_x)
            r_y = Scene.lord_scaler.convert(found_object.position_y)

            found_object.position_x = r_x
            found_object.position_y = r_y

            if (Scene.previous_aruco_list is not None) and identifier in Scene.previous_aruco_list:
                x_diff = found_object.position_x - \
                    Scene.previous_aruco_list[identifier].position_x
                y_diff = found_object.position_y - \
                    Scene.previous_aruco_list[identifier].position_y

                time_diff = perf_counter() - Scene.last_speed_calculation_time

                found_object.speed_x = round(x_diff / time_diff, 2)
                found_object.speed_y = round(y_diff / time_diff, 2)

        Scene.previous_aruco_list = aruco_list
        Scene.last_speed_calculation_time = perf_counter()

        if keyboard.is_pressed('d'):
            print("------")
            for entry in aruco_list:
                print(f"{entry['real_position']} & {round(entry['angle'],2)}")
            print("------")

        sample_frame = image_bgr.copy()

        # display results
        # Scene.publisher.send(aruco_list.copy())
        ratio = Scene.lord_scaler.ratio
        Scene.drawer.draw_ar(aruco_list, sample_frame, ratio)
        cv2.namedWindow('Webots Camera Image', cv2.WINDOW_NORMAL)
        cv2.imshow('Webots Camera Image', sample_frame)
        cv2.waitKey(1)  # waits 1ms to display the image

# Functions ********************************************************************

# Main *************************************************************************
