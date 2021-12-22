#!/usr/bin/python
# -*- coding: utf-8 -*-

# ************************************************************
# Copyright © 2019-2021 Acronis International GmbH.
# This source code is distributed under MIT software license.
# ************************************************************

import json			# used for manipulating JSON data
import pprint  # used for formatting the output of JSON objects received in API responses
from datetime import datetime, timedelta

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
last_week = datetime.today() - timedelta(days=7)

filters = {
     'completedAt': f'gt({last_week.strftime("%Y-%m-%dT00:00:00Z")})'
}

# Request for all activities, which were completed last 7 days
response = acronis.get(
    'api/task_manager/v2/activities',
    data=filters
)

if response.ok:
    with open(os.path.join(base_path, f'activities_{last_week.strftime("%Y-%m-%d")}.json'), 'w') as outfile:
        json.dump(response.json(), outfile)

    if response.json()["size"] > 0:
        # Filter JSON to create 3 lists
        # Successfully Completed Activities
        completed_ok_activities = [
            activity for activity in response.json()["items"]
            if (
                activity["state"] == "completed"
                and
                activity["result"]["code"] == "ok"
            )
            ]

        with open(os.path.join(base_path, f'activities_{last_week.strftime("%Y-%m-%d")}_ok.json'), 'w') as outfile:
            json.dump(completed_ok_activities, outfile)

        # Filter JSON to create 3 lists
        # Activities Completed With Error
        completed_error_activities = [
            activity for activity in response.json()["items"]
            if (
                activity["state"] == "completed"
                and
                activity["result"]["code"] == "error"
            )
            ]

        with open(os.path.join(base_path, f'activities_{last_week.strftime("%Y-%m-%d")}_error.json'), 'w') as outfile:
            json.dump(completed_error_activities, outfile)

        # Filter JSON to create 3 lists
        # Activities Completed With Warning
        completed_warning_activities = [
            activity for activity in response.json()["items"]
            if (
                activity["state"] == "completed"
                and
                activity["result"]["code"] == "warning"
            )
            ]

        with open(os.path.join(base_path, f'activities_{last_week.strftime("%Y-%m-%d")}_warning.json'), 'w') as outfile:
            json.dump(completed_warning_activities, outfile)

        print(f'Successful: {len(completed_ok_activities)}')
        print(f'Errors: {len(completed_error_activities)}')
        print(f'Warnings: {len(completed_warning_activities)}')
    else:
        pprint.pprint(response.json())
else:
    pprint.pprint(response.json())
