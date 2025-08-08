#!/usr/bin/python3
import json
import sys
import time

import tinytuya
import yaml

config = yaml.safe_load(open("/etc/tuya.yaml"))

mode_mapping = {
    "Cooling": 0,
    "Heating": 1,
    "Auto": 2
}

work_mode_mapping = {
    "Silence": 0,
    "Smart": 1,
    "Boost": 2,
}

d = tinytuya.Device(config["device_id"], config["ip_address"], config["local_key"], version=config["version"])
status = d.status()['dps']

formatted_data = []

formatted_entry = {
        "timestamp": int(time.time()),
        "device_id": d.id,
        "switch": status['1'],
        "mode": mode_mapping[status['2']],
        "temp_set": status['4'] / 10,
        "work_mode": work_mode_mapping[status['5']],
        "fault": status['15'],
        "temp_current": status['16'] / 10
    }

formatted_data.append(formatted_entry)

json.dump(formatted_data, sys.stdout)