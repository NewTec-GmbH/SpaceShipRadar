"""Publisher

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import json
import random

from paho.mqtt import client as mqtt_client

from utils.singleton_meta import SingletonMeta
from utils.time_checker import TimeChecker

# Variables ********************************************************************

# Classes **********************************************************************


class Publisher(TimeChecker, metaclass=SingletonMeta):
    """Publisher"""

    def __init__(self):
        super().__init__()
        self.broker = '192.168.56.1'
        self.port = 1883
        self.topic = "ssr/"

        self.client_id = f'publish-{random.randint(0, 1000)}'

        self._client = None
        self._last_call_time = None

        self._connected = True

    def _connect_mqtt(self) -> mqtt_client:
        """tries to connect to MQTT broker"""
        def on_connect(_client, _userdata, _flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(
            mqtt_client.CallbackAPIVersion.VERSION1, self.client_id)

        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def _publish(self, client: mqtt_client, msg_content, topic_level: int = "42"):
        """sends the message to the client with the topic level"""

        msg = f"{msg_content}"
        result = client.publish(f"{self.topic}{topic_level}", msg)

        status = result[0]
        if status == 0:
            pass
        else:
            print(f"Failed to send message to topic {self.topic}")

    def _send_message(self, msg_json, topic_level: str) -> bool:
        """connects to mqtt broker and sends message 

        Returns:
            bool: returns True if successful otherwise False
        """

        # check if connection can be established
        if self._client is None:
            try:
                self._client = self._connect_mqtt()
            except ConnectionRefusedError as e:
                print(e)
                return False

            if self._client is None:
                return False

        # send message
        self._client.loop_start()
        self._publish(self._client, msg_json, topic_level)
        self._client.loop_stop()
        return True

    @staticmethod
    def json_builder(position, speed, angle: int) -> str:
        """creates a json element with:
            - positionX
            - positionY
            - speedX
            - speedY
            - angle
        """
        position_x, position_y = position
        speed_x, speed_y = speed

        message_dict = {
            "positionX": position_x,
            "positionY": position_y,
            "speedX": speed_x,
            "speedY": speed_y,
            "angle": angle,
        }

        return json.dumps(message_dict)

    def send(self, found_objects):
        """sends for each list entry of found_objects a message to the MQTT broker

        Args:
            found_objects (dict): for each object stores information about:
                                        - identifier_number
                                        - real_postion
                                        - speed
                                        - angle
                                        - ratio
        """

        if self._connected is False:
            return

        if not self._check_time():
            return

        for identifier, found_object in found_objects.items():
            current_position = (found_object.position_x,
                                found_object.position_y)

            speed = (found_object.speed_x, found_object.speed_y)

            angle = found_object.angle

            msg_json_ = self.json_builder(
                current_position, speed, angle)
            self._connected = self._send_message(
                msg_json_, str(identifier))


# Functions ********************************************************************

# Main *************************************************************************
