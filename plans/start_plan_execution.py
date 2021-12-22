#!/usr/bin/python
# -*- coding: utf-8 -*-

# ************************************************************
# Copyright © 2019-2021 Acronis International GmbH.
# This source code is distributed under MIT software license.
# ************************************************************

import json
import pprint       # used for formatting the output of JSON objects received in API responses

import os
import sys

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, base_path)

from common.base_operations import Acronis, Config

# Initialize config and read all required values form JSON config
# an API client and a token files
cfg = Config(full=True)
acronis = Acronis(cfg)

# Request resources with type machines available for the current authorization scope
response = acronis.get(
    "api/resource_management/v4/resources?type=resource.machine"
)

# If we have any machine and not an error in response
if response.ok and "items" in response.json() and len(response.json()["items"]) > 0:
    # Get the first machine id
    first_machine_id = response.json()["items"][0]["id"]

    # Find applied policy
    response = acronis.get(
        f"/api/policy_management/v4/applications?context_id={first_machine_id}&policy_type=policy.backup.machine"
    )

    # If we have any applicable plan and not an error in response
    if response.ok and "items" in response.json() and len(response.json()["items"]) > 0:
       # Get the first applicable total policy
        # Either parent or have no parent
        if "parent_ids" in response.json()["items"][0][0]["policy"]:
            first_applicable_policy = response.json()["items"][0][0]["policy"]["parent_ids"][0]
        else:
            first_applicable_policy = response.json()["items"][0][0]["policy"]["id"]

        start = {
            "state": "running",
            "policy_id": f"{first_applicable_policy}",
            "context_ids": [f"{first_machine_id}"]
        }

        # Run the first applicable policy for the first found machines
        # FOR DEMO PURPOSES ONLY
        response = acronis.put(
                "/api/policy_management/v4/applications/run",
                data=json.dumps(start)
        )

        if response.ok:
            print("The plan execution successfully started for the first machine.")
            pprint.pprint(response.json())
        else:
            pprint.pprint(response.json())
    else:
        print("There are no plans to start.")
        pprint.pprint(response.json())
else:
    print("There are no resources to start a plan execution.")
    pprint.pprint(response.json())
