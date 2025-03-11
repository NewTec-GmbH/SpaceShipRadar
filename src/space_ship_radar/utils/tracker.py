"""Tracker

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

from time import perf_counter
import keyboard
import cv2

from utils.scene import Scene
from utils.image_getter import ImageGetter
from utils.object_finder import ObjectFinder
from utils.transformer import Transformer
from utils.settings import start_settings
from utils.rotation_director import RotationDirector

# Variables ********************************************************************

# Classes **********************************************************************


class Tracker:
    """Tracker"""

    @staticmethod
    def background(camera):

        start_settings()

        image_bgr = ImageGetter.get_image(camera)

        corners, _ = Scene.ar_authority.calculate_corners(
            image_bgr)
        image_bgr = Transformer.perspective_transform(image_bgr, corners)

        # if cv2.waitKey(0) == ord('b'):
        #     cv2.imwrite("transformed_one.png", image_bgr)
        #     Scene.background_manager.set_background(
        #         cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY))
        # cv2.waitKey(0)

    @staticmethod
    def setup(camera):
        """setup before the main loop"""
        image_bgr = ImageGetter.get_image(camera)

        corners, marker_perimeter = Scene.ar_authority.calculate_corners(
            image_bgr)
        image_bgr = Transformer.perspective_transform(image_bgr, corners)
        Scene.lord_scaler.init(marker_perimeter)

        # cv2.imwrite("transformed_one.png", image_bgr)

        empty = Scene.background_manager.background
        image_bgr = cv2.resize(
            image_bgr, (empty.shape[1], empty.shape[0]))

        boxes = ObjectFinder.get_contours(image_bgr, empty)
        for found_object_index, cnt in enumerate(boxes):
            x, y, w, h = cnt

            # center_point = (int(x+w/2), int(y+h/2))

            # check if the found object is a robot and should be tracked
            # or if it is 'noise' and can be added to the background and therefore
            # will not be considered for the tracking (does only work for static/non-moving obstacles)

            # roi_object = image_bgr[y:y+h, x:x+w]

            # if Scene.found_object_master.is_found_object(image_bgr, (x, y, w, h)):
            angle = RotationDirector.calc_angle(image_bgr, (x, y, w, h))
            Scene.found_object_master.add_found_object(
                found_object_index, (x, y, w, h), angle)
            # else:
            #     # copy the object into the background which will ignore it in the future
            #     Scene.background_manager.copy_region(
            #         image_bgr, (x, y, w, h))
            #     # pass

    @staticmethod
    def tracking(camera):
        """main loop"""
        start = perf_counter()
        if keyboard.is_pressed('s'):  # save image
            cv2.imwrite("image_saved" + str(Scene.save_index) +
                        ".png", ImageGetter.get_image(camera))
            Scene.save_index += 1

        image_bgr = ImageGetter.get_image(camera)

        cv2.namedWindow("Original Video", cv2.WINDOW_NORMAL)
        cv2.imshow("Original Video", image_bgr)

        if keyboard.is_pressed('r'):
            corners, _ = Scene.ar_authority.calculate_corners(image_bgr)
        else:
            corners = Scene.ar_authority.corners
        image_bgr = Transformer.perspective_transform(image_bgr, corners)
        image_bgr = cv2.resize(
            image_bgr, (Scene.background_manager.background.shape[1], Scene.background_manager.background.shape[0]))

        cv2.namedWindow("Transformed: ", cv2.WINDOW_NORMAL)
        cv2.imshow("Transformed: ", image_bgr)

        boxes = ObjectFinder.get_contours(
            image_bgr, Scene.background_manager.background)
        sample_frame = image_bgr.copy()

        found_list = []
        for cnt in boxes:
            x, y, w, h = cnt
            angle = RotationDirector.calc_angle(image_bgr, (x, y, w, h))
            found_list.append({"position": (x, y, w, h), "angle": angle})

        Scene.found_object_master.update_found_object(found_list)

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

        # Scene.publisher.send(found_object_list)
        Scene.drawer.draw_objects(found_object_list, sample_frame)
        cv2.namedWindow('Webots Camera Image', cv2.WINDOW_NORMAL)
        cv2.imshow('Webots Camera Image', sample_frame)

        end = perf_counter()
        print(f"Main Time: {end - start} seconds")

        cv2.waitKey(1)  # waits 1ms to display the image

    # Functions ********************************************************************

    # Main *************************************************************************
