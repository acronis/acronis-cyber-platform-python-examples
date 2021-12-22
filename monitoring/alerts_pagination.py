# ************************************************************
# Copyright © 2019-2021 Acronis International GmbH.
# This source code is distributed under MIT software license.
# ************************************************************

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
last_week = last_week.replace(tzinfo=timezone.utc).timestamp()*1000000

# Page size
page_size = 10

filters = {
     'limit': f'{page_size}',
     'updated_at': f'gt({int(last_week)})'
}

# Request for all alerts, which were updated last 7 days
response = acronis.get(
    'api/alert_manager/v1/alerts',
    data=filters
)

if response.ok:
    page_number = 1

    print(f"The page number {page_number}")

    while "after" in response.json()["paging"]["cursors"]:
        filters = {
            'limit': f'{page_size}',
            'updated_at': f'gt({int(last_week)})',
            'after': f'{response.json()["paging"]["cursors"]["after"]}'
        }

        response = acronis.get(
            'api/alert_manager/v1/alerts',
            data=filters
        )

        if response.ok:
            page_number = page_number + 1
            print(f"The page number {page_number}")
        else:
            pprint.pprint(response.json())
            print("An error occurred during alerts paging.")
            exit

    print("The alerts were paged to the end.")

    page_number = page_number - 1

    print(f"The page number {page_number}")

    size = page_size

    while "before" in response.json()["paging"]["cursors"]:
        filters = {
            'limit': f'{page_size}',
            'updated_at': f'gt({int(last_week)})',
            'before': f'{response.json()["paging"]["cursors"]["before"]}'
        }

        response = acronis.get(
            'api/alert_manager/v1/alerts',
            data=filters
        )

        if response.ok:
            page_number = page_number - 1
            print(f"The page number {page_number}")
        else:
            pprint.pprint(response.json())
            print("An error occurred during alerts paging.")
            exit

    print("The alerts were paged to the start.")
else:
    pprint.pprint(response.json())
