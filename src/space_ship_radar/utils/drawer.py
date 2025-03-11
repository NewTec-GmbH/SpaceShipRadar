"""Module for Drawing

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************


import cv2

# Variables ********************************************************************

# Classes **********************************************************************

# Functions ********************************************************************


def draw_text(frame, txt: str, location: tuple[int, int], color=(100, 100, 100)):
    """helper function to draw a text onto an image"""
    # scales text based on image size
    scaler = frame.shape[0] / 500
    cv2.putText(frame, txt, location, cv2.FONT_HERSHEY_SIMPLEX, .5 *
                scaler, color, int(scaler))


def _append_if_not_none(key, value):
    return f"{key}: {value} " if value is not None else ""


def draw_objects(found_object_list, frame):
    """Draws every object from an object master"""
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
        draw_text(frame, str(found_identifier_number), (x, y), found_color)

        # write text
        display_text += _append_if_not_none("P", found.get("real_position"))
        display_text += _append_if_not_none("S", found.get("speed"))
        display_text += _append_if_not_none("A", found.get("angle"))
        display_text += _append_if_not_none("T", found.get("type"))

        # scale text based on image size
        scaler = frame.shape[0] / 15
        draw_text(frame, display_text,
                  (5, int(current_found_object_amount * scaler)), color=found_color)


# Main *************************************************************************
