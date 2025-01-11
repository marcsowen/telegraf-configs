#!/usr/bin/python3

import json
import sys
from datetime import datetime, timedelta

import requests

station_str="DENI062"

yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
today = datetime.today().strftime("%Y-%m-%d")

response = json.loads(requests.get("https://www.umweltbundesamt.de/api/air_data/v3/airquality/json?date_from="
                                   + yesterday + "&time_from=1&date_to=" + today + "&time_to=24&station=" + station_str)
                      .content.decode('UTF-8'))

formatted_data = []

for station_id, station_data in response["data"].items():
    for timestamp, timestamp_data in station_data.items():
        for sensor_data in timestamp_data[3:]:
            formatted_entry = {
                "timestamp_start": timestamp, # CET
                "timestamp_end": timestamp_data[0], # CET
                "station_id": station_id,
                "sensor_id": sensor_data[0],
                "data_complete": timestamp_data[2],
                "aqi_overall": timestamp_data[1],
                "aqi": float(sensor_data[3]),
                "value": sensor_data[1]
            }
            formatted_data.append(formatted_entry)

json.dump(formatted_data, sys.stdout)
