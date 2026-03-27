#!/usr/bin/python3

import json
import sys

import requests
import yaml

with open("/etc/tibber.yaml", encoding="utf-8") as config_file:
    config = yaml.safe_load(config_file)

query = """
query FetchPriceInfo($homeId: ID!) {
  viewer {
    home(id: $homeId) {
      currentSubscription {
        priceInfo(resolution: QUARTER_HOURLY) {
          today {
            total
            startsAt
          }
          tomorrow {
            total
            startsAt
          }
        }
      }
    }
  }
}
"""

response = json.loads(
    requests.post(
        "https://api.tibber.com/v1-beta/gql",
        json={"query": query, "variables": {"homeId": config["home_id"]}},
        headers={"Authorization": f"Bearer {config['token']}"},
    ).content.decode("UTF-8")
)

price_info = (
    response.get("data", {})
    .get("viewer", {})
    .get("home", {})
    .get("currentSubscription", {})
    .get("priceInfo", {})
)

formatted_data = [
    {"price": entry["total"], "time": entry["startsAt"]}
    for day in ("today", "tomorrow")
    for entry in (price_info.get(day) or [])
]

json.dump(formatted_data, sys.stdout)
