"""Publisher

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import time
import json
import random

from paho.mqtt import client as mqtt_client

from utils.singleton_meta import SingletonMeta

# Variables ********************************************************************

# Classes **********************************************************************


class Publisher(metaclass=SingletonMeta):

    def __init__(self):
        self.broker = '192.168.56.1'
        self.port = 1883
        self.topic = "ssr/"

        # Generate a Client ID with the publish prefix.
        self.client_id = f'publish-{random.randint(0, 1000)}'

        self._client = None
        self._last_call_time = None

        self._connected = True

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(
            mqtt_client.CallbackAPIVersion.VERSION1, self.client_id)
        # client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def publish(self, client, msg_content, topic_level="42"):

        msg = f"{msg_content}"
        result = client.publish(f"{self.topic}{topic_level}", msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            # print(f"Send `{msg}` to topic `{self.topic}`")
            pass
        else:
            print(f"Failed to send message to topic {self.topic}")

    def run(self, msg_json, topic_level: str) -> bool:

        # check if connection can be established
        try:
            self._client = self.connect_mqtt()
        except ConnectionRefusedError as e:
            #  socket.gaierror as e:
            print(e)
            return False

        if self._client is None:
            return False

        # send message
        self._client.loop_start()
        self.publish(self._client, msg_json, topic_level)
        self._client.loop_stop()
        return True

    @staticmethod
    def json_builder(position_x: int, position_y: int,
                     speed_x: int, speed_y: int, angle: int, error_code: int) -> str:
        message_dict = {
            "positionX": position_x,
            "positionY": position_y,
            "speedX": speed_x,
            "speedY": speed_y,
            "angle": angle,
            "errorCode": error_code
        }

        return json.dumps(message_dict)

    def send(self, found_object_list):

        if self._connected is False:
            return

        if not self._check_time():
            return

        for found in found_object_list:
            # variables
            # identifier_number
            identifier_number = found.get("identifier_number")
            if identifier_number is None:
                return

            # position
            current_position = found["real_position"]
            x, y = current_position

            # speed
            speed = found["speed"]

            # angle
            angle = found["angle"]

            # error code
            ratio = found["ratio"]
            if ratio == 1:
                error_code = 1
            else:
                error_code = 0

            msg_json_ = self.json_builder(
                x, y, speed[0], speed[1], angle, error_code)
            publisher = Publisher()
            self._connected = publisher.run(msg_json_, str(identifier_number))

    def _check_time(self) -> bool:
        current_time = time.time()

        if self._last_call_time is None:
            self._last_call_time = current_time
            return False

        elapsed_time = current_time - self._last_call_time

        if elapsed_time >= 1:
            self._last_call_time = current_time
            return True
        else:
            return False


# Functions ********************************************************************

# Main *************************************************************************
