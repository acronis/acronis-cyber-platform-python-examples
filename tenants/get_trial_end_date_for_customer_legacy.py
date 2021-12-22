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
    creation_unixtime = pricing["version"]

    creation_datetime = datetime.utcfromtimestamp(creation_unixtime/1000.)

    if creation_datetime.day > 1:
        trial_end_month = creation_datetime.replace(month=creation_datetime.month+1)
    else:
        trial_end_month = creation_datetime

    last_day_of_month = calendar.monthrange(trial_end_month.year, trial_end_month.month)[1]
    trial_end = trial_end_month.replace(day=last_day_of_month, hour=23, minute=59, second=59,microsecond=999999)

    print(trial_end)
else:
    pprint.pprint(response.json())
