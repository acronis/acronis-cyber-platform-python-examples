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

customer = Tenant(os.path.join(base_path, 'customer.json'))

# Retrieve int tenant id by uuid tenant id
response = acronis.get(
         f"api/1/groups/{customer.tenant_id}"
        )

if response.ok:

    customer = Tenant(json_str=response.text)

    # Get list of all Acronis Agents for tenants subtree
    # where the root tenant is
    # a previously created customer
    response = acronis.get(
            f'api/agent_manager/v2/agents?tenant_id={customer.tenant_id}'
        )

    if response.ok:
        with open(os.path.join(base_path, 'customer_agents.json'), 'w') as outfile:
            json.dump(response.json(), outfile)
    else:
        pprint.pprint(response.json())
else:
    pprint.pprint(response.json())
