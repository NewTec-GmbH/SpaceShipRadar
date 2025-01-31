"""Module for Drawing"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************


import cv2
from utils.found_object_master import FoundObjectMaster
from utils import drawer

# Functions ********************************************************************


def draw_objet_master(object_master: FoundObjectMaster, frame):
    """Draws every object from an object master"""
    current_found_object_amount: int = 0
    for found in object_master.found_objects:
        current_found_object_amount += 1
        found_speed = found.calculate_speed()

        found_color = found.color
        x, y, w, h = found.current_position[:4]
        cv2.rectangle(frame, (x, y),
                      (x+w, y+h), found_color, 2)

        display_text = f"X: {int(x+w/2)} ; Y: {int(y+h/2)}; Speed {found_speed}"

        # scale text based on image size
        scaler = frame.shape[0] / 300
        drawer.draw_text(frame, display_text,
                         (5, int(20 + current_found_object_amount * scaler * 20)), color=found_color)


def draw_text(frame, txt: str, location: tuple[int, int], color=(100, 100, 100)):
    """helper functino to draw a text onto an image"""
    # scales text based on image size
    scaler = frame.shape[0] / 300
    cv2.putText(frame, txt, location, cv2.FONT_HERSHEY_SIMPLEX, .5 *
                scaler, color, int(1 * scaler))
