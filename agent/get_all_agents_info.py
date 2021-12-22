#!/usr/bin/python
# -*- coding: utf-8 -*-

# ************************************************************
# Copyright © 2019-2021 Acronis International GmbH.
# This source code is distributed under MIT software license.
# ************************************************************

import json			# used for manipulating JSON data
import pprint		# used for formatting the output of JSON objects received in API responses
import os
import sys

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, base_path)

from common.base_operations import Config, Tenant, Acronis

# Initialize config and read all required values form JSON config
# an API client and a token files
cfg = Config(full=True)
acronis = Acronis(cfg)

response = acronis.get(
    f'api/agent_manager/v2/agents'
)

if response.ok:
    with open(os.path.join(base_path, 'all_agents.json'), 'w') as outfile:
        json.dump(response.json(), outfile)
else:
    pprint.pprint(response.json())
