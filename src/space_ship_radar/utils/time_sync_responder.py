"""MQTT time synchronization responder.

Author: Tobias Haeckel (tobias.haeckel@gmx.net)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

from __future__ import annotations

import json
import logging
import os
import time
from dataclasses import dataclass
from typing import Optional, Protocol, runtime_checkable

from paho.mqtt import client as mqtt_client


@runtime_checkable
class TimeSource(Protocol): # pylint: disable=too-few-public-methods
    """Interface for time providers."""

    def now_ms(self) -> int:
        """Return current time in milliseconds."""


@dataclass
class WallClockTimeSource(TimeSource): # pylint: disable=too-few-public-methods
    """Epoch-based time source."""

    def now_ms(self) -> int:
        return int(time.time() * 1000)


class WebotsSimulationTimeSource(TimeSource): # pylint: disable=too-few-public-methods
    """Time source backed by the Webots simulation clock."""

    def __init__(self, robot) -> None:
        self._robot = robot

    def now_ms(self) -> int:
        return int(float(self._robot.getTime()) * 1000)


def auto_time_source(robot: Optional[object] = None) -> TimeSource:
    """Choose the best available time source.

    If a Webots Robot instance is provided, simulation time is used.
    Otherwise, epoch time is returned.
    """
    if robot is not None and hasattr(robot, "getTime"):
        try:
            # Validate that the robot instance can deliver simulation time.
            robot.getTime()
        except Exception as exc: # pylint: disable=broad-except
            logging.debug("TimeSync: Falling back to wall clock: %s", exc)
        else:
            return WebotsSimulationTimeSource(robot)

    if os.getenv("WEBOTS_ROBOT_NAME"):
        logging.info(
            "TimeSync: WEBOTS_ROBOT_NAME is set but no robot instance was provided; "
            "falling back to wall clock time."
        )
    return WallClockTimeSource()


class HostTimeSyncResponder:
    """Host-side MQTT responder for Zumo/ESP time synchronization."""

    def __init__(
        self,
        broker: str = "localhost",
        port: int = 1883,
        time_source: Optional[TimeSource] = None,
        use_background_loop: bool = False,
    ) -> None:
        self._broker = broker
        self._port = port
        self._use_background_loop = use_background_loop

        self._req_topic_filter = "+/zumo/time_sync/request"
        self._time_source = time_source or WallClockTimeSource()

        client_id = "host-timesync-responder"
        self._client = mqtt_client.Client(
            mqtt_client.CallbackAPIVersion.VERSION1, client_id
        )
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message

        self._connected = False

    def start(self) -> bool:
        """Connect to the MQTT broker and prepare message handling."""
        try:
            self._client.connect(self._broker, self._port)
        except OSError as exc:
            logging.warning(
                "TimeSync: Failed to connect to MQTT broker %s:%d (%s)",
                self._broker,
                self._port,
                exc,
            )
            return False

        self._connected = True

        if self._use_background_loop:
            self._client.loop_start()

        return True

    def stop(self) -> None:
        """Stop MQTT network handling."""
        if not self._connected:
            return

        if self._use_background_loop:
            self._client.loop_stop()

        self._client.disconnect()
        self._connected = False

    def loop(self, timeout: float = 0.0) -> None:
        """Run one iteration of the MQTT network loop."""
        if not self._connected or self._use_background_loop:
            return

        # timeout=0.0 -> non-blocking; keeps Webots simulation responsive.
        self._client.loop(timeout=timeout)

    def _on_connect(self, client, _userdata, _flags, rc) -> None:
        """Handle MQTT connect callback."""
        if rc == 0:
            logging.info("TimeSync: Connected to MQTT broker.")
            logging.info(
                "TimeSync: Subscribing to %s", self._req_topic_filter
            )
            client.subscribe(self._req_topic_filter)
        else:
            logging.error("TimeSync: MQTT connect failed with rc=%d", rc)

    def _on_message(self, _client, _userdata, msg) -> None:
        """Handle inbound MQTT messages."""
        topic = msg.topic
        payload = msg.payload.decode("utf-8", errors="replace")

        parts = topic.split("/")
        if (
            len(parts) != 4
            or parts[1] != "zumo"
            or parts[2] != "time_sync"
            or parts[3] != "request"
        ):
            logging.debug("TimeSync: Ignoring message on topic %s", topic)
            return

        robot_name = parts[0]
        self._handle_time_sync_request(robot_name, payload)

    def _handle_time_sync_request(self, robot_name: str, payload: str) -> None:
        """Process a time sync request payload."""
        t2_host_ms = self._time_source.now_ms()

        try:
            data = json.loads(payload)
        except json.JSONDecodeError as exc:
            logging.warning("TimeSync: Failed to parse JSON: %s", exc)
            return

        if "seq" not in data or "t1_esp_ms" not in data:
            logging.warning("TimeSync: Missing 'seq' or 't1_esp_ms' in request.")
            return

        seq = int(data["seq"])
        t1_esp_ms = int(data["t1_esp_ms"])

        rsp_topic = f"{robot_name}/zumo/time_sync/response"
        t3_host_ms = self._time_source.now_ms()

        rsp = {
            "seq": seq,
            "t1_esp_ms": t1_esp_ms,
            "t2_host_ms": t2_host_ms,
            "t3_host_ms": t3_host_ms,
        }

        rsp_json = json.dumps(rsp, separators=(",", ":"))
        result = self._client.publish(rsp_topic, rsp_json)

        if result.rc == mqtt_client.MQTT_ERR_SUCCESS:
            logging.info(
                "[%s] TimeSync response sent: seq=%d t1=%d t2=%d t3=%d",
                robot_name,
                seq,
                t1_esp_ms,
                t2_host_ms,
                t3_host_ms,
            )
        else:
            logging.warning(
                "[%s] TimeSync: Failed to publish response (rc=%d) for seq=%d",
                robot_name,
                result.rc,
                seq,
            )


# Functions ********************************************************************

# Main *************************************************************************
