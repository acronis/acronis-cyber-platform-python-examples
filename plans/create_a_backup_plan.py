#!/usr/bin/python
# -*- coding: utf-8 -*-

# ************************************************************
# Copyright © 2019-2021 Acronis International GmbH.
# This source code is distributed under MIT software license.
# ************************************************************

import json			# used for manipulating JSON data
import pprint       # used for formatting the output of JSON objects received in API responses
import uuid

import os
import sys

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
script_path = os.path.join(os.path.dirname(__file__))
sys.path.insert(0, base_path)

from common.base_operations import Acronis, Config

# Initialize config and read all required values form JSON config
# an API client and a token files
cfg = Config(full=True)
acronis = Acronis(cfg)

with open(os.path.join(script_path, 'base_plan.json')) as base_plan_file:
    base_plan = json.load(base_plan_file)

backup_plan_uuid = str(uuid.uuid4())
total_protection_plan_uuid = str(uuid.uuid4())

base_plan["subject"]["policy"][0]["id"] = total_protection_plan_uuid
base_plan["subject"]["policy"][1]["parent_ids"][0] = total_protection_plan_uuid
base_plan["subject"]["policy"][1]["id"] = backup_plan_uuid

response = acronis.post(
    'api/policy_management/v4/policies',
    data=json.dumps(base_plan)
)

if response.ok:
    with open(os.path.join(base_path, 'plan_creation_response.json'), 'w') as outfile:
        json.dump(response.json(), outfile)

    print("The base backup plan created successfully.")
else:
    pprint.pprint(response.json())
