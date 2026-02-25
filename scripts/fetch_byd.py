#!/usr/bin/python3
import json
import sys
import time

from pymodbus import FramerType
from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient(host='192.168.178.28', port=8080, framer=FramerType.RTU)
client.connect()

formatted_data = []

for module in range(1, 3):
    client.write_registers(0x0550, [module, 0x8100])
    while client.read_holding_registers(0x0551).registers[0] != 0x8801:
        time.sleep(.1)

    # Measurement done, collect timestamp.
    timestamp = time.time()

    data = []
    for _ in range(0, 5):
        data = data + client.read_holding_registers(0x0558, count=0x41).registers[1:]

    for cell in range(0, 16):

        formatted_entry = {
            "module": module,
            "cell": cell + 1,
            "timestamp": int(timestamp),
            "firmware_A": 'v%d.%d' % (data[30] & 0xff, data[30] >> 8),
            "firmware_B": 'v%d.%d' % (data[31] & 0xff, data[31] >> 8),
            "firmware_select": data[32],
            "table_A": 'v%d.%d' % (data[45] & 0xff, data[45] >> 8),
            "table_B": 'v%d.%d' % (data[46] & 0xff, data[46] >> 8),
            "warning1": data[27],
            "warning2": data[28],
            "warning3": data[29],
            "fault": data[47],
            "soc": data[24] * 0.1,
            "voltage": data[48 + cell] * 0.001,
            "datapoint": cell // 4,
            "temperature": data[177 + cell // 4] >> 8 if (cell % 4) // 2 == 0 else data[177 + cell // 4] & 0xFF,
        }

        formatted_data.append(formatted_entry)

json.dump(formatted_data, sys.stdout)
