#!/usr/bin/python
# -*- coding: utf-8 -*-

# ************************************************************
# Copyright © 2019-2021 Acronis International GmbH.
# This source code is distributed under MIT software license.
# ************************************************************

import json			# used for manipulating JSON data
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

# Construct JSON to request
# 301d1574-849e-4714-859f-3a2ec12a218b is predefined id for "Machines with agents" static group
# Thus this Static group is expected to contain machines with agents
# We need to have at least 1 machine w/agent to see that groups
# group_condition is SQL-like conditions using available fields and conditions
# the same as used in UI for group creation can be used in API. 
# The valid operators for condition are `=`, `!=`, `<`, `>`, `<=`, `>=`, `AND`, `OR`, `IN`, `NOT IN`, `LIKE`, `RANGE`. 
# Here is you can find more details https://dl.managed-protection.com/u/baas/help/20.10/user/en-US/index.html#cshid=46985
# If you have only condition to a resource name, you may not provide the field name, just condition.
# ****************************************************
# NOTICE. You can't add a sub-group to a dynamic group
# ****************************************************
group = {
    "type": "resource.group.computers",
    "parent_group_ids": [
        "301d1574-849e-4714-859f-3a2ec12a218b"
        ],
    "group_condition": "test*",
    "allowed_member_types": [
        "resource.machine"
    ],
    "name": "My Dynamic Group",
    "user_defined_name": "My Dynamic Group"
}

response = acronis.get(
    'api/resource_management/v4/resources',
    data=json.dumps(group)
)

if response.ok:
    print("Dynamic group created successfully.")
else:
    pprint.pprint(response.json())
