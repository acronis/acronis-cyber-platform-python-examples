#!/usr/bin/python
# -*- coding: utf-8 -*-

# ************************************************************
# Copyright © 2019-2021 Acronis International GmbH.
# This source code is distributed under MIT software license.
# ************************************************************

import json			# used for manipulating JSON data
import pprint       # used for formatting the output of JSON objects received in API responses
import time

import os
import sys

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, base_path)

from common.base_operations import Acronis, Config

# Initialize config and read all required values form JSON config
# an API client and a token files
cfg = Config(full=True)
acronis = Acronis(cfg)

report = {
    "parameters": {
        "kind": "usage_summary",
        "tenant_id": f"{cfg.tenant_id}",
        "level": "direct_partners",
        "formats": [
            "csv_v2_0"
        ],
        "show_skus": "true",
        "hide_zero_usage": "false",
        "period": {
            "start": "2021-10-01",
            "end": "2021-10-31"
        }
    },
    "schedule": {
        "type": "once"
    },
    "result_action": "save"
}

response = acronis.post(
    'api/2/reports',
    data=json.dumps(report)
)

if response.ok:
    report_status = "non saved"
    report_id = response.json()["id"]
    stored_report_id = None

    while report_status != "saved":
        response = acronis.get(
            f'api/2/reports/{report_id}/stored'
         )

        if response.ok:
            report_status = response.json()["items"][0]["status"]
        else:
            pprint.pprint(response.json())

        time.sleep(2)

    stored_report_id = response.json()["items"][0]["id"]

    response = acronis.get(
        f'api/2/reports/{report_id}/stored/{stored_report_id}',
        )

    if response.ok:
        with open(os.path.join(base_path, f'sku_report_for_tenant_{cfg.tenant_id}.csv'), 'w') as outfile:
            outfile.write(response.text)
    else:
        pprint.pprint(response.json())
else:
    pprint.pprint(response.json())
