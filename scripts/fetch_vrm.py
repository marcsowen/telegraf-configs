#!/usr/bin/python3
import json
import sys
from datetime import datetime, timedelta

import requests
import yaml

config = yaml.safe_load(open("/etc/vrm.yaml"))
headers = {'X-Authorization': 'Token ' + config["access_token"]}
in_two_days = datetime.today() + timedelta(days=2)
in_two_days_ms = in_two_days.timestamp()

response = json.loads(requests.get("https://vrmapi.victronenergy.com/v2/installations/" + str(config["installation_id"])
                                   + "/stats?end=" + str(in_two_days_ms) + "&interval=hours&type=forecast", headers=headers)
                      .content.decode('UTF-8'))

formatted_data = []

for entry in response["records"]["solar_yield_forecast"]:
    formatted_entry = {
        "timestamp": entry[0],
        "solar_yield_forecast": entry[1],
    }

    formatted_data.append(formatted_entry)

json.dump(formatted_data, sys.stdout)