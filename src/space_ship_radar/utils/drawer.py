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
    def __init__(self):
        self.prev_frame_time = 0
        self.new_frame_time = 0

    @staticmethod
    def _draw_text(frame, txt: str, location: tuple[int, int], color=(100, 100, 100)):
        """helper function to draw a text onto an image"""
        # scales text based on image size
        scaler = frame.shape[0] / 500
        cv2.putText(frame, txt, location, cv2.FONT_HERSHEY_SIMPLEX, .5 *
                    scaler, color, int(scaler))

    @staticmethod
    def _append_if_not_none(key, value):
        return f"{key}: {value} " if value is not None else ""

    def draw_objects(self, found_object_list, frame):
        """Draws every object from an object master"""
        self.new_frame_time = time.time()

        # Calculating the fps

        # fps will be number of frame processed in given time frame
        # since their will be most of time error of 0.001 second
        # we will be subtracting it to get more accurate result
        fps = 1/(self.new_frame_time - self.prev_frame_time)
        self.prev_frame_time = self.new_frame_time

        # converting the fps into integer
        fps = int(fps)

        # converting the fps to string so that we can display it on frame
        # by using putText function
        fps = str(fps)
        print(fps)

        # putting the FPS count on the frame
        self._draw_text(
            frame, fps, (frame.shape[1] - 10, frame.shape[0] - 5), (0, 255, 0))

        for current_found_object_amount, found in enumerate(found_object_list, start=1):

            display_text = ""

            if found["position"] is None:
                return

            # variables
            x, y, w, h = found["position"]
            found_identifier_number = found["identifier_number"]
            found_color = found["color"]

            # draw rectangle
            cv2.rectangle(frame, (x, y),
                          (x+w, y+h), found_color, 2)

            # draws the id above the rectangle
            Drawer._draw_text(frame, str(
                found_identifier_number), (x, y), found_color)

            # write text
            display_text += Drawer._append_if_not_none("P",
                                                       found.get("real_position"))
            display_text += Drawer._append_if_not_none("S", found.get("speed"))
            display_text += Drawer._append_if_not_none("A", found.get("angle"))
            display_text += Drawer._append_if_not_none("T", found.get("type"))

            # scale text based on image size
            scaler = frame.shape[0] / 15
            Drawer._draw_text(frame, display_text,
                              (5, int(current_found_object_amount * scaler)), color=found_color)


# Main *************************************************************************
