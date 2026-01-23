#!/usr/bin/python3

import json
import sys

import requests

sensor_id="37895"

response = json.loads(requests.get("https://data.sensor.community/airrohr/v1/sensor/" + sensor_id + "/")
                      .content.decode('UTF-8'))

formatted_data = []

for entry in response:
    timestamp = entry.get("timestamp")
    sensordatavalues = entry.get("sensordatavalues", [])

    for value in sensordatavalues:
        value_type = value.get("value_type")
        measurement = float(value.get("value", 0))

        formatted_entry = {
                "timestamp": timestamp,
                "sensor_id": sensor_id,
                "sensor_type": value_type,
                "measurement": measurement
        }

        formatted_data.append(formatted_entry)

json.dump(formatted_data, sys.stdout)
