""""Real Test

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import logging
import cv2
import keyboard
from utils.state import Context
from utils.state_configuration import ConfigurationState
from utils.image_getter import ImageGetter
from utils.scene import Scene
from utils.time_sync_responder import HostTimeSyncResponder, auto_time_source

# Variables ********************************************************************

# Classes **********************************************************************

# Functions ********************************************************************


def run() -> None:
    """run SSR for a real camera"""
    # Main Loop
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s")
    # Setup
    Scene.publisher.set_time_source(auto_time_source())
    time_sync_responder = HostTimeSyncResponder(
        time_source=auto_time_source(),
        use_background_loop=True,
    )
    if not time_sync_responder.start():
        logging.warning("TimeSync responder could not start; continuing without MQTT sync.")

    context = Context(ConfigurationState())
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FPS, 30)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)



    try:
        while True:
            context.update(camera)
            if keyboard.is_pressed('q'):  # quit
                break
            if keyboard.is_pressed('s'):
                ret, frame = camera.read()
                if ret:
                    cv2.imwrite("real_empty.png", frame)
    finally:
        camera.release()
        cv2.destroyAllWindows()
        time_sync_responder.stop()


def run_record() -> None:
    """Debug function to record a video"""
    width = 1920
    height = 1440
    cam = cv2.VideoCapture(1)

    video_output_file_name = 'real_video_output.mp4'
    video_out = cv2.VideoWriter(
        video_output_file_name, -1, 40, (width, height))

    logging.error('video recording starts ...')

    while True:
        logging.error("waiting...")
        if keyboard.is_pressed('s'):
            break

    while True:
        frame = ImageGetter.get_image(cam)

        video_out.write(frame)

        if keyboard.is_pressed('q'):
            logging.error("exit video 1")
            break

    video_out.release()

# Main *************************************************************************


if __name__ == "__main__":
    run()
