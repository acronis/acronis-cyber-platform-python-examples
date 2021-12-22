# ************************************************************
# Copyright © 2019-2021 Acronis International GmbH.
# This source code is distributed under MIT software license.
# ************************************************************

import pprint  		# used for formatting the output of JSON objects received in API responses
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

# Create an acceptable date for activities filtering
last_week = datetime.today() - timedelta(days=7)

# Page size
page_size = 10

filters = {
     'limit': f'{page_size}',
     'lod': 'short',
     'completedAt': f'gt({last_week.strftime("%Y-%m-%dT00:00:00Z")})'
}

# Request for all activities, which were completed last 7 days by page_size activities
response = acronis.get(
    'api/task_manager/v2/activities',
    data=filters
)

if response.ok:
    page_number = 1

    print(f"The page number {page_number}")

    while "paging" in response.json() and "after" in response.json()["paging"]["cursors"]:
        filters = {
            'limit': f'{page_size}',
            'lod': 'short',
            'after': f'{response.json()["paging"]["cursors"]["after"]}'
        }

        response = acronis.get(
            'api/task_manager/v2/activities',
            data=filters
        )

        if response.ok:
            page_number = page_number + 1
            print(f"The page number {page_number}")
        else:
            pprint.pprint(response.json())
            print("An error occurred during activities paging.")
            exit

    print("The activities were paged to the end.")
else:
    pprint.pprint(response.json())
