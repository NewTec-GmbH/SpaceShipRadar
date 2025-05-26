"""Module for Drawing

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import time

import cv2
import numpy as np

# Variables ********************************************************************

# Classes **********************************************************************

# Functions ********************************************************************


class Drawer:
    """Drawer"""

    def __init__(self):
        # used for fps calculation
        self.prev_frame_time = 0
        self.new_frame_time = 0
        self._color_list = []
        for _ in range(50):
            self._color_list.append(
                np.random.randint(50, 200, (1, 3))[0].tolist())

    @staticmethod
    def draw_text(frame, txt: str, location: tuple[int, int], color=(100, 100, 100)):
        """helper function to draw a text onto an image

        Args:
            frame (np.array): image in which the text should be written
            txt (str): new text which is added in the image
            location (tuple[int, int]): location of new text
            color (tuple, optional): color of text. Defaults to (100, 100, 100) [Gray].
        """

        # scales text based on image size
        scaler = frame.shape[0] / 500
        cv2.putText(frame, txt, location, cv2.FONT_HERSHEY_SIMPLEX, 0.7 *
                    scaler, color, 1 * int(scaler))

    @staticmethod
    def _append_if_not_none(key, value) -> str:
        return f"{key}: {value} " if value is not None else ""

    def _draw_fps(self, frame):
        self.new_frame_time = time.time()

        # Calculating the fps from:
        # (https://www.geeksforgeeks.org/
        # python-displaying-real-time-fps-at-which-webcam-video-file-is-processed-using-opencv/)

        # just to be safe
        try:
            fps = 1/(self.new_frame_time - self.prev_frame_time)
        except ZeroDivisionError:
            fps = -1

        self.prev_frame_time = self.new_frame_time

        fps = str(int(fps))

        # putting the FPS count on the frame
        # put the text in the bottom right corner and slightly to the center
        # slightly is in this case -100 in x-direction and -25 in the -y-direction
        self.draw_text(
            frame, fps, (frame.shape[1] - 100, frame.shape[0] - 25), (0, 255, 0))

    def draw_ar(self, found_objects, frame, ratio):
        """Draws every object from an object master"""

        self._draw_fps(frame)

        for current_found_object_amount, (identifier, found_object) in enumerate(
                sorted(found_objects.items(), key=lambda item: item[0]), start=1):
            display_text = ""

            x = found_object.position_x
            y = found_object.position_y

            found_identifier_number = identifier
            found_color = self._color_list[found_identifier_number]

            pixel_x = x / ratio
            pixel_y = y / ratio

            Drawer.draw_text(frame, str(
                found_identifier_number), (int(round(pixel_x, 1)), int(round(pixel_y, 1))), found_color)

            display_text += Drawer._append_if_not_none("P",
                                                       (x, y))
            display_text += Drawer._append_if_not_none(
                "S", (found_object.speed_x, found_object.speed_y))
            # display_text += Drawer._append_if_not_none(
            #     "A", round(found_object.get("angle"), 2))
            display_text += Drawer._append_if_not_none(
                "A", round(found_object.angle, 1))
            display_text += Drawer._append_if_not_none(
                "ID", found_identifier_number)

            # scale text based on image size
            # scaler determines the y-position of the text
            # currently only the top half of the screen
            #   should be used therefore the / 2
            # the scaler should be max 100 (100 is a magic number)
            scaler = min(frame.shape[0] / len(found_objects) / 2, 100)
            Drawer.draw_text(frame, display_text,
                             (5, int(current_found_object_amount * scaler)), color=found_color)


# Main *************************************************************************
