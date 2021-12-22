#!/usr/bin/python
# -*- coding: utf-8 -*-

# ************************************************************
# Copyright © 2019-2021 Acronis International GmbH.
# This source code is distributed under MIT software license.
# ************************************************************

import pprint  		# used for formatting the output of JSON objects received in API responses
import calendar     # used for datetimes convertions
from datetime import datetime

import os
import sys
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, base_path)

from common.base_operations import Config, BearerAuth, Tenant, Acronis

# Initialize config and read all required values form JSON config
# an API client and a token files
cfg = Config(full=True)
acronis = Acronis(cfg)

customer = Tenant(os.path.join(base_path, "customer.json"))

response = acronis.get(
                f'api/2/tenants/{customer.tenant_id}/pricing'
            )

if response.ok:
    pricing = response.json()
    trial_end = pricing["production_start_date"]

    print(trial_end)
else:
    pprint.pprint(response.json())
