"""Module for Drawing

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import time

import cv2

# Variables ********************************************************************

# Classes **********************************************************************

# Functions ********************************************************************


class Drawer:
    """Drawer"""

    def __init__(self):
        # used for fps calculation
        self.prev_frame_time = 0
        self.new_frame_time = 0

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
        cv2.putText(frame, txt, location, cv2.FONT_HERSHEY_SIMPLEX, .5 *
                    scaler, color, int(scaler))

    @staticmethod
    def _append_if_not_none(key, value) -> str:
        return f"{key}: {value} " if value is not None else ""

    def draw_objects(self, found_object_list, frame):
        """Draws every object from an object master"""
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

        for current_found_object_amount, found_object in enumerate(found_object_list, start=1):

            display_text = ""

            if found_object["position"] is None:
                return

            x, y, w, h = found_object["position"]
            found_identifier_number = found_object["identifier_number"]
            found_color = found_object["color"]

            cv2.rectangle(frame, (x, y),
                          (x+w, y+h), found_color, 2)

            Drawer.draw_text(frame, str(
                found_identifier_number), (x, y), found_color)

            # write text
            display_text += Drawer._append_if_not_none("P",
                                                       found_object.get("real_position"))
            display_text += Drawer._append_if_not_none(
                "S", found_object.get("speed"))
            display_text += Drawer._append_if_not_none(
                "A", found_object.get("angle"))
            display_text += Drawer._append_if_not_none(
                "T", found_object.get("type"))

            # scale text based on image size
            # scaler determines the y-position of the text
            # currently only the top half of the screen
            #   should be used therefore the / 2
            scaler = frame.shape[0] / len(found_object_list) / 2
            Drawer.draw_text(frame, display_text,
                             (5, int(current_found_object_amount * scaler)), color=found_color)


# Main *************************************************************************
