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


def draw_objects(found_object_list, frame):
    """Draws every object from an object master"""
    for current_found_object_amount, found in enumerate(found_object_list, start=1):

        found_speed = found["speed"]
        found_color = found["color"]
        x, y, w, h = found["position"]
        found_identifier_number = found["identifier_number"]
        found_angle = found["angle"]

        cv2.rectangle(frame, (x, y),
                      (x+w, y+h), found_color, 2)

        # draws the id above the rectangle
        draw_text(frame, str(found_identifier_number), (x, y), found_color)

        display_text = f"X: {int(x+w/2)} ; Y: {int(y+h/2)}; Speed {found_speed}; Angle {found_angle}"

        # scale text based on image size
        scaler = frame.shape[0] / 15
        draw_text(frame, display_text,
                  (5, int(current_found_object_amount * scaler)), color=found_color)


# Main *************************************************************************
