#!/usr/bin/python3

import json
import sys

import requests

response = json.loads(requests.get("http://192.168.178.65/rpc/Shelly.GetStatus")
                      .content.decode('UTF-8'))

formatted_data = []

for sw_id in range(4):
    switch = response["switch:" + str(sw_id)]
    formatted_entry = {
        "timestamp": response["sys"]["unixtime"],
        "mac": response["sys"]["mac"],
        "uptime": response["sys"]["uptime"],
        "wifi_rssi": response["wifi"]["rssi"],
        "switch_id": sw_id,
        "output": 1 if switch["output"] == True else 0,
        "apower": switch["apower"],
        "voltage": switch["voltage"],
        "freq": switch["freq"],
        "current": switch["current"],
        "pf": switch["pf"],
        "aenergy": switch["aenergy"]["total"],
        "ret_aenergy": switch["ret_aenergy"]["total"],
        "temperature": switch["temperature"]["tC"],
    }

    formatted_data.append(formatted_entry)

json.dump(formatted_data, sys.stdout)