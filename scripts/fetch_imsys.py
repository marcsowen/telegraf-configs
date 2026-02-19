#!/usr/bin/env python3

import json
import requests
import yaml
from datetime import date, timedelta
from bs4 import BeautifulSoup
from requests.auth import HTTPDigestAuth
from urllib3.exceptions import InsecureRequestWarning


def fetch_meter(url, token, cookies, type):
    today = date.today()
    from_date = (today - timedelta(days=1)).isoformat()
    to_date = today.isoformat()
    post_data = "tkn=" + token + "&action=meterform"
    res = requests.post(url, data=post_data, cookies=cookies, verify=False)
    soup = BeautifulSoup(res.content, 'html.parser')
    sel = soup.find(id='meterform_select_meter')
    meter_id = sel.find().attrs.get('value')
    post_data = "tkn=" + token + "&action=showMeterValues&mid=" + meter_id + "&from=" + from_date + "&to=" + to_date
    res = requests.post(url, data=post_data, cookies=cookies, verify=False)
    soup = BeautifulSoup(res.content, 'html.parser')
    table_data = soup.find('table', id="metervalue")
    rows = table_data.find_all('tr')[1:]
    meter_data = []
    for row in rows:
        meter_data.append({
            'timestamp': row.find(id="table_metervalues_col_timestamp").string,
            'type': type,
            'value': float(row.find(id="table_metervalues_col_wert").string),
        })
    return meter_data


def fetch_token_and_cookies(url, username, password):
    res = requests.get(
        url,
        auth=HTTPDigestAuth(username, password),
        verify=False,
    )
    cookies = res.cookies
    soup = BeautifulSoup(res.content, 'html.parser')
    tags = soup.find_all('input')
    token = tags[0].get('value')
    return token, cookies


requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

config = yaml.safe_load(open("/etc/imsys.yaml"))
url = 'https://' + config["ip"] + '/cgi-bin/hanservice.cgi'

data = []

for type in ['consumption', 'feedin']:
    token, cookies = fetch_token_and_cookies(
        url,
        config[type + '_user'],
        config[type + '_password'],
    )
    data.extend(fetch_meter(url, token, cookies, type))


print(json.dumps(data))
