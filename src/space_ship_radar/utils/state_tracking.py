"""Tracking State

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

from __future__ import annotations
import logging
import cv2
import numpy as np
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

        # setup
        corners, marker_perimeter = Scene.ar_authority.calculate_corners(
            image_bgr)
        image_bgr = Transformer.perspective_transform(image_bgr, corners)

        _, width_px, height_px = Transformer._calculate_matrix(corners)

        cx = width_px / 2.0 # Set center x from left top corner to center x
        cy = height_px / 2.0 # Set center y from left top corner to center y
        Scene.found_object_master.set_origin(cx, cy)

        # ArUco-width
        real_ar_width = cv2.getTrackbarPos("ArUco", "settings")
        real_ar_perimeter = np.float64(real_ar_width) * 4

        Scene.found_object_master.lord_scaler.init(
            marker_perimeter, real_ar_perimeter)
        # end setup

        if Scene.show_debug_windows:
            cv2.namedWindow("Original Video", cv2.WINDOW_NORMAL)
            cv2.imshow("Original Video", image_bgr)

        if Scene.show_debug_windows:
            cv2.namedWindow("Transformed: ", cv2.WINDOW_NORMAL)
            cv2.imshow("Transformed: ", image_bgr)

        Scene.found_object_master.update_list(ObjectFinder.get_ar(image_bgr))

        sample_frame = image_bgr.copy()

        # display results
        Scene.publisher.send(Scene.found_object_master.found_objects)
        ratio = Scene.found_object_master.lord_scaler.ratio
        Scene.drawer.draw_ar(
            Scene.found_object_master.found_objects, sample_frame, ratio)
        cv2.namedWindow('Webots Camera Image', cv2.WINDOW_NORMAL)
        cv2.imshow('Webots Camera Image', sample_frame)
        cv2.waitKey(1)  # waits 1ms to display the image
        field_w_mm = width_px * ratio
        field_h_mm = height_px * ratio
        logging.info(
            f"Field Size: {field_w_mm/1000:.4f}m x {field_h_mm/1000:.4f}m")



# Functions ********************************************************************

# Main *************************************************************************
