#!/usr/bin/python
# -*- coding: utf-8 -*-

# ************************************************************
# Copyright © 2019-2021 Acronis International GmbH.
# This source code is distributed under MIT software license.
# ************************************************************

import json			# used for manipulating JSON data
import pprint  		# used for formatting the output of JSON objects received in API responses
from datetime import datetime, timedelta, timezone

import os
import sys

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, base_path)

from common.base_operations import Config, Acronis

# Initialize config and read all required values form JSON config
# an API client and a token files
cfg = Config(full=True)
acronis = Acronis(cfg)

# Create an acceptable date for tasks filtering
last_week = (datetime.today() - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
# Unix Time in nanoseconds (1 billionth of a second)
last_week = last_week.replace(tzinfo=timezone.utc).timestamp()*1000000000

filters = {
     'updated_at': f'gt({int(last_week)})',
     'order': 'desc(created_at)'
}

# Request for all alerts, which were updated last 7 days
response = acronis.get(
    'api/alert_manager/v1/alerts',
    data=filters
)

if response.ok:
    with open(os.path.join(base_path, f'alerts_{int(last_week)}.json'), 'w') as outfile:
        json.dump(response.json(), outfile)

    # Filter JSON to create 3 lists
    # Warnings
    warning_alerts = [
        alert for alert in response.json()["items"]
        if (
            alert["severity"] == "warning"
        )
        ]

    with open(os.path.join(base_path, f'alerts_{int(last_week)}_warning.json'), 'w') as outfile:
        json.dump(warning_alerts, outfile)

    # Filter JSON to create 3 lists
    # Errors
    error_alerts = [
        alert for alert in response.json()["items"]
        if (
            alert["severity"] == "error"
        )
        ]

    with open(os.path.join(base_path, f'alerts_{int(last_week)}_error.json'), 'w') as outfile:
        json.dump(error_alerts, outfile)

    # Filter JSON to create 3 lists
    # Critical
    critical_alerts = [
        alert for alert in response.json()["items"]
        if (
            alert["severity"] == "critical"
        )
        ]

    with open(os.path.join(base_path, f'alerts_{int(last_week)}_critical.json'), 'w') as outfile:
        json.dump(critical_alerts, outfile)

    print(f'Critical: {len(critical_alerts)}')
    print(f'Errors: {len(error_alerts)}')
    print(f'Warnings: {len(warning_alerts)}')
else:
    pprint.pprint(response.json())
