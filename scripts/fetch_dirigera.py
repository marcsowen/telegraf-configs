#!/usr/bin/python3

import json
import sys
from datetime import datetime, timedelta

import requests
import urllib3
import yaml

urllib3.disable_warnings()

config = yaml.safe_load(open("/etc/dirigera.yaml"))
headers = {'Authorization': 'Bearer ' + config["access_token"]}
response = json.loads(requests.get("https://" + config["ip"] + ":8443/v1/devices/", headers=headers, verify=False)
                      .content.decode('UTF-8'))

formatted_data = []

for device in response:
    if device["deviceType"] == "environmentSensor":
        attributes = device["attributes"]
        formatted_entry = {
            "timestamp": device["lastSeen"],
            "serialNumber": attributes["serialNumber"],
            "name": attributes["customName"],
            "productCode": attributes["productCode"],
            "firmwareVersion": attributes["firmwareVersion"],
            "hardwareVersion": attributes["hardwareVersion"],
            "currentPM25": attributes["currentPM25"],
            "currentRH": attributes["currentRH"],
            "currentTemperature": attributes["currentTemperature"],
            "maxMeasuredPM25": attributes["maxMeasuredPM25"],
            "minMeasuredPM25": attributes["minMeasuredPM25"],
            "vocIndex": attributes["vocIndex"],
        }

        formatted_data.append(formatted_entry)

json.dump(formatted_data, sys.stdout)