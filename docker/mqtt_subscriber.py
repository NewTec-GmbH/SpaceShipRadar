"""MQTT Subscriber (subscribes to the topic ssr/# and prints all results it recieves)

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# source: https://www.emqx.com/en/blog/how-to-use-mqtt-in-python

# Imports **********************************************************************

from multiprocessing import Process
import random
import keyboard

from paho.mqtt import client as mqtt_client


# Variables ********************************************************************

BROKER = '192.168.56.1'
PORT = 1883
TOPIC = "ssr/#"
CLIENT_ID = f'subscribe-{random.randint(0, 100)}'

# Classes **********************************************************************

# Functions ********************************************************************


def _connect_mqtt() -> mqtt_client:
    def on_connect(_client, _userdata, _flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(
        mqtt_client.CallbackAPIVersion.VERSION1, CLIENT_ID)

    client.on_connect = on_connect
    client.connect(BROKER, PORT)
    return client


def _subscribe(client: mqtt_client):
    def on_message(_client, _userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(TOPIC)
    client.on_message = on_message


def run() -> None:
    """subscribes to the topic ssr/# and prints all results it recieves
    """
    client = _connect_mqtt()
    _subscribe(client)
    client.loop_forever()


# Main *************************************************************************
if __name__ == '__main__':
    process = Process(target=run)
    process.start()

    while process.is_alive():
        if keyboard.is_pressed('q'):
            process.terminate()
            break

    print('...')
