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
            "id": device.get("id"),
            "timestamp": device.get("lastSeen"),
            "serialNumber": attributes.get("serialNumber"),
            "name": attributes.get("customName"),
            "productCode": attributes.get("productCode"),
            "firmwareVersion": attributes.get("firmwareVersion"),
            "hardwareVersion": attributes.get("hardwareVersion"),
            "currentPM25": attributes.get("currentPM25"),
            "currentRH": attributes.get("currentRH"),
            "currentCO2": attributes.get("currentCO2"),
            "currentTemperature": attributes.get("currentTemperature"),
            "maxMeasuredPM25": attributes.get("maxMeasuredPM25"),
            "minMeasuredPM25": attributes.get("minMeasuredPM25"),
            "maxMeasuredCO2": attributes.get("maxMeasuredCO2"),
            "minMeasuredCO2": attributes.get("minMeasuredCO2"),
            "vocIndex": attributes.get("vocIndex"),
        }

        formatted_data.append(formatted_entry)

json.dump(formatted_data, sys.stdout)
