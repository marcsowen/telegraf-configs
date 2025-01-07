#!/usr/bin/python3

import json
import sys
from datetime import timedelta, datetime

import requests

next_day = datetime.today() + timedelta(days=1)
response = json.loads(requests.get("https://api.energy-charts.info/price?bzn=DE-LU&end=" + next_day.strftime("%Y-%m-%d")).content.decode('UTF-8'))

formatted_data = [
    {"time": ts, "price": (price / 1000 * 1.19) + 0.1978}
    for ts, price in zip(response["unix_seconds"], response["price"])
]

json.dump(formatted_data, sys.stdout)

