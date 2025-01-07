#!/usr/bin/python3

import sys
import json
import requests

region_codes = ['03355', '03355022']

formatted_data = []

for region_code in region_codes:
    response = json.loads(requests.get('https://api-energiemonitor.eon.com/meter-data?regionCode=' + region_code)
                          .content.decode('UTF-8'))

    autarky = float(response["autarky"])
    daily_co2_savings = float(response["dailyCo2Savings"])
    total_consumption = float(response["consumptions"]["total"]) * 4
    total_feed_in = float(response["feedIn"]["total"]) * 4
    feed_in_external = max(total_consumption - total_feed_in, 0)
    consumption_external = max(total_feed_in - total_consumption, 0)

    for consumption in response['consumptions']['list']:
        formatted_entry = {
            "timestamp": int(consumption.get("timestamp")),
            "regionCode": region_code,
            "type": "consumption",
            "name": consumption.get("name"),
            "usage": float(consumption.get("usage")) * 4,
            "numberOfInstallations": int(consumption.get("numberOfInstallations")),
            "autarky": autarky,
            "dailyCo2Savings": daily_co2_savings
        }

        formatted_data.append(formatted_entry)

    external_consumption_entry = {
        "timestamp": int(response["timestamp"]["start"]),
        "regionCode": region_code,
        "type": "consumption",
        "name": "external",
        "usage": consumption_external,
        "autarky": autarky,
        "dailyCo2Savings": daily_co2_savings
    }

    formatted_data.append(external_consumption_entry)

    for feed_in in response['feedIn']['list']:
        formatted_entry = {
            "timestamp": int(feed_in.get("timestamp")),
            "regionCode": region_code,
            "type": "feedIn",
            "name": feed_in.get("name"),
            "usage": float(feed_in.get("usage")) * 4,
            "numberOfInstallations": int(feed_in.get("numberOfInstallations")),
            "installedCapacity": float(feed_in.get("installedCapacity")),
            "autarky": autarky,
            "dailyCo2Savings": daily_co2_savings
        }

        formatted_data.append(formatted_entry)

    external_feed_in_entry = {
        "timestamp": int(response["timestamp"]["start"]),
        "regionCode": region_code,
        "type": "feedIn",
        "name": "external",
        "usage": feed_in_external,
        "autarky": autarky,
        "dailyCo2Savings": daily_co2_savings
    }

    formatted_data.append(external_feed_in_entry)

json.dump(formatted_data, sys.stdout)

