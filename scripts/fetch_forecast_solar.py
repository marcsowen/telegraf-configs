#!/usr/bin/python3

import json
import sys

import requests

response = json.loads(requests.get("https://api.forecast.solar/estimate/watts/53.254089/10.429055/20/0/8.8?time=utc")
                      .content.decode('UTF-8'))

formatted_data = []

for time_str, watts in response["result"].items():
    formatted_entry = {
        "timestamp": time_str,
        "watts": watts,
    }
    formatted_data.append(formatted_entry)

json.dump(formatted_data, sys.stdout)
